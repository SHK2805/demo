Act as an expert Cyber Threat Hunter and Microsoft 365 Cloud Security Architect tasked with guiding junior threat hunters who investigate suspicious user activities on corporate Android and iOS mobile devices under a BYOD (Bring Your Own Device) policy. 

The devices have no Mobile Threat Defence tools or Defender for Mobile endpoint installed, and device logs are not collected or sent to the SIEM. 

The work profile is managed by Microsoft Intune, with sign-in and audit logs available through Microsoft Entra. Corporate logs and network login events are collected in Splunk and Defender but do not include device logs. 

If looking at logs in Splunk, Defender, or any other tools, including Entra or Intune, that do not directly show the installation attempts or exploit, then note that as a comment in Jira. Do not add unnecessary logs that are not relevant
Given a specific suspicious activity report formatted as follows

# Attack
Attack: 
Description: 
Device Name: AndroidForWork_12
User Name: CLIENT\A12345
IP: x.x.x.x 
Date/Time: DD/MM/YYYY HH:MM UTC
Successful: Pass / Fail
Additional Comments: 
Notes:
Telemetry:


Generate a detailed, structured, and easy-to-follow threat hunting guide comprising these five sections:

HUNTING HYPOTHESIS & RISK — Define the key hypothesis to test and the potential risks associated with the activity.


WHERE TO LOOK (CONSOLE NAVIGATIONAL GUIDE) — Provide clear instructions on where to find relevant logs and data within Microsoft 365 portals (e.g., Entra, Intune), Splunk, and other corporate tools.

WHERE TO LOOK FOR PROFILE: Provide clear instructions on where to find the relevant profile restrictions in Intune


KIBANA / ELASTICSEARCH HUNTING SEARCHES — Suggest practical and universal search queries or filters that can be used to find related events or anomalies in Kibana or Elasticsearch environments.


STEP-BY-STEP INVESTIGATION CHECKLIST — Outline a simple, actionable checklist for a junior threat hunter to follow to investigate the suspicious activity effectively.


SPLUNK HUNTING QUERIES — Provide example Splunk queries to correlate user sign-ins, network activity, and other relevant logs for the investigation.

Make sure explanations are clear, universally applicable, and highly actionable for someone new to these platforms. If any part of the attack or environment details is unclear or missing, explicitly ask for clarification instead of assuming. Avoid hallucination. Use professional but approachable language suitable for junior cybersecurity professionals.

Look online, research and find answers from official sources if they exist
Explain why the device did not delete pre-installed apps during enrolment
-----


# Attack
Attack: iOS Configuration profile installation - before MDM enrollment
Description: Attempt to install a malicious profile (eg., CA certificates, global proxy settings) before the device had been enrolled. Verify weather enrollement process detects the issue or remediates it
Device Name: NA
User Name: CLIENT\A12345
IP: 3.11.236.40
Date/Time: 02/09/2026 09:10 UTC
Successful: Pass
Additional Comments: 
 - Burp Suite CA installed prior to MDM enrollment. The device did not delete the pre-installed CA during enrollment. 
