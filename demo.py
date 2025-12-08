let timeWindow=4h;
let maxRareThreshold=3;
let alertIdSeed="PUT-YOUR-ALERT-ID-HERE";

let seedAlert=AlertInfo
| where AlertId==alertIdSeed
| project AlertId,Title,Severity,TimeGenerated;

let ev=AlertEvidence
| where AlertId==alertIdSeed
| project AlertId,DeviceName,AccountDomain,AccountName;

// svcExec with AlertId attached
let svcExec=DeviceProcessEvents
| where Timestamp between (ago(timeWindow)..now())
| join kind=inner (ev|project AlertId,DeviceName) on DeviceName
| extend cmdLower=tolower(InitiatingProcessCommandLine)
| where cmdLower contains "\\\\" and (cmdLower has_any("sc ","create","start","config","psexec"))
| summarize Occurrences=count(),FirstSeen=min(Timestamp),LastSeen=max(Timestamp) by AlertId,DeviceName,InitiatingProcessFileName,InitiatingProcessCommandLine
| where Occurrences<=maxRareThreshold
| extend Signal="ServiceExec";

// rdpChains with AlertId attached
let rdpLeft=DeviceLogonEvents
| where Timestamp between (ago(timeWindow)..now())
| join kind=inner (ev|project AlertId,DeviceName,AccountDomain,AccountName) on DeviceName
| project AlertId,Account=strcat(AccountDomain,"\\",AccountName),SourceDevice=DeviceName,SourceTimestamp=Timestamp;

let rdpRight=DeviceLogonEvents
| where Timestamp between (ago(timeWindow)..now())
| join kind=inner (ev|project AlertId,DeviceName,AccountDomain,AccountName) on DeviceName
| where LogonType=="RemoteInteractive"
| project AlertId,Account=strcat(AccountDomain,"\\",AccountName),TargetDevice=DeviceName,TargetTimestamp=Timestamp;

let rdpChains=rdpLeft
| join kind=inner rdpRight on Account,AlertId
| where SourceDevice!=TargetDevice and abs(datetime_diff("minute",SourceTimestamp,TargetTimestamp))<=30
| summarize Occurrences=count(),FirstSeen=min(SourceTimestamp),LastSeen=max(TargetTimestamp),SourceDevices=make_set(SourceDevice,5),TargetDevices=make_set(TargetDevice,5) by AlertId,Account
| where Occurrences<=maxRareThreshold
| extend Signal="RDP Chain";

// socksPivot with AlertId attached
let socksPivot=DeviceNetworkEvents
| where Timestamp between (ago(timeWindow)..now())
| join kind=inner (ev|project AlertId,DeviceName) on DeviceName
| extend portsOfInterest=iff(RemotePort in(1080,8080,9050) or LocalPort in(1080,8080,9050),1,0)
| extend cmdLower=tolower(InitiatingProcessCommandLine)
| where portsOfInterest==1 or cmdLower has_any("socks","proxychains"," -d "," -D ")
| summarize Occurrences=count(),FirstSeen=min(Timestamp),LastSeen=max(Timestamp),Examples=make_set(InitiatingProcessCommandLine,5) by AlertId,DeviceName
| where Occurrences<=maxRareThreshold
| extend Signal="SOCKS/Proxy";

// final union and join
svcExec
| union rdpChains
| union socksPivot
| join kind=leftouter seedAlert on AlertId
| project AlertId,Title,Severity,TimeGenerated,Signal,DeviceName,InitiatingProcessFileName,InitiatingProcessCommandLine,Occurrences,FirstSeen,LastSeen
| order by LastSeen desc
