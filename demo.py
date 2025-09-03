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
