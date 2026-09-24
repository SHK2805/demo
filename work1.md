
Act strictly as a Microsoft Defender XDR KQL Query Generator. 

Based on the attack details below, generate standalone, optimized Advanced Hunting (KQL) queries for the Defender XDR schema. Do NOT include narrative summaries, remediation advice, or background explanations—output ONLY the KQL queries with clear table mappings and functional comments.

### ATTACK CONTEXT:
- Incident: Network token extraction on non-rooted Android device
- Device Name: AndroidForWork_12
- User Account: CLIENT\A12345 (UPN: test@tester.com)
- Source IP: 3.11.236.40
- Date/Time: 2026-08-25 16:07 UTC
- Mechanism: Rogue Root CA installed in Android personal profile to intercept traffic to graph.microsoft.com during passkey generation.
- Extracted Scopes: UserAuthenticationMethod.Read, UserAuthenticationMethod.ReadWrite, email, openid, profile
- Post-Exploitation Action: Graph API endpoint `/beta/users` accessed for directory enumeration.

---

### INSTRUCTIONS FOR QUERIES:

Generate separate KQL queries covering the following operational objectives:

1. **Sign-In & Auth Monitoring (AADInteractiveUserSignInLogs / AADNonInteractiveUserSignInLogs):**
   - Query for sign-in attempts from IP `3.11.236.40` or account `test@tester.com` around `2026-08-25T16:07:00Z`.
   - Filter for token requests issued with `UserAuthenticationMethod` scopes or anomalous user-agents.

2. **Microsoft Graph Directory Enumeration (MicrosoftGraphActivityLogs / CloudAppEvents):**
   - Query for API operations targeting `/beta/users` or `/v1.0/users` from IP `3.11.236.40` or associated with account `CLIENT\A12345`.
   - Highlight GET requests and high-volume response payloads indicating user enumeration.

3. **Device & Network Activity (DeviceInfo / DeviceNetworkEvents / DeviceProcessEvents):**
   - Query for network connections originating from `AndroidForWork_12` toward `3.11.236.40` or non-standard proxy ports around the timestamp.

4. **Broader Anomaly Detection (IdentityLogonEvents / Behavioral Correlation):**
   - Query for subsequent authentications using the extracted authentication methods or sessions originating from IP `3.11.236.40` across all tenant resources.

Ensure all queries use explicit `TimeGenerated` / `Timestamp` window filters centered around `2026-08-25T16:07:00Z` (+/- 2 hours) and project key diagnostic fields.
