Based on review of Microsoft’s documented behaviour for Intune App Protection Policies (APP) and Android Work Profile restrictions, the tester’s assessment is correct: there is no execution path for a personal‑account exfiltration attempt inside a managed Microsoft 365 application.

Microsoft officially states that when an app is managed under APP with “Require corporate account” or “Block multi‑identity” enabled, the application will not allow sign‑in with personal identities. In this configuration, the app enforces single‑identity mode, meaning the user cannot add or switch to a personal account within the same app session. Any attempt to add a second identity is blocked before the app can initiate authentication or access any data.

Additionally, Microsoft’s guidance for Android Work Profile confirms that personal accounts cannot be used inside work‑profile managed apps, and cross‑profile data movement is technically prevented by OS‑level sandboxing. This means the user cannot navigate between work and personal identities inside the same app, nor transfer data between profiles.

Outcome:  
Because both Intune APP and Android Work Profile restrictions prevent personal‑account sign‑in and block multi‑identity behaviour at the policy level, the attempted exfiltration cannot progress beyond the initial sign‑in attempt. No authentication occurs, no secondary identity is created, and no data movement path exists.
