The user attempted to weaken TLS inspection or redirect traffic by installing a malicious CA certificate or global proxy profile before enrolling the device into Intune. We must verify whether the enrollment process detects or mitigates this pre‑existing configuration.

Risks:

TLS interception: A malicious CA allows full HTTPS MITM against corporate apps.

Traffic redirection: A global proxy profile could route corporate traffic to an attacker-controlled server.

Bypassing App Protection Policies: If corporate apps trust the malicious CA, sensitive data could be intercepted.

False sense of security: Intune compliance checks may pass even though the device is compromised, because pre‑existing profiles are invisible to MDM.
