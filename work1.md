You are an expert Threat Hunter and Incident Response Specialist analyzing a security incident involving network-based token extraction via a rogue CA on an Android device. 

Use the incident parameters and detailed context below to construct Advanced Hunting (KQL) queries, perform impact analysis, evaluate risk, and outline containment and remediation steps.

---
### INCIDENT DETAILS:
- Incident Name: Network token extraction on non-rooted Android device
- Target Device: AndroidForWork_12
- User Account: CLIENT\A12345 (Test account: test@tester.com)
- Source/Attacker IP: 3.11.236.40
- Timestamp: 25/08/2026 16:07 UTC
- Result: Pass (Token successfully extracted)

### TECHNICAL ATTACK CONTEXT:
1. Attack Technique: Rogue User CA installation into the personal profile of an unrooted Android enterprise device.
2. Interception Mechanism: TLS Passthrough configured for all domains except graph.microsoft.com. Microsoft Authenticator trusts user-installed CAs (due to Network Security Config permissions), bypassing SSL certificate pinning for Graph endpoints.
3. Trigger Action: A failed passkey generation attempt forced an OAuth2 JWT token to be issued to graph.microsoft.com and intercepted by the proxy.
4. Token Scopes: `email`, `openid`, `profile`, `UserAuthenticationMethod.Read`, `UserAuthenticationMethod.ReadWrite`.
5. Post-Exploitation Actions: Endpoint `/beta/users` accessed for Directory Enumeration. No further data exposed.

---
### YOUR TASK:
Provide a step-by-step threat hunting report broken into four clear sections:

#### SECTION 1: KQL ADVANCED HUNTING QUERIES
Generate target Advanced Hunting (KQL) queries for Microsoft Sentinel / Microsoft Defender XDR to:
1. Audit log activity from User "CLIENT\A12345" or IP "3.11.236.40" targeting Microsoft Graph around `2026-08-25T16:07:00Z`.
2. Find token abuse by filtering for requests utilizing the explicit scopes (`UserAuthenticationMethod.ReadWrite`) across Microsoft Entra ID (Azure AD) Audit and Sign-in logs.
3. Search for directory enumeration via Microsoft Graph (e.g., calls to `/beta/users` or bulk read events).

#### SECTION 2: ATTACK VECTOR ANALYSIS & IMPACT ASSESSMENT
- Break down the gap in Microsoft Authenticator's Android Network Security Configuration that allowed user-installed root CAs to inspect traffic.
- Analyze the residual exposure risks of the captured scopes (`UserAuthenticationMethod.ReadWrite` and Graph `/beta/users`).

#### SECTION 3: IMMEDIATE CONTAINMENT STEPS
Detail the exact steps to revoke tokens, isolate the device, and revoke credentials in Microsoft Entra admin center and Intune.

#### SECTION 4: HARDENING & PREVENTION
Provide configuration rules for Microsoft Intune / Defender for Endpoint on Android to block user CA installation, enforce conditional access policies, and manage certificate trust stores.
