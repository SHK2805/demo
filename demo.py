let targetSender = "worker@example.com";  // Replace with actual sender
let targetDate = datetime(2025-09-02);    // Replace with your target date
let emailEvents = EmailEvents
    | where SenderFromAddress =~ targetSender
    | where Timestamp between (targetDate .. targetDate + 1d)
    | project ReportId, NetworkMessageId, EmailSubject=Subject, SenderFromAddress, RecipientEmailAddress, Timestamp, ThreatTypes, DeliveryAction;
let attachments = EmailAttachmentInfo
    | project NetworkMessageId, AttachmentName=FileName, FileType, SHA256, MalwareDetectionName;
let urls = EmailUrlInfo
    | project NetworkMessageId, Url, UrlDomain, UrlClickAction;
let clicks = UrlClickEvents
    | project NetworkMessageId, ClickTimestamp=ClickDateTime, ClickedUrl=Url, ClickedBy=UserPrincipalName, DeviceName;
let executions = DeviceFileEvents
    | project SHA256, ExecutionTimestamp=Timestamp, ExecutedOn=DeviceName, FileName, FolderPath, InitiatingProcessFileName, InitiatingProcessCommandLine;

emailEvents
| join kind=leftouter attachments on NetworkMessageId
| join kind=leftouter urls on NetworkMessageId
| join kind=leftouter clicks on NetworkMessageId
| join kind=leftouter executions on SHA256
| project Timestamp, SenderFromAddress, RecipientEmailAddress, EmailSubject, ThreatTypes, DeliveryAction,
          AttachmentName, FileType, MalwareDetectionName,
          Url, UrlDomain, UrlClickAction, ClickTimestamp, ClickedBy, DeviceName,
          ExecutionTimestamp, ExecutedOn, FileName, FolderPath, InitiatingProcessFileName, InitiatingProcessCommandLine
| sort by Timestamp desc


           -----
let alertId = "your_alert_id_here";  // Replace with actual AlertId

// Step 1: Get core alert metadata
let alertDetails = AlertInfo
| where AlertId == alertId
| project AlertId, Title, Category, Severity, DetectionSource, ServiceSource, Timestamp, AttackTechniques;

// Step 2: Get all evidence tied to the alert
let evidence = AlertEvidence
| where AlertId == alertId
| project AlertId, EntityType, EvidenceRole, FileName, FolderPath, SHA256, DeviceName, AccountName, RemoteIP, RemoteUrl;

// Step 3: Trace process execution from evidence
let processEvents = DeviceProcessEvents
| where Timestamp > ago(7d)
| where FileName in (evidence | where EntityType == "File" | project FileName)
| project Timestamp, DeviceName, FileName, ProcessCommandLine, InitiatingProcessFileName, InitiatingProcessCommandLine;

// Step 4: Trace file activity from evidence
let fileEvents = DeviceFileEvents
| where Timestamp > ago(7d)
| where SHA256 in (evidence | where EntityType == "File" | project SHA256)
| project Timestamp, DeviceName, FileName, FolderPath, SHA256, ActionType, InitiatingProcessFileName;

// Step 5: Trace network activity from evidence
let networkEvents = DeviceNetworkEvents
| where Timestamp > ago(7d)
| where RemoteIP in (evidence | where EntityType == "IpAddress" | project RemoteIP)
| project Timestamp, DeviceName, RemoteIP, RemotePort, InitiatingProcessFileName, InitiatingProcessCommandLine;

// Combine all views
alertDetails
| join kind=leftouter evidence on AlertId
| join kind=leftouter processEvents on DeviceName
| join kind=leftouter fileEvents on DeviceName
| join kind=leftouter networkEvents on DeviceName
| project Timestamp, AlertId, Title, Severity, DeviceName, AccountName,
          FileName, FolderPath, SHA256, ProcessCommandLine, InitiatingProcessFileName,
          RemoteIP, RemotePort, RemoteUrl, AttackTechniques
| sort by Timestamp desc

