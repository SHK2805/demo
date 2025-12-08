// =============================================
// Tunables
// =============================================
let timeWindow = 4h;                          // Lookback around the alert
let maxRareThreshold = 3;                     // Max occurrences allowed to still consider "rare"
let alertIdSeed = "PUT-YOUR-ALERT-ID-HERE";   // Replace with your actual AlertId

// =============================================
// Stage 1 - Pull the alert and evidence
// =============================================
let seedAlert =
    SecurityAlert
    | where AlertId == alertIdSeed
    | project AlertId, Title, Severity, VendorName, ProductName, TimeGenerated;

let ev =
    AlertEvidence
    | where AlertId == alertIdSeed
    | project AlertId, Timestamp, DeviceId, DeviceName, AccountDomain, AccountName,
              FileName, FilePath, ProcessCommandLine, Sha1, Sha256,
              RemoteUrl, RemoteIP, RemotePort, EvidenceRole, EvidenceType;

// =============================================
// Stage 2 - Enrich with process, network, file, logon context
// =============================================

// Process context
let procCtx =
    DeviceProcessEvents
    | where Timestamp between (ago(timeWindow) .. now())
    | where DeviceName in (ev | project DeviceName)
    | project Timestamp, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine,
              InitiatingProcessParentFileName, InitiatingProcessParentCommandLine, FileName, FolderPath, SHA1, SHA256;

// Network context
let netCtx =
    DeviceNetworkEvents
    | where Timestamp between (ago(timeWindow) .. now())
    | where DeviceName in (ev | project DeviceName)
    | project Timestamp, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine,
              LocalIP, LocalPort, RemoteIP, RemotePort, Protocol, Action;

// File context
let fileCtx =
    DeviceFileEvents
    | where Timestamp between (ago(timeWindow) .. now())
    | where DeviceName in (ev | project DeviceName)
    | project Timestamp, DeviceName, FileName, FolderPath, InitiatingProcessCommandLine;

// Logon context
let logonCtx =
    DeviceLogonEvents
    | where Timestamp between (ago(timeWindow) .. now())
    | where DeviceName in (ev | project DeviceName)
    | project Timestamp, DeviceName, AccountDomain, AccountName, LogonType, LogonSucceeded;

// =============================================
// Stage 3 - Behavioral funnels for lateral movement
// =============================================

// Service execution / remote service control
let svcExec =
    procCtx
    | extend cmdLower = tolower(InitiatingProcessCommandLine)
    | where cmdLower contains "\\\\"
        and (cmdLower has_any ("sc ", "create", "start", "config", "psexec"))
    | summarize Occurrences = count(), FirstSeen=min(Timestamp), LastSeen=max(Timestamp)
      by DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine
    | where Occurrences <= maxRareThreshold;

// RDP chains
let rdpChains =
    logonCtx
    | where LogonType in ("RemoteInteractive","Network")
    | project Account = strcat(AccountDomain, "\\", AccountName), DeviceName, Timestamp
    | join kind=inner (
        logonCtx
        | where LogonType == "RemoteInteractive"
        | project Account = strcat(AccountDomain, "\\", AccountName), DeviceName, Timestamp
    ) on Account
    | where $left.DeviceName != $right.DeviceName
      and abs(datetime_diff("minute", $left.Timestamp, $right.Timestamp)) <= 30
    | summarize Occurrences=count(),
                FirstSeen=min($left.Timestamp),
                LastSeen=max($right.Timestamp),
                SourceDevices=make_set($left.DeviceName, 5),
                TargetDevices=make_set($right.DeviceName, 5)
      by Account
    | where Occurrences <= maxRareThreshold;

// SOCKS tunneling indicators
let socksPivot =
    netCtx
    | extend portsOfInterest = iff(RemotePort in (1080,8080,9050) or LocalPort in (1080,8080,9050), 1, 0)
    | extend cmdLower = tolower(InitiatingProcessCommandLine)
    | where portsOfInterest == 1 or cmdLower has_any ("socks","proxychains"," -d "," -D ")
    | summarize Occurrences=count(), FirstSeen=min(Timestamp), LastSeen=max(Timestamp),
                Examples=make_set(InitiatingProcessCommandLine, 5)
      by DeviceName
    | where Occurrences <= maxRareThreshold;

// =============================================
// Final union and output
// =============================================
svcExec
| extend Signal="ServiceExec"
| union (rdpChains | extend Signal="RDP Chain")
| union (socksPivot | extend Signal="SOCKS/Proxy")
| join kind=leftouter seedAlert on $left.DeviceName == $right.ProductName
| project AlertId, Title, Severity, TimeGenerated,
          Signal, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine,
          Occurrences, FirstSeen, LastSeen
| order by LastSeen desc
