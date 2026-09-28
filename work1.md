// Title: iOS MDM Enrolment TLS Pinning Failure Detection
// Description: Identifies network connections to Apple/Intune enrollment endpoints that failed or were reset during the TLS handshake.
DeviceNetworkEvents
| where TimeGenerated > ago(24h)
// 1. Filter for critical Apple and Microsoft enrollment endpoints
| where RemoteUrl has_any (
    "://apple.com", 
    "://apple.com", 
    "://apple.com", 
    "://microsoft.com"
)
// 2. Look for aborted, reset, or failed connection actions
| where ActionType in~ ("ConnectionFailed", "ConnectionAborted") or AdditionalFields has_any ("Reset", "HandshakeFailed", "TLS_Error")
// 3. Focus on iOS devices (or general mobile clients if OS is unknown in proxy data)
| where DeviceName has "iOS" or InitiatingProcessOsPlatform =~ "IOS" or isempty(InitiatingProcessOsPlatform)
| project TimeGenerated, DeviceName, LocalIP, RemoteUrl, RemoteIP, RemotePort, ActionType, AdditionalFields
| order by TimeGenerated desc
