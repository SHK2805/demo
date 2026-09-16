The user attempted to move corporate data from the Intune-managed work profile into an unmanaged/personal app using Save-As, Open-In, or Share operations. The attempt failed due to policy restrictions.

Risk:  
Even though the attempt was blocked, this behaviour may indicate:

Intentional data exfiltration to personal cloud storage or external recipients.

Attempt to bypass App Protection Policies (APP) or Work Profile separation.

Potential misuse of corporate data on a BYOD device.

Testing of policy boundaries by a user (accidental or deliberate).

Because the work profile enforces strict DLP controls, no direct device logs exist.
Your evidence must come from Entra sign-in logs, M365 audit logs, and Intune app protection policy enforcement events.

----

No direct Entra telemetry exists for Save-As/Open-In actions on Android work profile. Only surrounding sign-in and policy enforcement logs will be available, which are not direct evidence of the activity

Intune does not provide direct logs of Save-As/Open-In attempts. Only policy configuration and enforcement status can be validated.

Splunk or Microsoft Defender does not contain any direct telemetry for Save-As/Open-In actions on Android work profile devices.

----
Summary: User attempted a Save-As/Open-In operation to move corporate data from the Intune-managed Android work profile to an unmanaged/personal app.
Result: Attempt failed. Intune App Protection Policies and Work Profile restrictions prevented data sharing and saving copies.
Telemetry: No direct logs exist for Save-As/Open-In attempts due to BYOD work profile isolation. Reviewed Entra sign-ins, M365 audit logs, and Intune policy status. No evidence of data exfiltration or file movement.
Conclusion: Activity blocked as designed. No data left the corporate boundary.
