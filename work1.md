

Threat Hunting Readiness Checklist

To build our threat hunting playbook and ensure we have full visibility following tester completion, please help fill in the gaps for the following items:

1. Log Architecture & Data Pipelines

• Log Destinations: Where are the logs for Defender, Splunk, Sentinel, Entra, and Intune being centralized? Are Entra/Intune logs being forwarded directly to Sentinel, Splunk, or both?
• Ingestion Mapping: Which specific log sources (e.g., Entra Sign-in logs, Intune device actions, Defender DeviceProcessEvents) are currently active and onboarding into our SIEM?
• Cross-Platform Sync: Is there a data sync or duplication between Splunk and Sentinel that we need to be aware of to avoid duplicate alerting or split-brain hunting?

2. Log Retention & Volumes

• Retention Windows: What is the hot, warm, and cold retention policy for logs in Splunk vs. Sentinel?
• Historical Lookback: How far back can we realistically hunt if a test case requires analyzing historical baselines (e.g., 30, 90, or 185+ days)?

3. Access & Permissions

• Access Requests: What are the exact AD groups, IAM roles, or Entra roles required for the purple team to query these logs?
• RBAC Restrictions: Are there any Row-Level Security (RLS) or tenant-level restrictions that will block us from seeing specific sensitive assets or executive logs?
• API / CLI Access: Do we have programmatic access (e.g., Jupyter Notebooks, KQL/Splunk APIs) if we need to automate extraction for large test cases?

4. Environment & Tooling Context

• Coverage Matrix: Is there an existing list or Confluence page mapping our IT assets to their respective logging coverage (e.g., which servers lack Defender, which enclaves don't log to Splunk)?
• Testing Baselines: Where are the testers documenting their source IPs, test accounts, and timestamps so we can cross-reference them during our hunts?
