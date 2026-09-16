After reviewing Microsoft’s official documentation for Intune App Protection Policies (APP) and Android Work Profile behaviour, the tester’s assessment is correct: there is no execution path for exfiltration via a personal account inside a managed Microsoft 365 application.

Microsoft states that when APP settings such as “Require corporate account” and “Block multi‑identity” are enabled, managed apps operate in single‑identity mode. In this mode, the application does not initiate any authentication flow for personal accounts. The app blocks the action at the UI layer before any token request, sign‑in attempt, or session creation occurs.

Android Work Profile documentation further confirms that work‑profile apps cannot authenticate personal identities, and cross‑profile data movement is prevented by OS‑level sandboxing. Because the platform blocks the action before any authentication or data‑handling logic is executed, no operational event is generated.

Why No Logs Are Seen
No direct logs:  
Entra, Intune, Defender, and Splunk only record events when an authentication attempt, token request, or network session is actually initiated. In this case, the app never reaches those stages. The personal‑account sign‑in is blocked locally by the Intune APP enforcement layer, so no sign‑in, token, or network event exists to log.

No indirect logs:  
Conditional Access, audit logs, and identity logs only trigger when an identity tries to authenticate. Because the personal identity is never passed to Entra ID, no CA evaluation, no audit entry, and no failed sign‑in event is produced.
Splunk and Defender do not receive device‑level logs and therefore cannot show app‑level policy enforcement or identity‑switch attempts.
