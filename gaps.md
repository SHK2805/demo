
## ThreatMetrix Gaps

| **Gap** | **One‑liner** | **Category** | **Why we need this** |
| --- | --- | --- | --- |
| **AiTM / real‑time phishing proxy** | Phishing proxy captures post‑MFA tokens for immediate replay. | Network / OAuth | Detects token capture that bypasses credential‑only controls and MFA. |
| **PRT / browser cookie theft & replay** | PRTs or browser SSO cookies stolen from Edge/Chrome and replayed. | Token / Identity | Validates token‑binding and long‑lived SSO protections for M365. |
| **Zscaler tunnel / app‑bypass scenarios** | M365 app traffic falling back to direct internet or being excluded from tunnel. | Network / Proxy | Ensures Zscaler policies actually force inspection and don’t leak traffic. |
| **Split‑tunnel leakage** | Sensitive endpoints reachable outside inspection due to split‑tunnel rules. | Network | Confirms no sensitive M365 flows escape inspection on BYOD. |
| **TLS downgrade / trust‑store manipulation** | Forcing weaker TLS or adding rogue CA to trust store to intercept traffic. | Network / Device | Tests robustness of TLS, pinning, and CA trust controls. |
| **Certificate pinning bypass on rooted/jailbroken devices** | Pinning bypassed after root/jailbreak to intercept app tokens. | Token / Device | Validates app pinning and detection of compromised devices. |
| **Cross‑app token pivoting** | Token from one app (e.g., Outlook) used against another (Graph/OneDrive). | Token / OAuth | Tests token scoping and app isolation across M365 services. |
| **Token issuance during enrolment** | Tokens issued before device is fully compliant or enrolled. | Enrolment / Identity | Ensures enrolment flow doesn’t create early token exposure windows. |
| **Enrolment phishing / mis‑binding** | User tricked into enrolling wrong account or attacker MDM. | Enrolment / Social | Validates enrolment hardening and telemetry for mis‑binding attempts. |
| **MDM/profile tampering or rogue .mobileconfig** | Malicious profile installs or MDM changes pre/post enrolment. | Device / Enrolment | Detects rogue CA/MDM installs that enable interception or persistence. |
| **Work‑profile provisioning race / sideloading** | Apps injected into work container during provisioning window. | Android Work Profile | Tests transient policy gaps and unauthorized app injection risk. |
| **Clipboard boundary bypass** | Corporate clipboard data copied to unmanaged apps. | App‑layer / DLP | Validates Intune APP clipboard controls and enforcement. |
| **Share‑sheet / file‑provider abuse** | Managed → unmanaged transfer via share sheet or file providers. | App‑layer / DLP | Ensures save‑as/open‑in and file provider paths are blocked or audited. |
| **Android intent / content provider exfiltration** | Intents or content URIs used to leak corporate data to personal apps. | App‑layer / DLP | Tests Android‑specific inter‑app data leakage vectors. |
| **Third‑party keyboard / input exfiltration** | Keyboard app captures typed credentials or MFA codes. | Input / App‑layer | Confirms managed apps block untrusted keyboards or redact input. |
| **Notification listener / extension exfiltration** | Notification previews or MFA codes read and exfiltrated. | App‑layer / MFA | Validates notification redaction and extension restrictions. |
| **Accessibility service abuse / persistence** | Accessibility APIs used to read screens or capture MFA. | Device / Persistence | Tests detection of persistent accessibility‑based implants. |
| **Native screen recording / remote control** | Screen capture via OS recorder or remote access apps. | Screen / Privacy | Ensures managed apps prevent screen capture and remote viewing. |
| **Commercial stalkerware / malware persistence** | Off‑the‑shelf stalkerware installed and persisting. | Device / Malware | Validates EDR/Mobile Threat Defense detection and containment. |
| **Zero‑click / vendor implant simulation** | High‑end exploit implant simulation for detection validation. | Device / Advanced Threat | Tests telemetry for sophisticated, low‑visibility compromises. |
| **Repair‑channel persistent implant** | Persistence via repair/service channel or vendor tools. | Device / Persistence | Ensures detection of non‑standard persistence mechanisms. |
| **OAuth consent abuse & redirect manipulation** | Malicious app consent or redirect URI manipulation on mobile. | OAuth / Identity | Tests mobile consent flows and redirect handling for tenant traversal. |
| **PRT / refresh token lifecycle anomalies** | Unusual refresh token usage patterns or long‑lived token reuse. | Token / Monitoring | Enables hunts for token misuse and anomalous refresh activity. |


## Test Case Gaps

| **Gap** | **One‑liner** | **Category** | **Why we need this** |
| --- | --- | --- | --- |
| **AiTM / real‑time phishing proxy** | Phishing proxy captures post‑MFA tokens (session/refresh) for immediate replay. | Network / OAuth | Tests real‑time token capture that bypasses credential‑only controls and defeats MFA; high impact for SSO/PRT. |
| **PRT / browser cookie theft & replay** | PRTs or browser SSO cookies stolen from Edge/Chrome and replayed against M365. | Token / Identity | Validates token‑binding and SSO protections for browser flows (Edge on Android/iOS is in scope). |
| **OAuth consent abuse & redirect manipulation** | Malicious consent or redirect URI manipulation in mobile OAuth flows. | OAuth / Identity | Mobile consent flows differ from desktop; tests tenant traversal and malicious app consent vectors. |
| **Cross‑app token pivoting** | Token from one M365 app used against another service (e.g., Outlook → Graph). | Token / OAuth | Verifies token scoping and app isolation across M365 services; high lateral‑movement risk. |
| **Token issuance during enrolment** | Tokens issued before device is fully enrolled/compliant (Account‑Driven enrolment). | Enrolment / Identity | Detects early‑window token exposure during provisioning; critical for BYOD account‑driven flows. |
| **Zscaler client connector / app‑bypass scenarios** | M365 app traffic falling back to direct internet or excluded from Zscaler inspection. | Network / Proxy | Ensures Zscaler policies actually enforce inspection; prevents uninspected token leakage. |
| **Split‑tunnel leakage validation** | Sensitive M365 endpoints reachable outside inspection due to split‑tunnel rules. | Network | Confirms no sensitive flows escape inspection on BYOD where full tunnelling is not enforced. |
| **Work‑profile provisioning race / sideloading** | Apps injected into work container during provisioning window or via sideload. | Android Work Profile | Tests transient policy gaps and unauthorized app injection into the work profile. |
| **Clipboard boundary bypass** | Corporate clipboard data copied and read by unmanaged apps. | App‑layer / DLP | Validates Intune APP clipboard controls and prevents silent data leakage. |
| **Share‑sheet / file‑provider abuse** | Managed → unmanaged transfer via iOS share sheet or third‑party file providers. | App‑layer / DLP | Ensures save‑as/open‑in and file provider paths are blocked or audited on BYOD. |
| **Android intent / content provider exfiltration** | Intents or content URIs used to leak corporate data to personal apps. | App‑layer / DLP | Android‑specific inter‑app vectors; must be tested for work profile isolation. |
| **PRT / refresh token lifecycle anomalies** | Unusual refresh token usage or long‑lived token reuse patterns. | Token / Monitoring | Enables hunts for token misuse and anomalous refresh activity not covered by functional tests. |
| **Zero‑click / vendor implant simulation** | Simulated low‑visibility exploit implant to validate telemetry. | Device / Advanced Threat | Tests detection for sophisticated compromises that bypass user interaction. |
| **Repair‑channel persistent implant** | Persistence via repair/service channel or vendor tools. | Device / Persistence | Validates detection of non‑standard persistence mechanisms not covered by standard malware tests. |
| **MDM/profile tampering / malicious .mobileconfig** | Rogue profile or CA installs pre/post enrolment enabling interception/persistence. | Device / Enrolment | Detects rogue MDM/CA installs and trust‑store changes that enable network interception. |

## Additional High Value ThreatMetrix to consider (may not be in scope)

| **Gap** | **One‑liner** | **Category** | **Why we need this** |
| --- | --- | --- | --- |
| **AiTM / real‑time phishing proxy** | Phishing proxy captures post‑MFA session tokens in real time for immediate replay. | **Network / OAuth** | **Bypasses MFA** and yields immediate account access; high speed, low noise compromise. |
| **OAuth redirect / consent abuse** | Malicious apps or crafted OAuth URLs abuse redirect behavior to deliver phishing or malware. | **OAuth / Identity** | Tests mobile consent flows and prevents rogue app consent or silent redirects. |
| **PRT / browser cookie theft & replay** | Primary Refresh Tokens or SSO cookies stolen from mobile browsers (Edge/Chrome) and replayed. | **Token / Identity** | Validates token‑binding and long‑lived SSO protections for mobile browsers. |
| **Zero‑click system exploits** | Remote, no‑interaction exploits (zero‑click) that achieve silent code execution on device. | **Device / Advanced Threat** | Enables stealthy full device compromise; detection must cover kernel/system anomalies. |
| **Zscaler client connector / tunnel bypass** | App or PAC misconfiguration allows M365 traffic to bypass Zscaler inspection. | **Network / Proxy** | Ensures network controls actually cover M365 apps; prevents uninspected token leakage. |
| **Work‑profile provisioning race / sideloading** | Transient provisioning window allows sideloading into Android work profile. | **Android Work Profile** | Tests for unauthorized app injection and cross‑profile data leakage. |
| **Repair‑channel / vendor persistence** | Persistence via repair/service channels or vendor tools that survive wipes. | **Device / Persistence** | Detects non‑standard persistence mechanisms that evade normal EDR/MTD. |
| **Clipboard / share‑sheet / file‑provider abuse** | Managed → unmanaged data transfer via clipboard, share sheet, or file providers. | **App‑layer / DLP** | Validates Intune APP DLP controls and prevents silent data exfiltration. |
| **PRT / refresh token lifecycle anomalies** | Unusual refresh token usage patterns and long‑lived token reuse. | **Token / Monitoring** | Enables hunting for token misuse and anomalous refresh activity. |
| **Accessibility / notification listener abuse** | Accessibility APIs or notification listeners used to capture MFA or screen content. | **Input / App‑layer** | Tests detection of persistent, high‑privilege exfiltration channels. |


## Logs to consider

### SIEM Log and Alert Priorities

- **Azure AD Sign‑in Logs** — ingest sign‑in events, clientApp, requestId, tokenId, ipAddress, deviceDetail; alert on token reuse, simultaneous sessions, impossible travel, and failed Conditional Access evaluations.  
- **Azure AD Audit and OAuth Consent Logs** — ingest consent grants, app registrations, redirect URIs, admin consent events; alert on new app consent, unusual redirect changes, and high‑privilege consent by non‑admins.  
- **Azure AD Token Issuance and Refresh Events** — ingest refresh token issuance and refresh activity, token lifetimes, and token binding metadata; alert on refresh token reuse, long‑lived refresh patterns, and token issuance during enrolment.  
- **Intune Enrollment and Device Compliance Logs** — ingest enrolment attempts, compliance state changes, profile installs, and deviceId; alert on token issuance before compliance, unexpected profile installs, and rapid compliance state flips.  
- **Intune App Protection and App Access Logs** — ingest app protection policy hits, clipboard events, save as open in events, and managed app sign‑ins; alert on blocked DLP actions, share sheet bypass attempts, and personal account sign‑ins in managed apps.  
- **Zscaler Client Connector and ZPA Session Logs** — ingest connector status, sessionID, PAC/app bypass events, and app routing decisions; alert on missing ZCC sessions for M365 apps, app bypass events, and PAC mismatches.  
- **Network Metadata DNS SNI and Proxy Logs** — ingest DNS queries, SNI, HTTP host headers, and proxy session metadata; alert on suspicious SNI patterns, AiTM proxy indicators, and unexpected M365 endpoint resolution.  
- **Mobile Defender for Endpoint and MTD Alerts** — ingest deviceRiskScore, jailbreak root detections, malicious app installs, and MTD verdicts; alert on root jailbreak, stalkerware detection, and high device risk scores.  
- **Tanium Endpoint Actions and Inventory Logs** — ingest installed apps, action history, device configuration, and remediation actions; alert on unexpected app installs, repair channel tool usage, and persistent service creation.  
- **App Telemetry from Managed Apps** — ingest appId, requestId, tokenId, API endpoints called, and error codes from Outlook Teams OneDrive; alert on cross‑app token usage, unusual Graph API calls, and failed token binding checks.  
- **Device Trust and Certificate Events** — ingest CA installs, trust store changes, mobileconfig installs, and profile changes; alert on new CA installs, malicious mobileconfig installs, and profile tampering.  
- **Network Access and Wi‑Fi Events** — ingest Wi‑Fi SSID joins, captive portal interactions, and DHCP lease metadata; alert on connections to known rogue SSIDs, captive portal credential submissions, and sudden network changes.  
- **Notification and Accessibility Events** — ingest notification listener registrations, accessibility service enables, and related app grants; alert on new notification listeners, accessibility API grants, and repeated MFA code exposures.  
- **Screen Capture and Remote Access Events** — ingest screen recording starts, remote control sessions, and screen share events; alert on screen capture attempts in managed apps and remote access tool usage on mobile devices.  
- **Correlation and Enrichment Fields** — ensure userPrincipalName, deviceId, deviceOS, appId, requestId, tokenId, and ipAddress are normalized across sources for correlation; alert on correlated anomalies spanning identity device and network signals.
