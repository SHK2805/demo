================================================================================
PRINCIPAL AWS SECURITY ARCHITECT & AI SECURITY INTERVIEW PREPARATION GUIDE
================================================================================
Target Role: Senior / Principal System Security Architect (Barclays)
Target Level: ~10 Years Experience (Cloud, AWS, AI Architecture, Risk Evaluation)
Baseline Study Budget: 27 Hours Baseline (+ 5 Hours Extension)

--------------------------------------------------------------------------------
DOCUMENT CONTROL & METADATA
--------------------------------------------------------------------------------
Document Type: Master Study Resource & Interview Prep Guide
Version: v2.0 (Interview-Optimized)
Date: 2026-11-09
Focus Areas: Technical Architecture, Trust Boundaries, Risk Decomposition, 
             Bedrock / Agentic AI Security, AWS Data Perimeters, Defense-in-Depth.

================================================================================
TOPIC T01: SECURITY ARCHITECTURE REVIEW METHODOLOGY & CHANGE GATING
================================================================================
[Core Guidance]
- Shift security from manual gatekeeping to automated policy-as-code change-gating embedded in CI/CD pipelines.
- Focus reviews on Data Flow Diagrams (DFDs), trust boundaries (AWS accounts, RAM cross-account roles, VPCs), and key policies.
- Clearly separate technical risk evaluation from enterprise governance: governance handles policy oversight, security architecture evaluates technical risk, threats, and control effectiveness.

[Recommended Resources & Search Terms]
- YouTube Search: "AWS re:Invent security architecture review", "Scale security architecture AWS", "Threat modeling enterprise AWS architecture"
- Authoritative Channels: AWS Events, AWS Online Tech Talks, OWASP Foundation
- Primary Docs: AWS Well-Architected Framework (Security Pillar), NIST SP 800-37 (Risk Management Framework)

[Verbal Interview Script]
Question: "How do you perform a security architecture review and decide whether a solution is production ready?"
Answer: "I structure architecture reviews around data flow analysis and trust boundary decomposition. First, I examine the DFD to identify where data crosses administrative or security boundaries—such as public internet to VPC, or tenant-isolated application tiers. Second, I evaluate risk by assessing likelihood and technical impact, ensuring preventive controls (IAM least-privilege, network perimeters) take precedence over detective alerting. Finally, I determine production readiness by verifying that residual risks are formally documented, automated policy-as-code gates are passing, and any technical risk acceptance is explicitly signed off against enterprise risk thresholds."


================================================================================
TOPIC T11: AI SECURITY RISK ASSESSMENT FRAMEWORKS & TECHNICAL RISK EVALUATION
================================================================================
[Core Guidance]
- Decompose AI architecture into 5 layers: UI, Orchestration/Agents, Foundation Models, Retrieval (Vector DB), Execution Sinks.
- Key Workloads:
  * Amazon Bedrock: Guardrails, model isolation, cross-region resilience.
  * Agentic AI: Scoped IAM execution roles, loop prevention, human-in-the-loop gates for destructive calls.
  * RAG Systems: Vector DB isolation (OpenSearch Serverless), chunk-level metadata tagging, dynamic JWT user-filtering.
  * MCP Architecture: Inter-server TLS, tool poisoning defense, input/output schema validation.
  * SaaS AI: AWS PrivateLink endpoints, egress data filtering, zero-data-retention verification.

[Recommended Resources & Search Terms]
- YouTube Search: "AWS re:Invent Generative AI security Bedrock", "OWASP Top 10 for LLMs deep dive", "AI security risk assessment architecture"
- Authoritative Channels: AWS Events, OWASP Foundation, Defcon
- Primary Docs: AWS Secure Generative AI on AWS, OWASP Top 10 for Large Language Models, NIST AI 100-1 (AI RMF)

[Verbal Interview Script]
Question: "How would you perform a security assessment of an AI solution utilizing Bedrock, RAG, and autonomous agents?"
Answer: "I perform a structured threat assessment by decomposing the architecture into its core functional layers. For Bedrock and foundation models, I verify input/output guardrails and prompt engineering boundaries. For RAG systems, I ensure vector database queries enforce fine-grained metadata filtering based on user-context JWT claims, preventing horizontal data leakage. For autonomous agents, I treat the LLM as an untrusted reasoning engine: its execution role is strictly scoped using least-privilege IAM policies, and any destructive tool call requires a deterministic, programmatic authorization token generated outside the LLM. Finally, I map these vectors to preventive and detective controls, establishing clear production-readiness criteria."


================================================================================
TOPIC T02: THREAT MODELLING WORKFLOW & LLM THREAT CATALOGUE
================================================================================
[Core Guidance]
- Apply STRIDE to LLM vectors: Tampering (Prompt Injection), Denial of Service (Denial of Wallet / Token Exhaustion), Elevation of Privilege (Excessive Agency).
- Architect defenses against indirect prompt injection by isolating retrieved untrusted data within strict XML delimiters and decoupling retrieval from downstream execution sinks.

[Recommended Resources & Search Terms]
- YouTube Search: "Threat modeling LLM applications OWASP", "Prompt injection attack vectors architecture"
- Authoritative Channels: OWASP Foundation, Black Hat, Defcon
- Primary Docs: OWASP LLM Application Security Verification Standard (LLMASVS), MITRE ATLAS

[Verbal Interview Script]
Question: "How do you architect defenses against indirect prompt injection in an enterprise RAG application?"
Answer: "We assume all external retrieved content is hostile. Architecturally, retrieved text is enclosed in strict XML delimiters (<untrusted_data>) and processed through intermediate parsers before reaching the primary prompt context. Furthermore, downstream execution sinks treat LLM output as untrusted string data, utilizing schema validation to prevent code execution."


================================================================================
TOPIC T04: AI IDENTITY ARCHITECTURE, AUTHORIZATION PATTERNS, & MCP
================================================================================
[Core Guidance]
- Machine-to-machine trust via IAM execution roles and short-term STS credentials.
- Propagate user identity (JWT claims via Cognito/OIDC) directly to backend services rather than trusting the LLM to manage entitlement checks.
- Enforce MCP server container isolation (AWS Fargate), mTLS, and strict input/output schema validation to mitigate tool poisoning and confused deputy exploits.

[Recommended Resources & Search Terms]
- YouTube Search: "AWS IAM advanced architectural patterns", "Zero trust authorization microservices AWS", "Secure AI agent tool invocation architecture"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: AWS IAM Best Practices, Model Context Protocol (MCP) Security Guidelines

[Verbal Interview Script]
Question: "How do you design authorization for an AI agent invoking tools via the Model Context Protocol?"
Answer: "The AI agent operates under strict least privilege. When invoking an MCP tool, it passes the end-user's signed JWT token. The MCP server independently validates token claims and enforces deterministic access control. The LLM never decides authorization."


================================================================================
TOPIC T08: CLOUD SECURITY DECISIONS, DATA PERIMETERS, & EGRESS DEFENSE
================================================================================
[Core Guidance]
- Establish cloud data perimeters using AWS Organizations SCPs (`aws:PrincipalOrgID`), S3 resource policies, and VPC endpoint policies.
- Eliminate public internet traversal for third-party AI APIs using AWS PrivateLink, AWS Network Firewall, and Route 53 Resolver DNS Firewall.

[Recommended Resources & Search Terms]
- YouTube Search: "AWS Data Perimeter architectural patterns re:Invent", "AWS PrivateLink security best practices"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: Building a Data Perimeter on AWS, AWS PrivateLink Guidance

[Verbal Interview Script]
Question: "How do you prevent a compromised AI workload from exfiltrating data to external endpoints?"
Answer: "We enforce defense-in-depth: organizational SCPs restrict data flows to trusted accounts; S3 and KMS policies deny external access; private VPCs route traffic through PrivateLink rather than NAT gateways; and DNS Firewall blocks unauthorized external domains."


================================================================================
TOPIC T07: SECURE RAG & SUPPLY CHAIN SECURITY
================================================================================
[Core Guidance]
- Sandbox document ingestion pipelines in ephemeral subnets.
- Enforce dynamic metadata filtering (tenant ID, ACLs) at the vector database layer (Amazon OpenSearch Serverless) during k-NN queries.

[Recommended Resources & Search Terms]
- YouTube Search: "Secure RAG architecture AWS Bedrock OpenSearch", "Vector database security enterprise"
- Authoritative Channels: AWS Events, OWASP Foundation
- Primary Docs: Amazon OpenSearch Service Security Guide, OWASP GenAI Security Project

[Verbal Interview Script]
Question: "How do you prevent horizontal data leakage across tenants in a shared vector database?"
Answer: "Every document chunk is indexed with cryptographic metadata attributes. At retrieval time, verified user JWT group claims are translated into mandatory query filters enforced directly by OpenSearch before ranking, ensuring unauthorized chunks never enter the LLM context."


================================================================================
TOPIC T05: IMPROPER OUTPUT HANDLING & DEFENSIVE SINKS
================================================================================
[Core Guidance]
- Treat all LLM outputs as untrusted string inputs.
- Enforce strict JSON / Pydantic schema validation, parameterized SQL query construction, and sandboxed execution environments (AWS Lambda / Fargate with read-only filesystems).

[Recommended Resources & Search Terms]
- YouTube Search: "Application security improper output handling LLM", "Secure coding practices AI integration"
- Authoritative Channels: OWASP Foundation, Black Hat
- Primary Docs: OWASP Top 10: Improper Output Handling, AWS Lambda Security Best Practices

[Verbal Interview Script]
Question: "How do you secure execution sinks when an LLM generates database queries or code?"
Answer: "We prohibit direct string execution. SQL queries use parameterized structures where the LLM only provides variable parameters. Code execution occurs within ephemeral, resource-constrained containers with zero network access."


================================================================================
TOPIC T06: AI-SPECIFIC INCIDENT RESPONSE & CONTAINMENT
================================================================================
[Core Guidance]
- Execute rapid containment using emergency IAM inline deny policies with the `aws:TokenIssueTime` condition key to instantly invalidate temporary security tokens.
- Automate parallel log preservation (Bedrock logs, CloudTrail, VPC Flow Logs) to immutable S3 vaults protected by S3 Object Lock.

[Recommended Resources & Search Terms]
- YouTube Search: "AWS incident response automation Lambda", "Cloud forensics and containment AWS"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: AWS Security Incident Response Guide, Automated Incident Response in the Cloud

[Verbal Interview Script]
Question: "How do you contain a compromised AI agent exhibiting runaway loops or data exfiltration?"
Answer: "We trigger automated Lambda playbooks that apply an emergency IAM inline deny policy using aws:TokenIssueTime to invalidate active tokens instantly. In parallel, forensic telemetry is snapshotted to an immutable S3 vault protected by Object Lock."


================================================================================
TOPIC T09: AI OBSERVABILITY, MONITORING, & TELEMETRY
================================================================================
[Core Guidance]
- Centralize telemetry streaming across Amazon Security Lake and OpenSearch.
- Monitor infrastructure anomalies via Amazon GuardDuty and track token consumption velocity to flag Denial of Wallet attacks and prompt flooding.

[Recommended Resources & Search Terms]
- YouTube Search: "Amazon Security Lake architecture and integration", "AWS GuardDuty advanced threat detection re:Invent"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: Amazon Security Lake User Guide, Amazon GuardDuty User Guide

[Verbal Interview Script]
Question: "How do you monitor distributed LLM workloads to detect prompt injection and token abuse?"
Answer: "We stream Bedrock invocation logs into Amazon Security Lake and ingest structured agent reasoning traces into OpenSearch. Real-time SIEM rules track token velocity anomalies and flag suspicious multi-turn prompt injection patterns."


================================================================================
TOPIC T10: SUPPORTING SECURITY DOMAINS (SAAS, CONTACT CENTRE, SDLC)
================================================================================
[Core Guidance]
- Amazon Connect Omnichannel Security: Real-time PII redaction on transcriptions, KMS CMKs, IAM Identity Center SAML/SCIM integration.
- Deploy SaaS Security Posture Management (SSPM) tools to audit third-party SaaS AI integrations.

[Recommended Resources & Search Terms]
- YouTube Search: "Amazon Connect security architecture best practices", "AWS IAM Identity Center SCIM integration"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: Amazon Connect Administrator Guide, AWS IAM Identity Center User Guide

[Verbal Interview Script]
Question: "How do you secure an Amazon Connect contact center integrating generative AI transcription and customer bots?"
Answer: "Voice streams are scrubbed of PII by automated redaction filters before transcription. Bedrock bots operate in isolated VPCs, accessing backend systems via rate-limited API gateways. Agent access is federated via IAM Identity Center with automated SCIM provisioning."


================================================================================
TOPIC T03: TECHNICAL PREVENTIVE VS. DETECTIVE TRADE-OFFS
================================================================================
[Core Guidance]
- Evaluate architectural trade-offs: Preventive controls (Bedrock Guardrails, SCPs) block threats upfront but carry latency/false-positive risks. Detective controls (GuardDuty, SIEM analytics) provide flexible anomaly detection for stochastic threats.
- Deploy a hybrid architecture: preventive controls guard hard boundaries, detective controls capture semantic evasion attempts.

[Recommended Resources & Search Terms]
- YouTube Search: "Preventative vs detective security controls AWS architecture", "Designing resilient security guardrails AWS"
- Authoritative Channels: AWS Events, AWS Online Tech Talks
- Primary Docs: AWS Well-Architected Framework (Security Pillar), AWS Security Reference Architecture (SRA)

[Verbal Interview Script]
Question: "How do you decide between preventive and detective controls for non-deterministic threats like prompt injection?"
Answer: "We use preventive controls (Bedrock Guardrails) at critical transaction boundaries to block superficial attacks. However, because prompt injection is semantic and evolving, we rely on detective controls (semantic monitoring, SIEM analytics) for real-time behavioral anomaly detection."


================================================================================
SCENARIO PREPARATION MODULES (SC01 - SC05)
================================================================================
SC01: Customer Service Bot & Core Banking APIs
- Focus: Omnichannel Amazon Connect trust boundaries, PII redaction, step-up auth (MFA/biometric) before transactional API execution, API Gateway WAF.

SC02: Multi-Tenant Data Platform & SaaS Integration
- Focus: Data perimeter (`aws:PrincipalOrgID`), AWS PrivateLink for SaaS AI, per-tenant KMS Customer Managed Keys, SCIM/SSO, SSPM.

SC03: Enterprise RAG Assistant & Metadata Filtering
- Focus: Ingestion metadata tagging, dynamic user-context JWT metadata filtering enforced directly inside vector database k-NN queries.

SC04: AI Monitoring, Detection, & Incident Response
- Focus: Differentiating GuardDuty (control-plane) from SIEM application logs; rapid IAM role containment via `aws:TokenIssueTime`; immutable S3 Object Lock vaults.

SC05: Remediating an Unreviewed Agentic Deployment
- Focus: Emergency network containment (VPC Security Group / Network ACL shutdown), IAM deny policy application, forensic log capture, retrofitting CloudFormation Guard policy-as-code in CI/CD pipelines.


================================================================================
EXTENSION TOPICS (EXT-1, EXT-2 - SECONDARY PRIORITY)
================================================================================
Note: Study only after completing T01-T11 and SC01-SC05.

Ext-1: Advanced Threat Hunting for Autonomous Agents
- Focus: Multi-turn prompt injection detection and silent exfiltration hunting (correlating Bedrock token counts with VPC flow logs and DNS queries).

Ext-2: Control Plane Hardening & Automated CI/CD Gating
- Focus: Automated policy-as-code checks (CloudFormation Guard / OPA) and pre-production AI agent red-teaming in build pipelines.
================================================================================
