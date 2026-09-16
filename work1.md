The activity under review occurred before the device was enrolled on Intune MDM. At this stage, the iOS device had no management profile, no MDM channel, and no telemetry connection to Intune or any Microsoft 365 security platform. As a result, no device‑level logs or configuration events were generated or collected for the attempted installation of the CA certificate or configuration profile.

Log Availability:

No direct device logs exist for this activity because Intune only begins collecting device telemetry after the MDM enrollment profile is installed.

The malicious CA certificate installation took place outside Intune’s visibility and control, and iOS does not expose pre‑enrollment configuration changes to MDM.

Any logs available in Entra ID (sign‑ins), Conditional Access, or Intune (enrollment metadata) relate to the user identity and enrollment process, not the device’s configuration state at the time of the activity. These therefore represent indirect evidence only, and do not provide visibility into the profile installation itself.

Platform Behaviour:  
Apple’s MDM protocol prevents Intune from detecting, viewing, or removing configuration profiles or certificates that were installed prior to enrollment. This is expected behaviour for BYOD iOS devices.

Conclusion:  
Because the device was not enrolled at the time of the attempted profile installation, there are no direct device logs available for this event. Only identity‑based and enrollment‑related logs can be referenced, and these do not provide device‑level visibility into the malicious CA installation. The absence of direct logs is expected and consistent with Apple’s BYOD and MDM security model.
