## HUNTING HYPOTHESIS & RISK

* **Hunting Hypothesis:** Users can enrol and utilize multiple biometric profiles (such as alternate fingerprints) on a corporate BYOD Android device, allowing secondary or unauthorized individuals to successfully authenticate against device-bound FIDO2/MFA passkeys tied to the primary user account.
* **Associated Risks:**
* Compromises non-repudiation and identity accountability for corporate resources protected by phishing-resistant passkeys.
* Permits physical or proxy sharing of corporate access tokens if an unauthorized individual registers their fingerprint on an active work-profile-enrolled device.
* Lack of local device telemetry (no Mobile Threat Defense, no MDE for Endpoint, and no local device event forwarding to SIEM) leaves enterprise security teams completely blind to local biometric additions or hardware-level enrollment changes.



---

## WHERE TO LOOK (CONSOLE NAVIGATIONAL GUIDE)

* **Microsoft Intune Admin Center:**
* Navigate to **Devices** > **Configuration profiles** to review compliance and device configuration policies enforcing biometric restrictions or device lock requirements.
* Navigate to **Devices** > **By platform** > **Android** > **Compliance policies** to verify whether baseline settings require lock screen complexity or restrict secondary biometric definitions.


* **Microsoft Entra Admin Center:**
* Navigate to **Identity** > **Monitoring & health** > **Sign-in logs** to inspect authentication events, Multi-Factor Authentication methods used, and device context attributes around `26/10/2026 10:28 UTC`.


* **Splunk / SIEM Enterprise Logs:**
* Query identity and authentication streams tracking token issuance and interactive login claims for user `CLIENT\A12345`. *(Note: Local device settings changes—such as registering a new fingerprint in Android OS settings—do not generate network logs or cloud audit events and are invisible to Splunk or Defender. Record this visibility gap explicitly as a comment in Jira).*



---

## WHERE TO LOOK FOR PROFILE

* **Microsoft Intune Admin Center Console Path:**
1. Open the **Intune admin center** (`intune.microsoft.com`).
2. Select **Devices** from the left-hand menu.
3. Under *Manage devices*, click **Configuration**.
4. Select the active **Device Restriction** or **Compliance Policy** assigned to Android Enterprise work profiles.
5. Click **Settings** and expand the **Device Experience** or **Password / Passcode** blocks.
6. Inspect parameters governing screen unlock security and biometric authentication constraints. *(Note: Standard Android Enterprise work profile controls manage corporate container security, but natively governing local OS-level biometric enrollment limits on a personal BYOD device requires custom OMA-URI policies or manufacturer-specific Knox/OEM configurations, as stock Android permits multiple biometric profiles by design).*



---

## KIBANA / ELASTICSEARCH HUNTING SEARCHES

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "user.name": "A12345"
          }
        },
        {
          "match": {
            "event.category": "authentication"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "2026-10-26T10:00:00Z",
              "lte": "2026-10-26T11:00:00Z"
            }
          }
        }
      ]
    }
  }
}

```

---

## STEP-BY-STEP INVESTIGATION CHECKLIST

1. **Inspect Authentication and MFA Method Context:** Target: Entra Sign-In Logs.
Filter Entra ID sign-in logs for user `CLIENT\A12345` around `26/10/2026 10:28 UTC` to identify successful token grants and verify whether passkey/FIDO2 authentication was leveraged.
*Verification:* Confirm authentication success status and check the authentication method details logged during the session.


2. **Audit Device Compliance and Restriction Policies:** Target: Intune Device Configuration.
Review active Intune device configuration profiles to check if restrictions prevent biometric sharing or if local OS modifications are unmanaged under the BYOD framework.
*Verification:* Document whether any policy specifically targets biometric limits or if management is restricted to work-profile container boundaries.


3. **Correlate Network and Session Activity:** Target: Splunk Identity Logs.
Query Splunk for network events originating from IP `82.34.244.83` during the target timeframe to ensure no anomalous external IPs or impossible travel indicators accompanied the authentication.
*Verification:* Confirm that sign-in IP matches expected baseline or corporate network parameters.


4. **Record Telemetry and Visibility Gaps in Jira:** Target: Jira Incident Ticket.
Document in the Jira ticket that local biometric registration (adding multiple fingerprints inside Android OS settings) generates zero logs in Entra, Intune, Splunk, or Defender due to BYOD privacy constraints.
*Verification:* Verify that the Jira comment explicitly states: *"Local OS biometric configuration changes are not captured by cloud or SIEM telemetry because Android does not stream local fingerprint enrollment events to management consoles."*


---

## SPLUNK HUNTING QUERIES

```splunk
index=entra_signins user="A12345" OR ip="82.34.244.83" 
| eval timestamp=strftime(_time, "%d/%m/%Y %H:%M UTC") 
| table timestamp, user, ip, appDisplayName, conditionalAccessStatus, status, authenticationMethod 
| sort - _time

```

---

### Technical Note on Why the Device Did Not Delete Pre-Installed Data / Configurations During Enrollment

When a BYOD device (such as the Pixel 8a) is enrolled into Microsoft Intune via a **Personally-owned work profile** deployment, existing device data, user settings, and local configurations are **intentionally preserved**:

1. **Work Profile Architecture vs. Full Wipe:** Unlike corporate-owned fully managed devices (where a factory reset and complete wipe occur during provisioning), BYOD work profile enrolment creates an isolated, encrypted logical container for corporate apps and data. Personal settings, existing operating system configurations, and local hardware features—including pre-registered user fingerprints or lock screen credentials—remain untouched to respect user privacy and data ownership.
2. **Design Limits of Local Biometrics:** Stock Android and mobile operating systems treat biometric hardware templates (fingerprints or face unlock models) at the OS/hardware abstraction layer (TEE / Secure Enclave). Enrolling a work profile manages enterprise policy within the work container but does not wipe or restrict personal OS-level biometric settings unless specialized, high-privilege device restriction policies or OEM-specific management frameworks are enforced.


> **Investigation Closing & Telemetry Statement:**
> Pursuant to the technical architecture of Android Enterprise Personally-Owned Work Profile deployments and corporate Bring Your Own Device (BYOD) governance frameworks, zero telemetry or audit logs will be generated or captured across cloud management consoles (Microsoft Entra ID, Intune), SIEM platforms (Splunk), or endpoint security portals (Microsoft Defender XDR) regarding local OS-level actions such as biometric template modifications.
> **Official Research & Architectural Constraints:**
> 1. **OS-Level Isolation & Privacy Boundaries:** According to Google's Android Enterprise architecture and [Microsoft Intune Documentation](https://learn.microsoft.com/en-us/intune/device-enrollment/android/enterprise-work-profile), the work profile creates a strictly isolated cryptographic and logical container on personal hardware. Local hardware security features—including Trusted Execution Environment (TEE) biometric enrollments (fingerprints or face models)—reside entirely within the personal OS layer and are bound by strict operating system privacy frameworks that prevent management controllers from inspecting or logging local credential configurations.
> 2. **Absence of Endpoint Sensors:** As established in [Microsoft Defender for Endpoint on Android Privacy Guidelines](https://learn.microsoft.com/en-us/defender-endpoint/android-privacy), telemetry collection requires an active MDE or Mobile Threat Defense sensor deployed on the target asset. In a BYOD model lacking MDE and local log forwarding, advanced hunting schemas (`DeviceEvents`, `DeviceInfo`) and SIEM ingestion pipelines remain completely unpopulated. Consequently, local setting adjustments leave no network footprints, API audit events, or security telemetry trails for downstream correlation.
> 
>
