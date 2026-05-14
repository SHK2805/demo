
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
