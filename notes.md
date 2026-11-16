
## HUNTING HYPOTHESIS & RISK

* **Hunting Hypothesis:** Users can successfully enrol unapproved or non-compliant mobile operating systems (such as Android 14 on a Google Pixel 8a) into the corporate Microsoft Intune BYOD work profile framework, potentially bypassing baseline passkey/MFA device-integrity guardrails if enrollment restrictions are misconfigured or unassigned.
* **Associated Risks:**
* Enrolment of unapproved OS versions can expose corporate infrastructure to platform-specific vulnerabilities or unpatched exploit chains.
* Weakened or non-compliant device security postures undermine Microsoft Entra ID Phishing-Resistant MFA Passkey trust chains, permitting unauthorized token issuance on compromised hardware.
* Lack of endpoint telemetry (no Mobile Threat Defense, no Defender for Mobile Endpoint, and no local device logs forwarded to SIEM) limits visibility into whether the underlying OS environment is rooted, bootloader-unlocked, or running customized ROMs.



---

## WHERE TO LOOK (CONSOLE NAVIGATIONAL GUIDE)

* **Microsoft Intune Admin Center:**
* Navigate to **Devices** > **Device onboarding** > **Enrollment** > **Device platform restrictions** to inspect OS version boundary configurations.
* Navigate to **Devices** > **By platform** > **Android** > **Android enrollment** > **Personally-owned work profile** to review active BYOD constraints.


* **Microsoft Entra Admin Center:**
* Navigate to **Identity** > **Monitoring & health** > **Sign-in logs** to correlate user session authentication and device registration metadata.
* Navigate to **Identity** > **Devices** > **All devices** to verify the object record corresponding to `Pixel_8A` (`AndroidForWork_12`).


* **Splunk / SIEM Enterprise Logs:**
* Query cloud-native audit channels tracking identity authentication pipelines, API calls, and directory changes originating from `CLIENT\A12345`. *(Note: Direct local device installation attempts, debug traces, or low-level OS exploit execution logs are absent from SIEM ingest due to BYOD telemetry limitations; record this visibility gap explicitly as a comment in Jira).*



---

## WHERE TO LOOK FOR PROFILE

* **Microsoft Intune Admin Center Console Path:**
1. Open the **Intune admin center** (`intune.microsoft.com`).
2. Select **Devices** from the left-hand menu.
3. Under *Device onboarding*, click **Enrollment**.
4. Select the **Device platform restrictions** tab.
5. Locate and open the applicable priority restriction policy assigned to standard users (e.g., *Default* or custom *BYOD Android Restrictions*).
6. Click **Properties** next to *Platform settings*.
7. Inspect the **Android Enterprise (work profile)** row parameters, specifically verifying the configured **Minimum OS version** and **Maximum OS version** attributes. *(Note: If the minimum version threshold is set too low—such as allowing Android 14 when policy intended restriction—this configuration gap explains why the Pixel 8a successfully enrolled).*



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
            "event.category": "iam"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "2026-10-19T15:00:00Z",
              "lte": "2026-10-19T15:40:00Z"
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

1. **Verify Entra ID Sign-In & Device Registration Context:** Target: Entra Sign-In Logs.
Filter sign-in logs for user `CLIENT\A12345` around `19/10/2026 15:20 UTC` originating from IP `82.34.244.83`. Check whether the device registered successfully and note the device trust state.
*Verification:* Confirm the appearance of an interactive sign-in event mapping to `Pixel_8A` with a success status code.


2. **Audit Intune Enrollment Platform Restrictions:** Target: Intune Device Platform Restrictions.
Inspect the active Android Enterprise device platform restriction profile in the Intune portal to check if OS version boundaries permitted Android 14.
*Verification:* Document the exact minimum and maximum version parameters configured in the active policy assignment.


3. **Correlate Network Activity via Splunk:** Target: Splunk Enterprise Logs.
Search corporate proxy and perimeter logs for connections from IP `82.34.244.83` to validate session characteristics during the enrollment window.
*Verification:* Cross-reference HTTP headers and user-agent strings against known Microsoft Company Portal application signatures.


4. **Record Telemetry and Visibility Gaps in Jira:** Target: Jira Incident Ticket.
Review findings against the environment constraint that local device logs and Mobile Threat Defense telemetry are absent. Note in the Jira ticket that low-level OS installation mechanics and exploit artifacts are invisible due to BYOD privacy boundaries.
*Verification:* Verify that the Jira comment explicitly states: *"Local device installation logs, debug outputs, and kernel telemetry are unavailable due to BYOD architecture limitations."*


---

## SPLUNK HUNTING QUERIES

```splunk
index=entra_audit user="A12345" OR ip="82.34.244.83" 
| eval timestamp=strftime(_time, "%d/%m/%Y %H:%M UTC") 
| table timestamp, user, ip, action, result, clientAppUsed, deviceDisplayName, os 
| sort - _time

```

---

### Technical Note on Why the Device Was Not Blocked Pre-Installation During Enrollment

When an Android BYOD device (such as the Pixel 8a running Android 14) successfully enrolls despite policy intent, it is typically driven by one of the following architectural root causes within Microsoft Intune:

1. **Misconfigured or Default OS Version Boundaries:** The active *Device Platform Restriction* policy assigned to the user group had its **Minimum OS Version** set to a value equal to or lower than Android 14 (e.g., set to `12.0` or `13.0` rather than a stricter or higher baseline), or the restriction was left at default factory baselines which do not proactively exclude newer major OS releases. Intune evaluates version numbers strictly against the configured integer/decimal range; if the target OS falls within the allowed minimum-to-maximum bracket, enrollment proceeds successfully.
2. **Policy Scope or Priority Conflict:** A broader default policy with lower security stringency took precedence over a restrictive custom policy due to assignment priority ordering or incorrect user group targeting, allowing the enrollment engine to validate and accept the device identity token.


When it comes to **Advanced Hunting in Microsoft Defender XDR using KQL (Kusto Query Language)**, there is a critical constraint given your environment setup:

> **Important Architecture Constraint:** Advanced Hunting tables (such as `DeviceEvents`, `DeviceInfo`, `DeviceFileEvents`, etc.) **only populate if Microsoft Defender for Endpoint (MDE) sensors are actively deployed and running on the endpoint.** Because these corporate BYOD mobile devices have *no* MDE or Mobile Threat Defense installed, running device-level KQL queries in the Defender portal will return **zero results** for this device.

However, if you want to query what *is* captured by Microsoft 365 (via Entra ID sign-ins and audit telemetry ingested into Defender XDR/Log Analytics workspaces), you can use identity-centric KQL tables like `SigninLogs` and `AuditLogs`.

---

### Alternative KQL Queries (Identity & Enrollment Focus)

Since device telemetry tables (`DeviceInfo`) will be empty for `Pixel_8A`, use these identity-focused KQL queries in Microsoft Defender Advanced Hunting or Microsoft Sentinel to track the user activity and sign-in context:

#### 1. Correlating User Sign-Ins and Device Registration Context

This query checks Microsoft Entra sign-in events for user `A12345` around the incident timestamp to see how the device authenticated and whether it was tagged as compliant or registered during the passkey workflow.

```kusto
SigninLogs
| where TimeGenerated between (ago(7d) .. now())
| where UserPrincipalName has "A12345" or UserId has "A12345"
| project TimeGenerated, UserPrincipalName, IPAddress, DeviceDetail, ConditionalAccessStatus, Status, ResultDescription
| sort by TimeGenerated desc

```

#### 2. Tracking Intune Audit and Enrollment Configuration Changes

To check if policy rules or device enrollment restrictions were modified around the time of the event, query the audit logs:

```kusto
AuditLogs
| where TimeGenerated between (ago(7d) .. now())
| where OperationName has_any ("Device", "Enrollment", "Restriction", "Policy")
| where InitiatedBy has "A12345" or TargetResources has "A12345"
| project TimeGenerated, OperationName, InitiatedBy, TargetResources, Result
| sort by TimeGenerated desc

```

---

### Jira Documentation Note

When completing your incident report, document the Advanced Hunting limitation explicitly:

* *"KQL queries against MDE tables (`DeviceInfo`, `DeviceEvents`) returned 0 results due to the absence of Defender for Mobile Endpoint on the BYOD asset (`Pixel_8A`). Investigation was restricted to identity-layer Entra logs (`SigninLogs`)."*

Here is a concise, ready-to-paste closing comment tailored for your Jira ticket:

> **Investigation Summary & Closing Note:**
> Threat hunting and log correlation were conducted across Microsoft Entra ID, Intune, Splunk, and Microsoft Defender XDR for user `CLIENT\A12345` (`Pixel_8A` / `AndroidForWork_12`) originating from IP `82.34.244.83` at `19/10/2026 15:20 UTC`.
> **Findings:**
> * **Policy Configuration:** The device successfully enrolled under Android 14 because the active Intune *Device Platform Restriction* profile permitted the OS version range (either due to the minimum/maximum OS boundary settings allowing Android 14 or policy assignment priority).
> * **Telemetry Limitations:** Because this is a BYOD asset without Microsoft Defender for Endpoint (MDE) or Mobile Threat Defense (MTD) installed, local device telemetry, app installation traces, and MDE KQL tables (`DeviceInfo`, `DeviceEvents`) contained zero endpoint records. Analysis was restricted to cloud identity sign-in and audit logs (`SigninLogs`, `AuditLogs`, and Splunk authentication streams).
> 
> 
> **Disposition:** Confirmed expected behavior based on current Intune enrollment configuration boundaries. No indicators of external compromise or anomalous post-enrollment activity were identified in identity logs. Closing ticket and recommending review of Intune Android Enterprise platform restriction baselines if Android 14 is intended to be blocked for MFA Passkey onboarding.
