## Gaps

Token & Credential Abuse

Refresh Token Replay — attacker reuses a stolen refresh token to mint new access tokens without MFA.

Mobile OS Token Exfiltration — attacker steals authentication tokens from a compromised mobile OS.

Enrolment Abuse

Unmanaged Browser Enrolment — attacker enrols a passkey/authenticator through a non‑MDM browser to bypass device trust.

Cloned OS Image Enrolment — attacker uses a cloned device image to reuse previously enrolled credentials.

Outdated Authenticator App Enrolment — attacker installs an old Authenticator version to bypass modern attestation checks.

Shared Apple/Google ID Sync — attacker receives synced passkeys by logging into the same Apple/Google account.

Protocol & Device Tampering

WebAuthn Client Data JSON Tampering — attacker modifies WebAuthn payload fields before submission.

CTAP2 Message Tampering — attacker intercepts or alters CTAP2 messages during authentication.

OS Biometric Framework Tampering — attacker bypasses biometric checks using OS‑level manipulation.

Authenticator App Storage Tampering — attacker extracts or replaces private keys stored in secure enclave/keystore.

Device Integrity Signal Tampering — attacker spoofs SafetyNet/DeviceCheck to hide root/jailbreak status.

Conditional Access Weaknesses

CA Policy Race Conditions — attacker uses tokens issued before CA changes to bypass new restrictions.

Passkey vs FIDO2 Misalignment — attacker selects the weaker method when CA policies differ.

Legacy Protocol Bypass — attacker authenticates via IMAP/POP/SMTP to avoid MFA.

Offline Authentication Fallback — attacker uses cached credentials during offline mode to bypass CA.

Supply‑Chain & MDM

Compromised MDM Vendor — attacker pushes malicious compliance profiles to falsely mark devices as compliant.

User‑Driven Weakening

Developer Mode Enabled — attacker uses developer mode to weaken OS protections and extract sensitive data.

Integrity Checks Disabled — attacker disables device integrity checks to hide compromise.

Recovery & Fallback Abuse

Fallback to Weaker MFA — attacker triggers fallback flows (SMS/email) to bypass passkeys.

Break‑Glass Accounts Unprotected — attacker targets emergency accounts lacking MFA.

Recovery Channel Hijacking — attacker takes over recovery email/phone to reset or add authenticators.

Infrastructure Dependencies

Push Notification Dependency — attacker exploits push outages to force weaker fallback authentication.

MDM Compliance Latency — attacker authenticates during the delay before non‑compliance is enforced.


## Logging & SIEM Requirements

Passkey registration logging — record every passkey or authenticator registration event.

Authenticator app version logging — record version changes and downgrades of Microsoft Authenticator.

Device integrity logging — record root/jailbreak and attestation failures.

Attestation result logging — record AAGUID, attestation type, and attestation failures.

Token replay detection — record refresh token reuse across devices or locations.

Refresh token redemption logging — record all refresh‑to‑access token exchanges.

WebAuthn anomaly logging — record RP ID mismatches, challenge mismatches, and verification flag anomalies.

CTAP2 transport logging — record CTAP2 failures, anomalies, and unexpected command sequences.

Fallback MFA logging — record all fallback authentication method usage.

Break‑glass account logging — record all break‑glass account logins and token issuance events.

Recovery channel change logging — record email/phone number changes and MFA reset attempts.

MDM compliance logging — record compliance state changes and timestamps.

Push notification failure logging — record push delivery failures and fallback triggers.

Legacy protocol logging — record IMAP/POP/SMTP authentication attempts.

Offline authentication logging — record cached‑credential authentication events.

Cross‑device passkey usage logging — record passkeys used on devices other than the enrolment device.

Graph API credential operations logging — record add/remove/modify operations on credentials via Graph API.
