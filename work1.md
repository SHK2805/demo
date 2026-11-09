# STUDY PLAN —Cloud Security Architect & AI Security

**Focus Areas:** Technical Architecture · Trust Boundaries · Risk Decomposition  
Bedrock / Agentic AI Security · AWS Data Perimeters · Defense-in-Depth

---

## TOPIC OVERVIEW

- **T01** Security Architecture Review Methodology & Change Gating
- **T02** Threat Modelling Workflow & LLM Threat Catalogue
- **T03** Technical Preventive vs. Detective Trade-offs
- **T04** AI Identity Architecture, Authorization Patterns, & MCP
- **T05** Improper Output Handling & Defensive Sinks
- **T06** AI-Specific Incident Response & Containment
- **T07** Secure RAG & Supply Chain Security
- **T08** Cloud Security Decisions, Data Perimeters, & Egress Defense
- **T09** AI Observability, Monitoring, & Telemetry
- **T10** Supporting Security Domains (SaaS, Contact Centre, SDLC)
- **T11** AI Security Risk Assessment Frameworks & Technical Risk Evaluation
- **SC01–SC05** Scenario Preparation Modules
- **EXT-1–2** Extension Topics (study after T01–T11 and SC01–SC05)

---

## T01 · Security Architecture Review Methodology & Change Gating

### Key Concepts

- Shift security from manual gatekeeping → automated policy-as-code change-gating embedded in CI/CD pipelines
- Focus reviews on:
  - Data Flow Diagrams (DFDs)
  - Trust boundaries (AWS accounts, RAM cross-account roles, VPCs)
  - Key policies
- Separate concerns clearly:
  - Governance → policy oversight
  - Security Architecture → technical risk, threats, control effectiveness

### Study Resources

- **Docs**
  - AWS Well-Architected Framework (Security Pillar)
  - NIST SP 800-37 (Risk Management Framework)
- **YouTube**
  - "AWS re:Invent security architecture review"
  - "Scale security architecture AWS"
  - "Threat modeling enterprise AWS architecture"
- **Channels**
  - AWS Events · AWS Online Tech Talks · OWASP Foundation

### Q&A

**Q: How do you perform a security architecture review and decide whether a solution is production ready?**

**A:** I structure reviews around data flow analysis and trust boundary decomposition.

**Step 1** — examine the DFD to identify where data crosses administrative or security boundaries (e.g. public internet → VPC, or tenant-isolated application tiers).

**Step 2** — evaluate risk by assessing likelihood and technical impact, ensuring preventive controls (IAM least-privilege, network perimeters) take precedence over detective alerting.

**Step 3** — determine production readiness by verifying:

- Residual risks are formally documented
- Automated policy-as-code gates are passing
- Technical risk acceptance is explicitly signed off against enterprise risk thresholds

---

## T02 · Threat Modelling Workflow & LLM Threat Catalogue

### Key Concepts

- Apply STRIDE to LLM vectors:
  - Tampering → Prompt Injection
  - Denial of Service → Denial of Wallet / Token Exhaustion
  - Elevation of Priv → Excessive Agency
- Defend against indirect prompt injection by:
  - Isolating retrieved untrusted data inside strict XML delimiters
  - Decoupling retrieval from downstream execution sinks

### Study Resources

- **Docs**
  - OWASP LLM Application Security Verification Standard (LLMASVS)
  - MITRE ATLAS
- **YouTube**
  - "Threat modeling LLM applications OWASP"
  - "Prompt injection attack vectors architecture"
- **Channels**
  - OWASP Foundation · Black Hat · Defcon

### Q&A

**Q: How do you architect defenses against indirect prompt injection in an enterprise RAG application?**

**A:** We assume all external retrieved content is hostile.

**Architecturally:**

- Retrieved text is enclosed in strict XML delimiters (`<untrusted_data>`) and processed through intermediate parsers before reaching the primary prompt context
- Downstream execution sinks treat LLM output as untrusted string data, using schema validation to prevent code execution

---

## T03 · Technical Preventive vs. Detective Trade-offs

### Key Concepts

- Preventive controls (e.g. Bedrock Guardrails, SCPs):
  - Block threats upfront
  - Trade-off: latency and false-positive risks
- Detective controls (e.g. GuardDuty, SIEM analytics):
  - Flexible anomaly detection for stochastic threats
- Recommended approach: hybrid architecture
  - Preventive controls → guard hard boundaries
  - Detective controls → capture semantic evasion attempts

### Study Resources

- **Docs**
  - AWS Well-Architected Framework (Security Pillar)
  - AWS Security Reference Architecture (SRA)
- **YouTube**
  - "Preventative vs detective security controls AWS architecture"
  - "Designing resilient security guardrails AWS"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you decide between preventive and detective controls for non-deterministic threats like prompt injection?**

**A:** We use preventive controls (Bedrock Guardrails) at critical transaction boundaries to block superficial attacks.

However, because prompt injection is semantic and constantly evolving, we rely on detective controls (semantic monitoring, SIEM analytics) for real-time behavioral anomaly detection.

---

## T04 · AI Identity Architecture, Authorization Patterns, & MCP

### Key Concepts

- Machine-to-machine trust via IAM execution roles and short-term STS credentials
- Propagate user identity (JWT claims via Cognito/OIDC) directly to backend services — do NOT trust the LLM to manage entitlement checks
- MCP server security:
  - Container isolation (AWS Fargate)
  - Mutual TLS (mTLS)
  - Strict input/output schema validation
  - Mitigates tool poisoning and confused deputy exploits

### Study Resources

- **Docs**
  - AWS IAM Best Practices
  - Model Context Protocol (MCP) Security Guidelines
- **YouTube**
  - "AWS IAM advanced architectural patterns"
  - "Zero trust authorization microservices AWS"
  - "Secure AI agent tool invocation architecture"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you design authorization for an AI agent invoking tools via the Model Context Protocol?**

**A:** The AI agent operates under strict least privilege.

**When invoking an MCP tool:**

- The agent passes the end-user's signed JWT token
- The MCP server independently validates token claims and enforces deterministic access control
- The LLM never decides authorization

---

## T05 · Improper Output Handling & Defensive Sinks

### Key Concepts

- Treat ALL LLM outputs as untrusted string inputs
- Enforce:
  - Strict JSON / Pydantic schema validation
  - Parameterized SQL query construction (never raw string execution)
  - Sandboxed execution environments (AWS Lambda / Fargate with read-only filesystems)

### Study Resources

- **Docs**
  - OWASP Top 10: Improper Output Handling
  - AWS Lambda Security Best Practices
- **YouTube**
  - "Application security improper output handling LLM"
  - "Secure coding practices AI integration"
- **Channels**
  - OWASP Foundation · Black Hat

### Q&A

**Q: How do you secure execution sinks when an LLM generates database queries or code?**

**A:** We prohibit direct string execution entirely.

- SQL queries use parameterized structures — the LLM only supplies variable parameters, never the query structure
- Code execution occurs within ephemeral, resource-constrained containers with zero network access

---

## T06 · AI-Specific Incident Response & Containment

### Key Concepts

- Rapid containment using emergency IAM inline deny policies with the `aws:TokenIssueTime` condition key → instantly invalidates temporary tokens
- Automate parallel log preservation:
  - Bedrock logs, CloudTrail, VPC Flow Logs
  - Store in immutable S3 vaults protected by S3 Object Lock

### Study Resources

- **Docs**
  - AWS Security Incident Response Guide
  - Automated Incident Response in the Cloud
- **YouTube**
  - "AWS incident response automation Lambda"
  - "Cloud forensics and containment AWS"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you contain a compromised AI agent exhibiting runaway loops or data exfiltration?**

**A:** We trigger automated Lambda playbooks that:

1. Apply an emergency IAM inline deny policy using `aws:TokenIssueTime` to invalidate active tokens instantly
2. In parallel, snapshot forensic telemetry to an immutable S3 vault protected by Object Lock

---

## T07 · Secure RAG & Supply Chain Security

### Key Concepts

- Sandbox document ingestion pipelines in ephemeral subnets
- Enforce dynamic metadata filtering at the vector DB layer:
  - Tenant ID and ACLs applied at Amazon OpenSearch Serverless
  - Filters enforced during k-NN queries before results are returned

### Study Resources

- **Docs**
  - Amazon OpenSearch Service Security Guide
  - OWASP GenAI Security Project
- **YouTube**
  - "Secure RAG architecture AWS Bedrock OpenSearch"
  - "Vector database security enterprise"
- **Channels**
  - AWS Events · OWASP Foundation

### Q&A

**Q: How do you prevent horizontal data leakage across tenants in a shared vector database?**

**A:** Every document chunk is indexed with cryptographic metadata attributes.

**At retrieval time:**

- Verified user JWT group claims are translated into mandatory query filters enforced directly by OpenSearch before ranking
- Unauthorized chunks never enter the LLM context

---

## T08 · Cloud Security Decisions, Data Perimeters, & Egress Defense

### Key Concepts

- Establish cloud data perimeters using:
  - AWS Organizations SCPs (`aws:PrincipalOrgID`)
  - S3 resource policies
  - VPC endpoint policies
- Eliminate public internet traversal for third-party AI APIs using:
  - AWS PrivateLink
  - AWS Network Firewall
  - Route 53 Resolver DNS Firewall

### Study Resources

- **Docs**
  - Building a Data Perimeter on AWS
  - AWS PrivateLink Guidance
- **YouTube**
  - "AWS Data Perimeter architectural patterns re:Invent"
  - "AWS PrivateLink security best practices"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you prevent a compromised AI workload from exfiltrating data to external endpoints?**

**A:** We enforce defense-in-depth across four layers:

1. Organizational SCPs restrict data flows to trusted accounts
2. S3 and KMS policies deny external access
3. Private VPCs route traffic through PrivateLink (not NAT gateways)
4. DNS Firewall blocks unauthorized external domains

---

## T09 · AI Observability, Monitoring, & Telemetry

### Key Concepts

- Centralize telemetry streaming across Amazon Security Lake and OpenSearch
- Monitor with Amazon GuardDuty for infrastructure anomalies
- Track token consumption velocity to flag:
  - Denial of Wallet attacks
  - Prompt flooding

### Study Resources

- **Docs**
  - Amazon Security Lake User Guide
  - Amazon GuardDuty User Guide
- **YouTube**
  - "Amazon Security Lake architecture and integration"
  - "AWS GuardDuty advanced threat detection re:Invent"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you monitor distributed LLM workloads to detect prompt injection and token abuse?**

**A:** We stream Bedrock invocation logs into Amazon Security Lake and ingest structured agent reasoning traces into OpenSearch.

**Real-time SIEM rules:**

- Track token velocity anomalies
- Flag suspicious multi-turn prompt injection patterns

---

## T10 · Supporting Security Domains (SaaS, Contact Centre, SDLC)

### Key Concepts

- Amazon Connect Omnichannel Security:
  - Real-time PII redaction on transcriptions
  - KMS Customer Managed Keys (CMKs)
  - IAM Identity Center SAML/SCIM integration
- Deploy SaaS Security Posture Management (SSPM) tools to audit third-party SaaS AI integrations

### Study Resources

- **Docs**
  - Amazon Connect Administrator Guide
  - AWS IAM Identity Center User Guide
- **YouTube**
  - "Amazon Connect security architecture best practices"
  - "AWS IAM Identity Center SCIM integration"
- **Channels**
  - AWS Events · AWS Online Tech Talks

### Q&A

**Q: How do you secure an Amazon Connect contact center integrating generative AI transcription and customer bots?**

**A:**

- Voice streams are scrubbed of PII by automated redaction filters before transcription
- Bedrock bots operate in isolated VPCs, accessing backend systems via rate-limited API gateways
- Agent access is federated via IAM Identity Center with automated SCIM provisioning

---

## T11 · AI Security Risk Assessment Frameworks & Technical Risk Evaluation

### Key Concepts

- Decompose AI architecture into 5 layers:
  1. UI
  2. Orchestration / Agents
  3. Foundation Models
  4. Retrieval (Vector DB)
  5. Execution Sinks

- Key workload security patterns:

| Workload | Security patterns |
|---|---|
| Amazon Bedrock | Guardrails, model isolation, cross-region resilience |
| Agentic AI | Scoped IAM execution roles, loop prevention, human-in-the-loop gates for destructive calls |
| RAG Systems | Vector DB isolation (OpenSearch Serverless), chunk-level metadata tagging, dynamic JWT user-filtering |
| MCP Architecture | Inter-server TLS, tool poisoning defense, input/output schema validation |
| SaaS AI | AWS PrivateLink endpoints, egress data filtering, zero-data-retention verification |

### Study Resources

- **Docs**
  - AWS Secure Generative AI on AWS
  - OWASP Top 10 for Large Language Models
  - NIST AI 100-1 (AI RMF)
- **YouTube**
  - "AWS re:Invent Generative AI security Bedrock"
  - "OWASP Top 10 for LLMs deep dive"
  - "AI security risk assessment architecture"
- **Channels**
  - AWS Events · OWASP Foundation · Defcon

### Q&A

**Q: How would you perform a security assessment of an AI solution utilizing Bedrock, RAG, and autonomous agents?**

**A:** I perform a structured threat assessment by decomposing the architecture into its core functional layers:

**Bedrock / Foundation Models**  
→ Verify input/output guardrails and prompt engineering boundaries

**RAG Systems**  
→ Ensure vector DB queries enforce fine-grained metadata filtering based on user-context JWT claims, preventing horizontal data leakage

**Autonomous Agents**

- Treat the LLM as an untrusted reasoning engine
- Execution role strictly scoped using least-privilege IAM policies
- Destructive tool calls require a deterministic, programmatic authorization token generated outside the LLM

**Final step:** map these vectors to preventive and detective controls, establishing clear production-readiness criteria.

---

## SCENARIO MODULES (SC01 – SC05)

### SC01 · Customer Service Bot & Core Banking APIs

**Focus areas:**

- Omnichannel Amazon Connect trust boundaries
- PII redaction
- Step-up authentication (MFA/biometric) before transactional API execution
- API Gateway WAF

### SC02 · Multi-Tenant Data Platform & SaaS Integration

**Focus areas:**

- Data perimeter enforcement (`aws:PrincipalOrgID`)
- AWS PrivateLink for SaaS AI
- Per-tenant KMS Customer Managed Keys
- SCIM/SSO
- SaaS Security Posture Management (SSPM)

### SC03 · Enterprise RAG Assistant & Metadata Filtering

**Focus areas:**

- Ingestion metadata tagging
- Dynamic user-context JWT metadata filtering enforced directly inside vector database k-NN queries

### SC04 · AI Monitoring, Detection, & Incident Response

**Focus areas:**

- Differentiating GuardDuty (control-plane) from SIEM application logs
- Rapid IAM role containment via `aws:TokenIssueTime`
- Immutable S3 Object Lock vaults

### SC05 · Remediating an Unreviewed Agentic Deployment

**Focus areas:**

- Emergency network containment (VPC Security Group / Network ACL shutdown)
- IAM deny policy application
- Forensic log capture
- Retrofitting CloudFormation Guard policy-as-code into CI/CD pipelines

---

## EXTENSION TOPICS (study after completing T01–T11 and SC01–SC05)

### EXT-1 · Advanced Threat Hunting for Autonomous Agents

**Focus:**

- Multi-turn prompt injection detection
- Silent exfiltration hunting — correlating Bedrock token counts with VPC flow logs and DNS queries

### EXT-2 · Control Plane Hardening & Automated CI/CD Gating

**Focus:**

- Automated policy-as-code checks (CloudFormation Guard / OPA)
- Pre-production AI agent red-teaming in build pipelines
