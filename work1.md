HUNTING HYPOTHESIS & RISK
Hypothesis:  
The user attempted to bypass Android Work Profile restrictions by installing a third‑party keyboard (net.milosz.keyboard) into the work profile using ADB sideloading and pm install-existing. The goal was to test whether personal‑profile apps could be forced into the work profile.

Risk:  
If successful, this could allow:

Keystroke interception inside corporate apps (Teams, Outlook, Edge).

Data leakage via malicious keyboard apps.

Cross‑profile contamination, violating Android Enterprise isolation.

Policy circumvention, indicating a potential insider threat or misconfiguration.

Outcome:  
All attempts failed, and the work profile correctly enforced restrictions. Only approved keyboards were available inside Teams.

---

Entra ID (Sign‑in & Audit Logs)
Note: Entra does NOT log keyboard installation attempts or ADB/pm commands. Only app launches, sign‑ins, and device compliance events may appear.

Intune (Device Compliance & Work Profile App Inventory)
Note: Intune does not log failed sideload attempts or cross‑profile installation attempts. It only shows apps successfully installed in the work profile.

---
The attempted installation of the third‑party keyboard (net.milosz.keyboard) into the Android Work Profile failed due to enforced Intune and Android Enterprise restrictions.

Official Microsoft documentation confirms that Work Profiles are isolated containers, and Intune can only manage the work partition. BYOD devices do not send OS‑level logs (such as ADB, sideload, or package manager events) to Intune, Entra, Splunk, or Defender, so no telemetry exists for the failed installation attempt.

The device has an Intune Android Enterprise Device Restrictions profile applied, with Approved Keyboards: Require, and only Gboard and SwiftKey selected. This policy prevents unapproved keyboards from being installed or used inside the Work Profile.

The ADB error “shell does not have permission to access user 10” is consistent with Android Enterprise sandboxing and confirms that the Work Profile blocked access.

Policy is functioning as expected, and there is no evidence of compromise or policy bypass.
