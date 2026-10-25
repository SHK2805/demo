### Explanation: Why Pre-Installed Apps Are Not Deleted During Enrolment

Apple’s iOS operating system architecture embeds core pre-installed system applications (such as Safari, Messages, Settings, and default utilities) within the **Sealed System Volume (SSV)**, which is cryptographically signed and read-only. MDM enrolment—especially under a BYOD (Bring Your Own Device) or User Enrolment model—cannot modify, uninstall, or delete built-in system apps. Furthermore, BYOD privacy boundaries intentionally protect existing personal applications and pre-installed software; MDM policies only govern corporate work profiles and managed applications, leaving pre-installed or personal apps completely intact.

---

## 1. Hunting Hypothesis & Risk

* **Hypothesis:** A threat actor or compromised insider with valid Entra ID credentials and completed MFA is attempting to use developer tools (such as Xcode and iOS simulators) or virtualized/emulated iOS devices to bypass device compliance controls, fraudulently register an unauthorized device, and provision MFA passkeys for persistent access.
* **Risks:**
* Bypassing hardware-backed device compliance and conditional access policies using emulated hardware parameters.
* Unauthorized generation or theft of phishing-resistant credentials (FIDO2 / passkeys) tied to an unmanaged or attacker-controlled virtual endpoint.
* Expanding attacker foothold within corporate cloud resources without triggering traditional device-health telemetry due to the absence of Mobile Threat Defense (MTD) tools.



---

## 2. Where to Look (Console Navigational Guide)

* **Microsoft Entra ID Portal:**
* **Path:** `Identity` > `Sign-in logs` (to inspect authentication attempts, risk detections, device ID, IP address `3.11.236.40`, and user agent strings matching the timestamp `22/10/2026 10:52 UTC`).
* **Path:** `Identity` > `Users` > Select user `CLIENT\A12345` > `Authentication methods` (to audit registered passkeys, FIDO2 security keys, or MFA device registrations).


* **Microsoft Intune Admin Center:**
* **Path:** `Devices` > `Enrollment` > `Device enrollment restrictions` (to review platform restrictions blocking personal or unrecognized iOS client types).
* **Path:** `Devices` > `Audit logs` (to review failed or blocked iOS device registration/enrolment events for the device name `iPad`).



---

## 3. Where to Look for Profile (Intune Profile Restrictions)

* **Intune Device Platform Restrictions & Compliance Policies:**
* **Path:** `Intune Admin Center` > `Devices` > `Enrollment` > `Device platform restrictions` > Select `iOS/iPadOS restrictions`. Check configuration settings under **Platform settings** for `Personally owned devices` (set to `Block` or `Allow`) and minimum/maximum iOS version constraints.
* **Path:** `Intune Admin Center` > `Devices` > `iOS/iPadOS` > `Compliance policies` > Select the active policy to verify hardware integrity checks (blocking jailbroken/rooted or emulated devices).


* *Jira Note Requirement:* Since Intune audit logs and Entra sign-in logs record the authentication and enrollment failure, but do *not* capture local Xcode simulator logs or IDE-level app installation errors (as device-level logs are not sent to the SIEM and no MTD is installed), this absence of direct device-side installation telemetry must be explicitly documented as a comment in the Jira ticket:
> **Jira Comment:** *"Corporate SIEM, Defender, Entra, and Intune logs confirm the authentication and enrollment failure, but do not capture direct local device logs or Xcode installation telemetry due to lack of MTD and absence of device log forwarding in a BYOD context."*



---

## 4. Kibana / Elasticsearch Hunting Searches

*(Note: In environments utilizing Elasticsearch/Kibana alongside cloud event shippers, use the following direct log queries to target authentication and enrollment failures.)*

* **Query 1 (Entra Sign-ins from Suspicious IP / User):**
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "userPrincipalName": "A12345" } },
        { "match": { "clientAppUsed": "Browser" } }
      ],
      "filter": [
        { "range": { "@timestamp": { "gte": "2026-10-22T10:00:00Z", "lte": "2026-10-22T11:30:00Z" } } }
      ]
    }
  }
}

```


* **Query 2 (Failed Device Registration / Enrolment Anomalies):**
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.category": "iam" } },
        { "match": { "event.outcome": "failure" } }
      ],
      "filter": [
        { "term": { "source.ip": "3.11.236.40" } }
      ]
    }
  }
}

```



---

## 5. Step-by-Step Investigation Checklist

1. **Verify Authentication & MFA Context:** Open Microsoft Entra ID Sign-in logs for user `CLIENT\A12345` around `22/10/2026 10:52 UTC`. Confirm whether the IP `3.11.236.40` corresponds to a known corporate VPN, residential network, or cloud hosting provider.
2. **Inspect Entra Authentication Methods:** Check if any new FIDO2 security keys, passkeys, or Microsoft Authenticator methods were successfully registered or modified during or immediately after this timestamp.
3. **Check Intune Enrolment Logs:** Navigate to Intune Audit Logs to confirm the blocked enrollment attempt for device name `iPad` under user `CLIENT\A12345`.
4. **Validate Local Telemetry Gap & Document Jira Comment:** Verify that SIEM/Defender logs *do not* contain direct evidence of the local Xcode installation attempt or simulator runtime errors. Document this limitation explicitly as a comment in Jira.
5. **Review Conditional Access Policies:** Ensure that policies enforcing compliant devices or approved client apps successfully blocked the unauthorised access attempt.
6. **Remediate & Notify:** If credential compromise is suspected, force a password reset, revoke existing refresh tokens, and require re-authentication with strong MFA.

---

## 6. Splunk Hunting Queries

* **Query 1: Correlating Entra Sign-In and User Activity for User A12345 from IP 3.11.236.40**
```splunk
index=entra_logs userPrincipalName="*A12345*" src_ip="3.11.236.40" 
| eval timestamp=strftime(_time, "%Y-%m-%d %H:%M:%S") 
| table timestamp, userPrincipalName, src_ip, appDisplayName, status.errorCode, conditionalAccessStatus

```


* **Query 2: Identifying Failed Device Registrations or MDM Enrolment Failures**
```splunk
index=intune_audit_logs operationName="Enrol device" result="Failure" userPrincipalName="*A12345*"
| eval timestamp=strftime(_time, "%Y-%m-%d %H:%M:%S")
| table timestamp, userPrincipalName, deviceName, result, failureReason

```
