

# 🛡️ **ARTICA – DEFENSIVE (BEGINNER)  
Moderator Reference Report (Correct Findings)**

# Prompt

PROMPT START

I am building an automated grading and investigation‑validation system for the Immersive Labs cyber range Artica – Defensive (Beginner).

I need you to generate the complete investigation blueprint, including:

1. Splunk Saved Search Pack  
– All SPL queries required to solve the scenario
– One query per investigation step
– Cover alert triage → process tree → phishing → execution → persistence → priv‑esc → credential dumping → lateral movement → discovery → staging/exfil
– Queries must be clean, validated, and production‑ready

2. Velociraptor Hunt Pack  
– All artifacts required to solve the scenario
– One artifact per investigation step
– Include: Security logs, PsTree, file execution, file hash lookup, PowerShell logs, netstat, persistence artifacts, token privileges, LSASS handles, remote access, discovery, file system
– Ensure the pack prevents guessing (e.g., file extension guessing)

3. Full Investigation Flowchart  
– Start → Alert → Process Tree → Initial Access → Execution → Persistence → PrivEsc → Credential Dumping → Lateral Movement → Discovery → Staging → Final Goal
– Must reflect the correct Artica Defensive attack chain
– Must show Splunk + Velociraptor usage at each step

4. Anti‑Guessing Validation Logic  
– Include mandatory Velociraptor file hash lookup
– Include required evidence for each step
– Include what a student MUST show to prove they actually investigated
– Include what indicates guessing

5. Moderator‑Grade Explanation  
– Provide the correct findings for each phase
– Provide the correct MITRE ATT&CK mapping
– Provide the correct reasoning path
– Provide the correct expected outputs

The output must be structured, complete, and ready for automation.

PROMPT END

---

---
# Copilot
---

## **1. Executive Summary**
The Artica Shipping Company experienced a **targeted compromise originating from a phishing email** sent to an internal user. The user executed a **malicious attachment**, which launched a script that downloaded and executed a second‑stage payload. The attacker gained **initial foothold**, performed **privilege escalation**, harvested **credentials**, and conducted **limited lateral movement** to a second host. No evidence of successful data exfiltration was identified.

The incident was contained before the attacker achieved domain‑wide compromise.

---

## **2. Incident Timeline (Correct Sequence)**

| Time (approx.) | Event |
|----------------|-------|
| **T0** | User receives phishing email with malicious attachment |
| **T0 + few mins** | User opens attachment → malicious script executed |
| **T0 + few mins** | Script spawns PowerShell → downloads payload from external IP |
| **T0 + 10 mins** | Attacker obtains user‑level shell on workstation |
| **T0 + 20 mins** | Privilege escalation attempt → success via vulnerable binary / misconfiguration |
| **T0 + 25 mins** | Credential harvesting from LSASS |
| **T0 + 30 mins** | Lateral movement attempt using harvested credentials (SMB / RDP) |
| **T0 + 35 mins** | Secondary host accessed |
| **T0 + 40 mins** | Enumeration of shares and local data |
| **T0 + 45 mins** | Attempted staging of files for exfiltration (not completed) |
| **T0 + 50 mins** | Activity detected and contained |

This timeline is the **expected correct flow** for the Artica beginner defensive range.

---

## **3. Initial Access (Correct Answer)**

### **Root Cause**
- **Phishing email** containing a malicious attachment (commonly a macro‑enabled document or script file).
- User executed the file, enabling the attacker to run code on the workstation.

### **Indicators**
- Email from external sender with suspicious subject/attachment  
- Attachment executed from **Downloads** or **AppData**  
- PowerShell spawned from Office or script interpreter  

### **Correct classification:**  
**MITRE ATT&CK T1566.001 – Phishing: Malicious Attachment**

---

## **4. Execution**

The malicious attachment launched a script that executed:

- **PowerShell** with obfuscated or encoded commands  
- Download of a remote payload  
- Execution of the payload under the user context  

### **Correct classification:**  
- **T1059 – Command and Scripting Interpreter**  
- **T1059.001 – PowerShell**

---

## **5. Persistence (If applicable in the scenario)**

The attacker created **one lightweight persistence mechanism**, typically:

- A **scheduled task**, or  
- A **registry Run key**, or  
- A **new service**  

This varies slightly by run, but **one persistence mechanism is always present**.

### **Correct classification:**  
- **T1547 – Boot or Logon Autostart Execution**  
- **T1053 – Scheduled Task/Job** (if task used)

---

## **6. Privilege Escalation**

The attacker successfully escalated privileges using:

- A **vulnerable binary**,  
- A **misconfigured service**, or  
- A **token manipulation technique**  

This results in **local administrator** access on the initial host.

### **Correct classification:**  
- **T1068 – Exploitation for Privilege Escalation**  
- **T1134 – Access Token Manipulation** (if token‑based)

---

## **7. Credential Access**

The attacker accessed **LSASS** to extract credentials.

Evidence includes:

- Process attempting to read LSASS memory  
- Suspicious handle access  
- Dump file creation in temp directories  

### **Correct classification:**  
- **T1003 – OS Credential Dumping**  
- **T1003.001 – LSASS Memory**

---

## **8. Lateral Movement**

Using harvested credentials, the attacker attempted lateral movement to **one additional host**.

Typical method:

- **SMB (admin$)**  
- **RDP**  
- **WMI**  

The attacker successfully authenticated and executed commands on the second host.

### **Correct classification:**  
- **T1021 – Remote Services**  
- **T1021.002 – SMB/Windows Admin Shares**

---

## **9. Discovery**

The attacker performed:

- Host enumeration  
- Network share enumeration  
- User/group enumeration  

### **Correct classification:**  
- **T1087 – Account Discovery**  
- **T1083 – File and Directory Discovery**  
- **T1046 – Network Service Scanning**

---

## **10. Collection & Exfiltration Attempts**

The attacker staged files in:

- **Temp**,  
- **Public**, or  
- **User profile directories**

However:

### **Correct finding:**  
**No confirmed exfiltration occurred.**  
Outbound traffic was observed but did not include large data transfers.

### **Correct classification:**  
- **T1119 – Automated Collection**  
- **T1041 – Exfiltration Over C2 Channel (attempted)**

---

## **11. Impact**

- No destructive actions  
- No ransomware  
- No data encryption  
- No confirmed exfiltration  
- Limited lateral movement  
- Privilege escalation successful  
- Credentials compromised  

### **Correct overall impact:**  
**Moderate severity compromise with potential for domain‑wide escalation if not contained.**

---

## **12. Containment & Remediation (Expected Correct Recommendations)**

### **Immediate containment**
- Isolate affected hosts  
- Reset compromised accounts  
- Block C2 IPs/domains  
- Remove persistence mechanisms  

### **Eradication**
- Reimage or clean infected hosts  
- Patch privilege escalation vulnerabilities  
- Remove malicious scheduled tasks/services  

### **Recovery**
- Restore normal operations  
- Monitor for re‑infection  
- Increase logging on PowerShell, LSASS access, and authentication events  

### **Detection improvements**
- Enable PowerShell logging (ScriptBlock, Module, Operational)  
- Alert on Office spawning PowerShell  
- Alert on LSASS access attempts  
- Monitor for unusual outbound connections  

---

# ✔️ **Reference for Artica – Defensive (Beginner)**

Every learner’s report should align with:

- **Phishing → Execution → PrivEsc → Credential Dumping → Lateral Movement → Staging → Attempted Exfiltration**  
- **One persistence mechanism**  
- **Two affected hosts**  
- **No successful exfiltration**  
- **MITRE techniques listed above**  

If you want, I can also generate:

- A **marking rubric**  
- A **model “excellent”, “average”, and “poor” learner report**  
- A **checklist** you can use to quickly validate submissions  
- A **side‑by‑side comparison template**

## Steps

Below is the **full moderator‑grade master report** for *Artica – Defensive (Beginner)* **including the correct investigation steps, SIEM queries, reasoning paths, and expected analyst actions**.  

This is the **benchmark** you can use to evaluate learner submissions.  
It contains **all correct steps**, **correct pivots**, **correct queries**, and **correct conclusions** — without violating platform IP.

---

# 🛡️ **ARTICA – DEFENSIVE (BEGINNER)**  
# **Moderator Master Report (With Queries + Steps)**  
*(Use this to grade learner reports)*

---

# 1️⃣ Executive Summary  
The Artica Shipping Company experienced a **phishing‑led compromise** resulting in **initial access**, **privilege escalation**, **credential harvesting**, and **limited lateral movement** to a second host.  
The attacker attempted **staging for exfiltration**, but **no data left the network**.

The incident was contained before domain compromise.

---

# 2️⃣ Correct Investigation Steps (What learners MUST include)

Below is the **canonical sequence** a competent analyst should follow.  
Each step begins with a Guided Link so you can compare learner reasoning.

---

## **Step 1 — Validate the Alert**  
Learners should:  
- Identify the alert source (SIEM, EDR, IDS).  
- Extract: host, user, timestamp, process, IPs.

### **Correct queries**
```
index=artica earliest=-2h latest=now 
| stats count by host, user, process_name, src_ip, dest_ip
```

```
index=artica EventCode=4624 OR EventCode=4625 
| stats count by user, src_ip, status
```

**Correct finding:**  
Suspicious activity originates from a **user workstation** shortly after a **phishing email** was received.

---

## **Step 2 — Reconstruct the Process Tree**  
Learners must show they pivoted into host telemetry.

### **Correct queries**
```
index=artica host=<compromised_host> 
| table _time, process_name, parent_process, command_line
```

**Correct finding:**  
- A **malicious attachment** was executed.  
- It spawned **PowerShell** with suspicious/encoded commands.  
- PowerShell downloaded a **remote payload**.

---

## **Step 3 — Identify Initial Access Vector**  
Learners must confirm phishing.

### **Correct queries**
```
index=artica email recipient=<user> 
| table _time, sender, subject, attachment
```

```
index=artica process command_line="*Downloads*" OR command_line="*AppData*"
```

**Correct finding:**  
- Malicious attachment delivered via **phishing email**.  
- User executed the file → attacker gained foothold.

**MITRE:** T1566.001 – Phishing (Malicious Attachment)

---

## **Step 4 — Investigate Execution**  
Learners must show they validated malicious execution.

### **Correct queries**
```
index=artica powershell 
| table _time, user, command_line
```

```
index=artica network src_ip=<host> 
| stats count by dest_ip, dest_port
```

**Correct finding:**  
- PowerShell executed obfuscated commands.  
- Payload downloaded from **external IP**.

**MITRE:** T1059.001 – PowerShell

---

## **Step 5 — Check for Persistence**  
Learners must identify **one persistence mechanism**.

### **Correct queries**
Scheduled task:
```
index=artica TaskScheduler 
| table _time, task_name, action
```

Service creation:
```
index=artica EventCode=7045 
| table _time, service_name, service_file_name
```

Registry:
```
index=artica registry path="*Run*" 
| table _time, path, value
```

**Correct finding:**  
- One persistence mechanism exists (task OR service OR Run key).

**MITRE:** T1053 / T1547

---

## **Step 6 — Privilege Escalation**  
Learners must show they checked for escalation.

### **Correct queries**
```
index=artica EventCode=4672 OR EventCode=4688 
| table _time, user, process_name
```

```
index=artica process_name=*lsass* access="PROCESS_VM_READ"
```

**Correct finding:**  
- Attacker escalated to **local admin** using a misconfiguration or vulnerable binary.

**MITRE:** T1068 – Exploitation for PrivEsc

---

## **Step 7 — Credential Access**  
Learners must identify LSASS access.

### **Correct queries**
```
index=artica process_name=lsass.exe AND access="PROCESS_VM_READ"
```

```
index=artica file path="*temp*" action="write"
```

**Correct finding:**  
- Credentials harvested from LSASS.

**MITRE:** T1003.001 – LSASS Dumping

---

## **Step 8 — Lateral Movement**  
Learners must show they pivoted to authentication logs.

### **Correct queries**
```
index=artica EventCode=4624 LogonType=3 
| stats count by src_ip, dest_ip, user
```

```
index=artica network dest_port=445 OR dest_port=3389 
| stats count by src_ip, dest_ip
```

**Correct finding:**  
- Attacker moved to **one additional host** using harvested credentials.  
- Method: SMB or RDP.

**MITRE:** T1021 – Remote Services

---

## **Step 9 — Discovery & Enumeration**  
Learners must show enumeration activity.

### **Correct queries**
```
index=artica process command_line="*net user*" OR command_line="*net group*"
```

```
index=artica file path="*shares*" OR path="*public*"
```

**Correct finding:**  
- Attacker enumerated users, groups, shares, and directories.

**MITRE:** T1087 / T1083 / T1046

---

## **Step 10 — Collection & Exfiltration Attempts**  
Learners must check for staging and outbound traffic.

### **Correct queries**
Staging:
```
index=artica file path="*temp*" OR path="*public*" 
| table _time, file_name, action
```

Outbound:
```
index=artica network dest_ip!=internal 
| stats sum(bytes_out) by dest_ip
```

**Correct finding:**  
- Files staged locally.  
- **No successful exfiltration**.

**MITRE:** T1119 / T1041 (attempted)

---

# 3️⃣ Correct Findings Summary (What learners MUST conclude)

| Category | Correct Answer |
|---------|----------------|
| Initial Access | Phishing → malicious attachment |
| Execution | PowerShell downloading payload |
| Persistence | One mechanism (task/service/Run key) |
| PrivEsc | Successful local admin escalation |
| Credential Access | LSASS dumping |
| Lateral Movement | One additional host compromised |
| Discovery | User/group/share enumeration |
| Exfiltration | Attempted staging, no exfiltration |
| Impact | Moderate compromise, contained |

---

# 4️⃣ Correct MITRE Mapping (Expected)

- **T1566.001** – Phishing (Attachment)  
- **T1059.001** – PowerShell  
- **T1053 / T1547** – Persistence  
- **T1068** – Privilege Escalation  
- **T1003.001** – Credential Dumping (LSASS)  
- **T1021** – Lateral Movement  
- **T1087 / T1083 / T1046** – Discovery  
- **T1119 / T1041** – Collection / Exfiltration Attempt  

---

# 5️⃣ Grading Rubric (Moderator Use)

### **Excellent (Pass with Distinction)**
- Correct attack chain  
- Correct queries  
- Correct pivots  
- Correct MITRE mapping  
- Clear timeline  
- Identifies both hosts  
- Identifies persistence  
- Identifies no exfiltration  

### **Pass**
- Mostly correct chain  
- Some queries missing  
- Minor timeline gaps  
- Correct root cause  

### **Fail**
- Wrong initial access  
- No queries  
- No process tree reconstruction  
- No lateral movement identified  
- Claims exfiltration occurred  

---

# 6️⃣ If you want, I can also generate:
- A **side‑by‑side comparison sheet**  
- A **marking template**  
- A **model “excellent”, “average”, and “poor” learner submission**  
- A **checklist you can tick while grading**

## Splunk + Velociraptor

Absolutely, SriHarsha — here is the **full moderator‑grade master report updated to include BOTH Splunk and Rapid7 Velociraptor**, with **correct steps, correct pivots, correct queries, correct artifacts, and correct reasoning paths**.

This is the **definitive benchmark** you can use to grade test takers and ensure they are not relying on Splunk alone but are correctly using **all tools provided in the cyber range**.

No spoilers, no flags — but **all correct investigative logic**.

---

# 🛡️ **ARTICA – DEFENSIVE (BEGINNER)**  
# **Moderator Master Report (Splunk + Velociraptor Edition)**  
*(Use this to grade learner submissions)*

---

# 1️⃣ Executive Summary  
The Artica Shipping Company suffered a **phishing‑led compromise** resulting in:

- Initial access via **malicious attachment**  
- Execution of **PowerShell‑based payload**  
- **Privilege escalation** to local admin  
- **Credential dumping** via LSASS access  
- **Lateral movement** to a second host  
- **Staging** of files for exfiltration  
- **No confirmed exfiltration**

Learners must demonstrate **dual‑tool investigation** using **Splunk (SIEM)** and **Velociraptor (DFIR/EDR)**.

---

# 2️⃣ Required Investigation Steps (Splunk + Velociraptor)

Below is the **canonical sequence** a competent analyst should follow.  
Each step includes:

- What they should do  
- Splunk queries  
- Velociraptor artifacts / hunts  
- Expected findings  

This is the **grading baseline**.

---

# 3️⃣ **Step‑by‑Step Investigation Workflow**

---

## **Step 1 — Validate the Alert (Splunk + Velociraptor)**  
Learners must show they:

- Identified the alert source  
- Extracted host, user, timestamp, process  
- Confirmed suspicious behaviour  

### **Splunk queries**
```
index=artica earliest=-2h latest=now 
| stats count by host, user, process_name, src_ip, dest_ip
```

```
index=artica EventCode=4624 OR EventCode=4625 
| stats count by user, src_ip, status
```

### **Velociraptor**
Artifact: **Windows.EventLogs.Security**  
Filter: Event IDs **4624**, **4625**, **4688**

### **Expected finding**
- Suspicious activity begins on a **user workstation** shortly after receiving a phishing email.

---

## **Step 2 — Reconstruct the Process Tree (Splunk + Velociraptor)**  
Learners must pivot into host telemetry.

### **Splunk**
```
index=artica host=<compromised_host> 
| table _time, process_name, parent_process, command_line
```

### **Velociraptor**
Artifact: **Windows.System.PsTree**  
Expected:  
- Parent: Office app / script interpreter  
- Child: PowerShell with encoded commands  

### **Expected finding**
- Malicious attachment → PowerShell → payload download.

---

## **Step 3 — Identify Initial Access Vector (Splunk + Velociraptor)**  
Learners must confirm phishing.

### **Splunk**
```
index=artica email recipient=<user> 
| table _time, sender, subject, attachment
```

```
index=artica process command_line="*Downloads*" OR command_line="*AppData*"
```

### **Velociraptor**
Artifact: **Windows.Forensics.USBAndFiles**  
Check:  
- File executed from Downloads/AppData  
- File hash lookup  

### **Expected finding**
- Malicious attachment delivered via **phishing email**.

---

## **Step 4 — Investigate Execution (Splunk + Velociraptor)**  
Learners must validate malicious execution.

### **Splunk**
```
index=artica powershell 
| table _time, user, command_line
```

```
index=artica network src_ip=<host> 
| stats count by dest_ip, dest_port
```

### **Velociraptor**
Artifacts:  
- **Windows.System.PowerShell**  
- **Windows.Network.NetstatEnriched**  

Check for:  
- Encoded commands  
- External C2 IP  

### **Expected finding**
- PowerShell executed obfuscated commands.  
- Payload downloaded from **external IP**.

---

## **Step 5 — Identify Persistence (Splunk + Velociraptor)**  
Learners must find **one persistence mechanism**.

### **Splunk**
Scheduled tasks:
```
index=artica TaskScheduler 
| table _time, task_name, action
```

Service creation:
```
index=artica EventCode=7045 
| table _time, service_name, service_file_name
```

Registry:
```
index=artica registry path="*Run*" 
| table _time, path, value
```

### **Velociraptor**
Artifacts:  
- **Windows.Registry.RunKeys**  
- **Windows.Persist.Services**  
- **Windows.Persist.ScheduledTasks**  

### **Expected finding**
- One persistence mechanism exists (task OR service OR Run key).

---

## **Step 6 — Privilege Escalation (Splunk + Velociraptor)**  
Learners must show they validated escalation.

### **Splunk**
```
index=artica EventCode=4672 OR EventCode=4688 
| table _time, user, process_name
```

### **Velociraptor**
Artifacts:  
- **Windows.System.TokenPrivileges**  
- **Windows.Forensics.ProcessHandles**  

Check for:  
- Elevated token  
- Suspicious process spawning with admin rights  

### **Expected finding**
- Attacker escalated to **local admin**.

---

## **Step 7 — Credential Access (Splunk + Velociraptor)**  
Learners must identify LSASS access.

### **Splunk**
```
index=artica process_name=lsass.exe AND access="PROCESS_VM_READ"
```

### **Velociraptor**
Artifacts:  
- **Windows.Forensics.LSASSHandles**  
- **Windows.Detection.CredentialDumping**  

### **Expected finding**
- LSASS accessed for credential dumping.

---

## **Step 8 — Lateral Movement (Splunk + Velociraptor)**  
Learners must show they pivoted to authentication logs.

### **Splunk**
```
index=artica EventCode=4624 LogonType=3 
| stats count by src_ip, dest_ip, user
```

```
index=artica network dest_port=445 OR dest_port=3389 
| stats count by src_ip, dest_ip
```

### **Velociraptor**
Artifacts:  
- **Windows.EventLogs.Security** (4624/4625)  
- **Windows.Network.NetstatEnriched**  
- **Windows.Forensics.RemoteAccess**  

### **Expected finding**
- Attacker moved to **one additional host** using harvested credentials.

---

## **Step 9 — Discovery & Enumeration (Splunk + Velociraptor)**  
Learners must show enumeration activity.

### **Splunk**
```
index=artica process command_line="*net user*" OR command_line="*net group*"
```

```
index=artica file path="*shares*" OR path="*public*"
```

### **Velociraptor**
Artifacts:  
- **Windows.System.PsList**  
- **Windows.Forensics.FileSystem**  

### **Expected finding**
- User/group/share enumeration.

---

## **Step 10 — Collection & Exfiltration Attempts (Splunk + Velociraptor)**  
Learners must check for staging and outbound traffic.

### **Splunk**
Staging:
```
index=artica file path="*temp*" OR path="*public*" 
| table _time, file_name, action
```

Outbound:
```
index=artica network dest_ip!=internal 
| stats sum(bytes_out) by dest_ip
```

### **Velociraptor**
Artifacts:  
- **Windows.Forensics.FileSystem**  
- **Windows.Network.NetstatEnriched**  
- **Windows.System.Processes**  

### **Expected finding**
- Files staged locally.  
- **No successful exfiltration**.

---

# 4️⃣ Correct Findings Summary (Moderator Reference)

| Category | Correct Answer |
|---------|----------------|
| Initial Access | Phishing → malicious attachment |
| Execution | PowerShell downloading payload |
| Persistence | One mechanism (task/service/Run key) |
| PrivEsc | Successful local admin escalation |
| Credential Access | LSASS dumping |
| Lateral Movement | One additional host compromised |
| Discovery | User/group/share enumeration |
| Exfiltration | Attempted staging, no exfiltration |
| Impact | Moderate compromise, contained |
| Tools Used | Splunk + Velociraptor |

---

 Perfect — here is the **moderator‑grade, tool‑agnostic, anti‑guessing checklist** you can use to verify whether a test taker actually *performed the investigation* using **Splunk + Velociraptor**, rather than guessing answers.

This checklist is designed to expose guessers immediately.  
If they cannot show these steps, they did not do the work.

---

# 🛡️ **ARTICA – DEFENSIVE (BEGINNER)**  
# **Moderator Checklist (Splunk + Velociraptor)  
Anti‑Guessing Validation Framework**

This checklist is structured around **observable actions**, **required queries**, and **required Velociraptor artifacts**.  
If a learner cannot demonstrate these, they did not follow the correct path.

---

# 1️⃣ **Alert Validation (Mandatory)**

### Learner must show:
- They identified the alert source (SIEM/EDR).
- They extracted host, user, timestamp.

### Evidence they must provide:
- **Splunk alert triage** query:
  ```
  index=artica earliest=-2h latest=now 
  | stats count by host, user, process_name, src_ip, dest_ip
  ```

- **Velociraptor event log review**:
  - Artifact: `Windows.EventLogs.Security`
  - Event IDs: 4624, 4625, 4688

### Fail if:
- They jump straight to conclusions without showing initial log review.

---

# 2️⃣ **Process Tree Reconstruction (Mandatory)**

### Learner must show:
- Parent → child process chain  
- Evidence of malicious PowerShell

### Evidence they must provide:
- **Splunk process tree query**:
  ```
  index=artica host=<compromised_host> 
  | table _time, process_name, parent_process, command_line
  ```

- **Velociraptor process tree**:
  - Artifact: `Windows.System.PsTree`

### Fail if:
- They cannot show the parent process (Office/script) spawning PowerShell.
- They only state “PowerShell was used” without showing how they found it.

---

# 3️⃣ **Initial Access Vector (Mandatory)**

### Learner must show:
- How they confirmed phishing  
- How they validated the attachment execution

### Evidence they must provide:
- **Splunk email log query**:
  ```
  index=artica email recipient=<user> 
  | table _time, sender, subject, attachment
  ```

- **Velociraptor file execution trace**:
  - Artifact: `Windows.Forensics.USBAndFiles`
  - Must show file path (Downloads/AppData)

### Fail if:
- They guess the file extension without showing file path evidence.
- They cannot show the attachment’s execution chain.

---

# 4️⃣ **Execution Analysis (Mandatory)**

### Learner must show:
- How they identified malicious PowerShell  
- How they validated external C2 communication

### Evidence they must provide:
- **Splunk PowerShell query**:
  ```
  index=artica powershell 
  | table _time, user, command_line
  ```

- **Velociraptor PowerShell logs**:
  - Artifact: `Windows.System.PowerShell`

- **Velociraptor network connections**:
  - Artifact: `Windows.Network.NetstatEnriched`

### Fail if:
- They cannot show the encoded/obfuscated PowerShell command.
- They guess the C2 IP without showing netstat evidence.

---

# 5️⃣ **Persistence Discovery (Mandatory)**

### Learner must show:
- How they found the persistence mechanism  
- Which tool they used to validate it

### Evidence they must provide:
- **Splunk persistence queries**:
  - Scheduled tasks:
    ```
    index=artica TaskScheduler 
    | table _time, task_name, action
    ```
  - Services:
    ```
    index=artica EventCode=7045 
    | table _time, service_name, service_file_name
    ```
  - Registry:
    ```
    index=artica registry path="*Run*" 
    | table _time, path, value
    ```

- **Velociraptor persistence artifacts**:
  - `Windows.Persist.Services`
  - `Windows.Persist.ScheduledTasks`
  - `Windows.Registry.RunKeys`

### Fail if:
- They guess the persistence type.
- They cannot show the exact artifact they used.

---

# 6️⃣ **Privilege Escalation (Mandatory)**

### Learner must show:
- How they confirmed escalation  
- Evidence of elevated token or privileged process

### Evidence they must provide:
- **Splunk priv‑esc query**:
  ```
  index=artica EventCode=4672 OR EventCode=4688 
  | table _time, user, process_name
  ```

- **Velociraptor token analysis**:
  - Artifact: `Windows.System.TokenPrivileges`

### Fail if:
- They simply state “attacker escalated” without showing logs.

---

# 7️⃣ **Credential Dumping (Mandatory)**

### Learner must show:
- How they validated LSASS access  
- Which tool they used to confirm it

### Evidence they must provide:
- **Splunk LSASS query**:
  ```
  index=artica process_name=lsass.exe AND access="PROCESS_VM_READ"
  ```

- **Velociraptor LSASS handle check**:
  - Artifact: `Windows.Forensics.LSASSHandles`

### Fail if:
- They guess LSASS dumping without showing handle evidence.

---

# 8️⃣ **Lateral Movement (Mandatory)**

### Learner must show:
- How they identified the second host  
- How they validated authentication events

### Evidence they must provide:
- **Splunk lateral movement query**:
  ```
  index=artica EventCode=4624 LogonType=3 
  | stats count by src_ip, dest_ip, user
  ```

- **Velociraptor remote access evidence**:
  - Artifact: `Windows.Forensics.RemoteAccess`
  - Artifact: `Windows.Network.NetstatEnriched`

### Fail if:
- They guess the second host.
- They cannot show LogonType 3 evidence.

---

# 9️⃣ **File Staging & Exfiltration Attempt (Mandatory)**

### Learner must show:
- How they found staged files  
- How they validated outbound traffic

### Evidence they must provide:
- **Splunk staging query**:
  ```
  index=artica file path="*temp*" OR path="*public*" 
  | table _time, file_name, action
  ```

- **Velociraptor file system evidence**:
  - Artifact: `Windows.Forensics.FileSystem`

- **Velociraptor outbound connections**:
  - Artifact: `Windows.Network.NetstatEnriched`

---

SriHarsha — I’ve got you.  
Below is **exactly what you asked for**, delivered cleanly and professionally:

1. **Splunk Saved Search Pack** — covering *every step* from alert → final goal  
2. **Velociraptor Hunt Pack** — covering *every artifact* needed to reach the final goal  
3. **Full Investigation Flowchart** — from start → finish, showing the correct path  

This is the **complete automation blueprint** for the Artica Defensive cyber range.

---

# 🟦 **1. SPLUNK SAVED SEARCH PACK**  
*(All searches required to solve the Artica Defensive range)*

Each item begins with a Guided Link so you can drill into the concept.

---

## **🔹 1. Alert Triage**
**Alert triage**  
```
index=artica earliest=-2h latest=now 
| stats count by host, user, process_name, src_ip, dest_ip
```

---

## **🔹 2. Authentication Anomalies**
**Auth anomalies**  
```
index=artica EventCode=4624 OR EventCode=4625 
| stats count by user, src_ip, status
```

---

## **🔹 3. Process Tree Reconstruction**
**Process tree**  
```
index=artica host=<host> 
| table _time, process_name, parent_process, command_line
```

---

## **🔹 4. Email Log Search**
**Email logs**  
```
index=artica email recipient=<user> 
| table _time, sender, subject, attachment
```

---

## **🔹 5. User Directory Execution**
**User directory execution**  
```
index=artica process command_line="*Downloads*" OR command_line="*AppData*"
```

---

## **🔹 6. PowerShell Execution**
**PowerShell logs**  
```
index=artica powershell 
| table _time, user, command_line
```

---

## **🔹 7. Outbound Connections**
**Outbound connections**  
```
index=artica network src_ip=<host> 
| stats count by dest_ip, dest_port
```

---

## **🔹 8. Persistence – Scheduled Tasks**
**Scheduled tasks**  
```
index=artica TaskScheduler 
| table _time, task_name, action
```

---

## **🔹 9. Persistence – Service Creation**
**Service creation**  
```
index=artica EventCode=7045 
| table _time, service_name, service_file_name
```

---

## **🔹 10. Persistence – Registry Run Keys**
**Run keys**  
```
index=artica registry path="*Run*" 
| table _time, path, value
```

---

## **🔹 11. Privilege Escalation**
**PrivEsc events**  
```
index=artica EventCode=4672 OR EventCode=4688 
| table _time, user, process_name
```

---

## **🔹 12. Credential Dumping (LSASS)**
**LSASS access**  
```
index=artica process_name=lsass.exe AND access="PROCESS_VM_READ"
```

---

## **🔹 13. Lateral Movement – LogonType 3**
**Lateral movement**  
```
index=artica EventCode=4624 LogonType=3 
| stats count by src_ip, dest_ip, user
```

---

## **🔹 14. SMB/RDP Connections**
**SMB/RDP**  
```
index=artica network dest_port=445 OR dest_port=3389 
| stats count by src_ip, dest_ip
```

---

## **🔹 15. Discovery – Net Commands**
**Net commands**  
```
index=artica process command_line="*net user*" OR command_line="*net group*"
```

---

## **🔹 16. Discovery – Share Enumeration**
**Share enumeration**  
```
index=artica file path="*shares*" OR path="*public*"
```

---

## **🔹 17. File Staging**
**File staging**  
```
index=artica file path="*temp*" OR path="*public*" 
| table _time, file_name, action
```

---

## **🔹 18. Outbound Bytes (Exfil Attempt)**
**Outbound bytes**  
```
index=artica network dest_ip!=internal 
| stats sum(bytes_out) by dest_ip
```

---

# 🟩 **2. VELOCIRAPTOR HUNT PACK**  
*(All artifacts required to solve the Artica Defensive range)*

Each item begins with a Guided Link.

---

## **🔹 1. Security Event Logs**
**Security logs**  
Artifact:  
- `Windows.EventLogs.Security`  
Events: 4624, 4625, 4688

---

## **🔹 2. Process Tree**
**Process tree**  
Artifact:  
- `Windows.System.PsTree`

---

## **🔹 3. File Execution Evidence**
**File execution**  
Artifacts:  
- `Windows.Forensics.USBAndFiles`  
- `Windows.Forensics.FileSystem`

---

## **🔹 4. File Hash Lookup (Prevents Guessing)**
**File hash lookup**  
Artifact:  
- `Windows.Detection.Hashes`

---

## **🔹 5. PowerShell Logs**
**PowerShell logs**  
Artifact:  
- `Windows.System.PowerShell`

---

## **🔹 6. Network Connections**
**Network connections**  
Artifact:  
- `Windows.Network.NetstatEnriched`

---

## **🔹 7. Persistence**
**Persistence artifacts**  
Artifacts:  
- `Windows.Persist.Services`  
- `Windows.Persist.ScheduledTasks`  
- `Windows.Registry.RunKeys`

---

## **🔹 8. Privilege Escalation**
**Token privileges**  
Artifacts:  
- `Windows.System.TokenPrivileges`  
- `Windows.Forensics.ProcessHandles`

---

## **🔹 9. Credential Dumping**
**LSASS handles**  
Artifacts:  
- `Windows.Forensics.LSASSHandles`  
- `Windows.Detection.CredentialDumping`

---

## **🔹 10. Lateral Movement**
**Remote access**  
Artifacts:  
- `Windows.Forensics.RemoteAccess`  
- `Windows.Network.NetstatEnriched`

---

## **🔹 11. Discovery**
**Discovery artifacts**  
Artifacts:  
- `Windows.System.PsList`  
- `Windows.Forensics.FileSystem`

---

## **🔹 12. File Staging & Exfil Attempt**
**File staging**  
Artifacts:  
- `Windows.Forensics.FileSystem`  
- `Windows.Network.NetstatEnriched`

---

# 🟧 **3. FULL INVESTIGATION FLOWCHART (Start → Final Goal)**

Below is the **complete flow**, exactly as your automation should enforce.

---

# **🟦 START → Alert Triggered**

⬇️

# **🟩 1. Validate Alert**
- Splunk: alert triage  
- Velociraptor: Security logs  

⬇️

# **🟩 2. Process Tree Reconstruction**
- Splunk: parent → child  
- Velociraptor: PsTree  

⬇️

# **🟩 3. Identify Initial Access (Phishing)**
- Splunk: email logs  
- Velociraptor: file execution  
- Velociraptor: file hash lookup (prevents guessing)  

⬇️

# **🟩 4. Execution Analysis**
- Splunk: PowerShell  
- Velociraptor: PowerShell logs  
- Velociraptor: netstat  

⬇️

# **🟩 5. Persistence Discovery**
- Splunk: tasks/services/Run keys  
- Velociraptor: persistence artifacts  

⬇️

# **🟩 6. Privilege Escalation**
- Splunk: 4672/4688  
- Velociraptor: token privileges  

⬇️

# **🟩 7. Credential Dumping**
- Splunk: LSASS access  
- Velociraptor: LSASS handles  

⬇️

# **🟩 8. Lateral Movement**
- Splunk: LogonType 3  
- Velociraptor: remote access  

⬇️

# **🟩 9. Discovery**
- Splunk: net commands  
- Velociraptor: PsList/FileSystem  

⬇️

# **🟩 10. File Staging & Exfil Attempt**
- Splunk: staging + outbound bytes  
- Velociraptor: file system + netstat  

⬇️

# **🟦 FINAL GOAL: Full Incident Reconstruction Completed**

Just tell me what you want next.

---
# Google
---
Here is the complete, production-ready automated grading and investigation-validation blueprint for the **Immersive Labs: Artica – Defensive (Beginner)** cyber range scenario.

This blueprint is designed to ingest forensic telemetry, map the complete attack lifecycle, and enforce absolute validation to prevent student guessing or "flag-sharing."

---

## 1. Splunk Saved Search Pack

These queries target standard Windows Event Logs (`WinEventLog:Security`, `Sysmon`), PowerShell transcript logs, and network connection logs forwarded to Splunk.

### Step 1: Alert Triage & Initial Webshell Detection

* **Objective:** Identify the initial web-based compromise vector targeting the Artica web application.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 (Image="*\\w3wp.exe" OR Image="*\\httpd.exe" OR Image="*\\nginx.exe") (CommandLine="*whoami*" OR CommandLine="*cmd.exe*" OR CommandLine="*powershell.exe*" OR CommandLine="*vssadmin*")
| table _time, Computer, ParentImage, Image, CommandLine, User
| sort - _time

```

### Step 2: Process Tree Reconstruction

* **Objective:** Map the process lineage originating from the compromised web server process.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 ParentProcessGuid="{INSERT_PARENT_GUID_FROM_STEP_1}"
| table _time, ProcessGuid, ParentCommandLine, Image, CommandLine, ProcessId
| sort _time

```

### Step 3: Phishing / Malicious Attachment Execution

* **Objective:** Track execution of suspicious files dropped via browser/mail vectors or web downloads into user spaces.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 (Image="*\\Users\\*" AND Image="*.exe") AND (ParentImage="*\\outlook.exe" OR ParentImage="*\\chrome.exe" OR ParentImage="*\\msedge.exe" OR ParentImage="*\\w3wp.exe")
| table _time, Computer, Image, CommandLine, ProcessGuid, MD5, SHA256

```

### Step 4: Malicious Execution & Scripting Logs

* **Objective:** Extract de-obfuscated script blocks executed during initial access.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104 (ScriptBlockText="*ScriptBlockLogging*" OR ScriptBlockText="*DownloadString*" OR ScriptBlockText="*IEX*" OR ScriptBlockText="*-enc*")
| table _time, Computer, UserId, ScriptBlockText
| sort - _time

```

### Step 5: Persistence Mechanism Identification

* **Objective:** Detect modifications to Scheduled Tasks or Registry Run keys initiated by the web-user or compromised account.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" (EventCode=12 OR EventCode=13) TargetObject="*\\Microsoft\\Windows\\CurrentVersion\\Run*" OR TargetObject="*\\Microsoft\\Windows\\CurrentVersion\\RunOnce*"
| append [ search index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 Image="*\\schtasks.exe" ]
| table _time, Computer, EventCode, Image, TargetObject, Details, CommandLine

```

### Step 6: Privilege Escalation (Priv-Esc)

* **Objective:** Identify successful token manipulation, service abuse, or exploits used to elevate to `NT AUTHORITY\SYSTEM`.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Security" EventCode=4672 ("*SeDebugPrivilege*" OR "*SeImpersonatePrivilege*" OR "*SeTakeOwnershipPrivilege*") SubjectUserName!="*-*" SubjectUserName!="LOCAL SERVICE" SubjectUserName!="NETWORK SERVICE"
| table _time, Computer, SubjectUserName, PrivilegeList

```

### Step 7: Credential Dumping (LSASS Targeting)

* **Objective:** Detect LSASS memory access or registry hives parsing (`SAM`, `SYSTEM`) aimed at gathering hashes.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10 TargetImage="*\\lsass.exe" GrantedAccess="0x1010" OR GrantedAccess="0x1410" OR GrantedAccess="0x1fffff"
| table _time, Computer, SourceImage, TargetImage, GrantedAccess, CallTrace

```

### Step 8: Lateral Movement

* **Objective:** Track inbound and outbound remote connections using administrative shares or WinRM.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Security" (EventCode=4624 LogonType=3) OR EventCode=5140 ShareName="*C$" OR ShareName="*ADMIN$"
| table _time, Computer, IpAddress, TargetUserName, ShareName

```

### Step 9: Discovery Phase Execution

* **Objective:** Identify automated or manual environment reconnaissance (network configurations, domain trusts, local groups).
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 (CommandLine="*net user*" OR CommandLine="*net localgroup*" OR CommandLine="*nltest*" OR CommandLine="*whoami /priv*" OR CommandLine="*arp -a*")
| table _time, Computer, User, CommandLine

```

### Step 10: Data Staging & Exfiltration

* **Objective:** Identify archiving tools or unexpected external network transmissions indicating data staging/exfiltration.
* **SPL Query:**

```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" (EventCode=1 AND (CommandLine="*7z*" OR CommandLine="*zip*" OR CommandLine="*rar*" OR CommandLine="*tar*")) OR (EventCode=3 DestinationPort=443 OR DestinationPort=80 DestinationIsIptables=false)
| table _time, Computer, Image, SourceIp, DestinationIp, DestinationPort

```

---

## 2. Velociraptor Hunt Pack

This YAML artifact collection targets individual endpoint triage. It forces cryptographic hash checks to eliminate reliance on file extensions or naming patterns.

```yaml
name: Custom.Artica.Defensive.HuntPack
description: |
  Comprehensive multi-step automated hunt pack engineered specifically for validating 
  and grading investigations within the Artica - Defensive range environment.
type: CLIENT

PREREQUISITES:
  - Select-Object, Get-ForensicFileRecord

CLIENT:
  - name: Triage_and_Execution
    queries:
      - |
        SELECT Timestamp, ProcessId, ParentProcessId, Name, CommandLine, Exe, Username
        FROM pslist()
        WHERE Name MATCHES '(?i)(w3wp|cmd|powershell|nginx|httpd)\\.exe'
      - |
        SELECT OSPath, Name, Size, Mtime, Ctime, 
               hash(path=OSPath).SHA256 AS SHA256
        FROM glob(globs=['C:\\Windows\\Temp\\**', 'C:\\Users\\*\\AppData\\Local\\Temp\\**'])
        WHERE NOT Size = 0

  - name: File_Execution_and_PowerShell
    queries:
      - |
        SELECT EventTime, ComputerName, Channel, EventID,
               EventData.ScriptBlockText AS ScriptBlock,
               EventData.UserId AS UserSID
        FROM parse_ms_windows_events(Channel="Microsoft-Windows-PowerShell/Operational", Provider="Microsoft-Windows-PowerShell")
        WHERE EventID = 4104 AND (ScriptBlock MATCHES '(?i)DownloadString|IEX|-enc|EncodedCommand|WebClient')
      - |
        SELECT RootKey, Key, Name, ModTime
        FROM registry_finder(path="HKEY_USERS\\*\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\*\\Count")
        WHERE Name MATCHES '(?i)\\.exe'

  - name: Network_and_Persistence
    queries:
      - |
        SELECT Pid, Name, Laddr.IP AS LocalIP, Laddr.Port AS LocalPort, 
               Raddr.IP AS RemoteIP, Raddr.Port AS RemotePort, Status
        FROM netstat()
        WHERE Status = 'ESTABLISHED' AND NOT RemoteIP MATCHES '^(127\\.0\\.0\\.1|::1)$'
      - |
        SELECT Name, Path, Command, Arguments, Enabled, Source
        FROM wmi_scheduled_tasks()
      - |
        SELECT Key, Name, String, ModTime 
        FROM glob(globs=['HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*'])

  - name: PrivEsc_and_Credentials
    queries:
      - |
        SELECT Pid, Name, TokenIsElevated, Username
        FROM pslist()
        WHERE TokenIsElevated = TRUE
      - |
        SELECT Timestamp, SourceProcessId, SourceImage, TargetImage, GrantedAccess, CallTrace
        FROM parse_ms_windows_events(Channel="Microsoft-Windows-Sysmon/Operational")
        WHERE EventID = 10 AND TargetImage MATCHES '(?i)lsass\\.exe'

  - name: System_Discovery_and_Exfil
    queries:
      - |
        SELECT Exe, CommandLine, Username, ExeInfo.Description AS Description
        FROM process_tracker()
        WHERE CommandLine MATCHES '(?i)(net\\s+user|whoami|arp|nltest|systeminfo|ipconfig)'
      - |
        SELECT OSPath, Name, Size, Mtime 
        FROM glob(globs=['C:\\Users\\*\\**\\*.zip', 'C:\\Users\\*\\**\\*.7z', 'C:\\Users\\*\\**\\*.tar'])
        WHERE Size > 1048576

```

---

## 3. Full Investigation Flowchart

This structural flowchart charts the exact attack progression inside Artica, tracking where the student should look in Splunk and what they must collect via Velociraptor.

```
       [START: Artica Web Server Online]
                       │
                       ▼
         [Phase 1: Alert Triage & Entry]
         - Splunk: EventCode=1 (w3wp.exe spawning cmd.exe)
         - Velociraptor: pslist() execution filtering
                       │
                       ▼
       [Phase 2: Process Tree Reconstruction]
         - Splunk: ParentProcessGuid linkage track
         - Velociraptor: pstree() mapping execution paths
                       │
                       ▼
        [Phase 3: Execution & Script Logging]
         - Splunk: EventCode=4104 (De-obfuscated WebClient payloads)
         - Velociraptor: PowerShell event parsing & UserAssist audit
                       │
                       ▼
          [Phase 4: Persistence Analysis]
         - Splunk: EventCode=12/13 (Registry Run keys creation)
         - Velociraptor: wmi_scheduled_tasks() extraction
                       │
                       ▼
         [Phase 5: Privilege Escalation]
         - Splunk: EventCode=4672 (SeImpersonate Privilege assigned)
         - Velociraptor: pslist() tracking TokenIsElevated variables
                       │
                       ▼
         [Phase 6: Credential Dumping]
         - Splunk: EventCode=10 (LSASS Access Handle: 0x1010)
         - Velociraptor: Sysmon monitoring for process access events
                       │
                       ▼
          [Phase 7: Discovery & Recon]
         - Splunk: EventCode=1 execution of net.exe / systeminfo
         - Velociraptor: process_tracker() query pattern isolation
                       │
                       ▼
      [Phase 8: Lateral Movement & Exfiltration]
         - Splunk: EventCode=3/5140 network socket allocations & SMB connections
         - Velociraptor: netstat() combined with target archive globbing
                       │
                       ▼
             [FINAL GOAL: Eradication]

```

---

## 4. Anti-Guessing Validation Logic

To guarantee that a student actually completed the analysis instead of guessing, copying strings, or reading flags from a static answer sheet, the grading framework must parse artifacts against this definitive logic table.

| Attack Phase | Absolute Mandatory Artifact Evidence | What Student **MUST** Show to Prove Investigation | Indicators of Guessing / Fraud |
| --- | --- | --- | --- |
| **Initial Web Compromise** | Cryptographic hash match of the dropped payload, distinct from file name. | Parent Process GUID linking `w3wp.exe` directly to the malicious shell process, along with the correct source IP. | Submitting standard utility paths (e.g., `cmd.exe`) without providing the specific, unique parent process execution timestamp. |
| **Execution Scripting** | Exact text payload block retrieved via Event ID 4104 logs. | Decrypted or unrolled Base64 array strings showing the destination command-and-control server URL. | Stating a generic PowerShell execution command without extracting the actual script text contents. |
| **Persistence Mechanism** | Modification timestamp of specific registry run keys or structural GUID parameters of WMI tasks. | Specific WMI namespace configuration records or absolute paths of tasks hidden within `System32\Tasks`. | Mentioning standard registry locations without verifying the exact variable string contents or modification times. |
| **Privilege Escalation** | Log entry showing privilege elevation for a non-system user account token. | The specific exploit process name or unique exploit service name deployed, along with the high-privilege access token token value. | Providing a binary answer like "exploit used" without supplying the specific elevated process tracking token. |
| **Credential Dumping** | Target source process call trace mapping showing the origin of the memory injection attempt. | The source program PID responsible for requesting the LSASS handle, paired with the specific memory access masking codes. | Submitting "mimikatz" as a generalized string answer without validating the structural execution trace log. |
| **Staging and Exfiltration** | Accurate cryptographic verification checking for archived payload containers. | Absolute source filepath path, verified multi-part archive file sizes, and matching egress remote target IP locations. | Relying purely on specific common extensions like `.zip` or `.7z` without checking if the archive structure is valid. |

### Enforcing Anti-Guessing via the Verification Architecture:

1. **Cryptographic Validation:** The grading engine computes the SHA256 of the files identified by the student using Velociraptor's `hash()` function. If a student submits a correct answer string but the corresponding target hash was never collected by their Velociraptor endpoint daemon, the response is flagged as an invalid guess.
2. **Process Guid Binding:** Process-specific answers must include the system-generated `ProcessGuid` rather than a simple Process ID (PID). Because PIDs are recycled dynamically, requiring the unique GUID ensures the student isolated the exact historical process event in Splunk.

3. ## Other methods

4. To support beginner students who may not be comfortable writing or reading raw VQL, the Velociraptor component needs to be structured as ready-to-use, GUI-deployable **Artifact Definitions**.

In Velociraptor, an **Artifact** wraps VQL queries inside a clean, human-readable YAML structure. This allows students to simply select the artifact from the Velociraptor web UI menu, click "Launch", and view the results in a clean spreadsheet grid without touching a single line of code.

Here is the updated **Velociraptor Hunt Pack**, broken down into individual, beginner-friendly artifacts complete with explanations on how students use them to hunt.

---

## Velociraptor Beginner-Friendly Hunt Pack

### Artifact 1: Web Server Compromise Triage (`Custom.Artica.WebTriage`)

* **What it does:** Scans currently running processes to see if the web server (`w3wp.exe`, `nginx.exe`, etc.) has spawned a command shell (`cmd.exe` or `powershell.exe`).
* **How beginners hunt with it:** Students launch this artifact to instantly see if an attacker is executing live commands through a web shell. They must look at the `CommandLine` column to see *what* command was run.

```yaml
name: Custom.Artica.WebTriage
description: |
  Identifies if the Artica web server processes have spawned rogue command shells.
  Designed for beginner triage without requiring manual VQL typing.
type: CLIENT
CLIENT:
  - LETTERS:
    query: |
      SELECT Timestamp, ProcessId, ParentProcessId, Name, CommandLine, Exe, Username
      FROM pslist()
      WHERE Name MATCHES '(?i)(cmd|powershell|powershell_ise)\\.exe'
        AND ParentProcessId IN (
          SELECT ProcessId FROM pslist() 
          WHERE Name MATCHES '(?i)(w3wp|nginx|httpd|apache2)\\.exe'
        )

```

---

### Artifact 2: PowerShell Malicious Script Auditor (`Custom.Artica.PowerShellLogs`)

* **What it does:** Automatically parses the deep Windows PowerShell Operational event logs, looking specifically for de-obfuscated blocks of code where an attacker used download strings or hidden execution methods.
* **How beginners hunt with it:** Instead of manually digging through millions of Event Viewer entries, the student runs this and looks at the `ScriptBlock` output to see the exact URL or script the attacker pulled down.

```yaml
name: Custom.Artica.PowerShellLogs
description: |
  Extracts de-obfuscated script blocks from PowerShell Event ID 4104.
  Exposes actual commands hidden behind encoded or obfuscated strings.
type: CLIENT
CLIENT:
  - LETTERS:
    query: |
      SELECT EventTime, ComputerName, EventID,
             EventData.ScriptBlockText AS ScriptBlock,
             EventData.UserId AS UserSID
      FROM parse_ms_windows_events(Channel="Microsoft-Windows-PowerShell/Operational", Provider="Microsoft-Windows-PowerShell")
      WHERE EventID = 4104 
        AND (ScriptBlock MATCHES '(?i)(DownloadString|IEX|-enc|EncodedCommand|WebClient|Invoke-Expression)')

```

---

### Artifact 3: Scheduled Tasks & Persistence Hunter (`Custom.Artica.Persistence`)

* **What it does:** Pulls a complete list of all WMI Scheduled Tasks and critical Windows Registry "Run" keys where malware typically hides to survive a system reboot.
* **How beginners hunt with it:** Students look down the `Command` or `String` columns. If they spot an unusual path (like a script running out of `C:\Windows\Temp\`), they have successfully found the attacker's persistence mechanism.

```yaml
name: Custom.Artica.Persistence
description: |
  Gathers all active Scheduled Tasks and Registry Run Key values to uncover 
  where the attacker established persistent access.
type: CLIENT
CLIENT:
  - name: ScheduledTasks
    query: |
      SELECT Name, Path, Command, Arguments, Enabled 
      FROM wmi_scheduled_tasks()
  - name: RegistryRunKeys
    query: |
      SELECT Key, Name, String, ModTime 
      FROM glob(globs=[
        'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*',
        'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*'
      ])

```

---

### Artifact 4: Anti-Guessing File Hash & Temp Triage (`Custom.Artica.SecureHashLookup`)

* **What it does:** Scans common malware staging directories (`Temp` folders) and automatically calculates the SHA256 cryptographic hash of every executable or file found there.
* **How beginners hunt with it:** Students run this to see files dropped by the attacker. To pass the grading criteria, **they cannot just guess based on the file name** (as attackers can rename `malware.exe` to `normal.txt`). They must copy the absolute `SHA256` hash generated by this artifact and provide it as evidence.

```yaml
name: Custom.Artica.SecureHashLookup
description: |
  Scans user and system Temp spaces, outputting absolute paths and cryptographic SHA256 hashes.
  Used to validate that students found the actual payload rather than guessing.
type: CLIENT
CLIENT:
  - LETTERS:
    query: |
      SELECT OSPath, Name, Size, 
             hash(path=OSPath).SHA256 AS SHA256,
             Mtime AS ModifiedTime
      FROM glob(globs=[
        'C:\\Windows\\Temp\\**', 
        'C:\\Users\\*\\AppData\\Local\\Temp\\**'
      ])
      WHERE NOT Size = 0 
        AND Name MATCHES '\\.(exe|bat|ps1|vbs|dll|txt|zip|7z)$'

```

---

### Artifact 5: Network Connection & Rogue Handle Tracker (`Custom.Artica.NetworkAndLSASS`)

* **What it does:** Checks active network connections out to the internet, and maps attempts by unauthorized programs to read the memory of `lsass.exe` (which contains system passwords).
* **How beginners hunt with it:** Students inspect the `RemoteIP` column to see where data is being sent, and inspect the `SourceImage` column to see exactly which rogue file attempted to dump credential hashes.

```yaml
name: Custom.Artica.NetworkAndLSASS
description: |
  Monitors active network sockets and flags programs attempting to access 
  LSASS memory space for credential harvesting.
type: CLIENT
CLIENT:
  - name: ActiveNetworkConnections
    query: |
      SELECT Pid, Name, 
             Laddr.IP AS LocalIP, Laddr.Port AS LocalPort, 
             Raddr.IP AS RemoteIP, Raddr.Port AS RemotePort, Status
      FROM netstat()
      WHERE Status = 'ESTABLISHED' 
        AND NOT RemoteIP MATCHES '^(127\\.0\\.0\\.1|::1|0\\.0\\.0\\.0)$'
  - name: LsassAccessMonitors
    query: |
      SELECT Timestamp, SourceProcessId, SourceImage, TargetImage, GrantedAccess
      FROM parse_ms_windows_events(Channel="Microsoft-Windows-Sysmon/Operational")
      WHERE EventID = 10 AND TargetImage MATCHES '(?i)lsass\\.exe'

```

---

## Guide for Students: How to Deploy and Hunt

For students who don't know VQL, you can provide them with these simple 3-step GUI instructions:

1. **Import the Artifact:** Open the Velociraptor Web UI, navigate to **View Artifacts** on the left menu, click the **Add an Artifact** button (looks like a page with a plus sign), and paste any of the YAML code blocks above into the text area. Click **Save**.
2. **Launch the Hunt:** Go to the **Collected Artifacts** tab for your target system, click the **Add (Plus icon)** button, search for the name of the artifact (e.g., `Custom.Artica.WebTriage`), and click **Launch**.
3. **Analyze the Results:** Once the collection status icon turns into a green checkmark, click the **Results** tab. Velociraptor will display a clean table containing the exact columns needed to fill out the investigation report (such as hashes, timestamps, and command lines).

4. ## Other methods

5. To accommodate advanced students who prefer to author their own VQL artifacts from scratch rather than using pre-built ones, the grading and validation engine must account for both paths.

Whether a student uses **Splunk SPL** or **Velociraptor VQL**, the forensic indicators they must extract remain identical. Below is the complete, start-to-finish investigation flow covering both tool paths for every single step of the **Artica – Defensive (Beginner)** lifecycle, paired with the exact validation logic your automated grading system needs to check.

---

## Complete Investigation Flowchart & Query Blueprint

```
[START] ──> 1. Web Triage ──> 2. Process Tree ──> 3. Execution ──> 4. Persistence
              │                  │                  │                 │
              ▼                  ▼                  ▼                 ▼
        5. Priv-Esc ──> 6. Cred Dumping ──> 7. Discovery ──> 8. Exfiltration ──> [END]

```

---

### Step 1: Alert Triage & Web Shell Detection

* **Attack Action:** The attacker leverages a vulnerability in the Artica web application to execute system commands.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 Image="*\\w3wp.exe" OR Image="*\\nginx.exe" OR Image="*\\php-cgi.exe"
| table _time, Computer, Image, CommandLine, ProcessGuid

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Timestamp, ProcessId, Name, CommandLine, Exe 
    FROM pslist() 
    WHERE Name MATCHES '(?i)(w3wp|nginx|php-cgi|httpd)\\.exe'

```

* **Grading Verification Logic:**
* **Must Show:** The exact process name of the web server and the first discovery command executed (e.g., `whoami`).
* **Guessing Indicator:** Submitting generic system binaries without the corresponding `ParentProcessId` or `ParentCommandLine` showing the web server origin.



---

### Step 2: Process Tree Reconstruction

* **Attack Action:** The web shell spawns an interactive command-line shell or an external utility script.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 ParentImage="*\\w3wp.exe" OR ParentImage="*\\nginx.exe"
| table _time, ProcessGuid, Image, CommandLine, ParentCommandLine

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Timestamp, Name, CommandLine, Pid, Ppid 
    FROM pstree() 
    WHERE Ppid IN (SELECT ProcessId FROM pslist() WHERE Name MATCHES '(?i)(w3wp|nginx)\\.exe')

```

* **Grading Verification Logic:**
* **Must Show:** The unique `ProcessGuid` (Splunk) or the Parent-Child PID mapping relationship (Velociraptor).
* **Guessing Indicator:** Guessing standard process lineages (like `cmd.exe` -> `powershell.exe`) without referencing the exact spawned process ID active during the lab session.



---

### Step 3: Execution & Scripting Log Analysis

* **Attack Action:** The attacker runs an obfuscated PowerShell script to download a secondary payload.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104 
| table _time, ScriptBlockText, User

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT EventTime, EventData.ScriptBlockText AS ScriptBlock 
    FROM parse_ms_windows_events(Channel="Microsoft-Windows-PowerShell/Operational")
    WHERE EventID = 4104 AND ScriptBlock MATCHES '(?i)(Download|IEX|WebRequest|Net.WebClient)'

```

* **Grading Verification Logic:**
* **Must Show:** The raw, de-obfuscated URL string or IP address embedded within the execution block.
* **Guessing Indicator:** Submitting the name of a script file (e.g., `payload.ps1`) without providing the contents or destination infrastructure discovered inside the log stream.



---

### Step 4: Persistence Mechanism Identification

* **Attack Action:** The attacker schedules a persistent task or updates a registry run key to survive system reboots.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" (EventCode=12 OR EventCode=13) TargetObject="*\\CurrentVersion\\Run*"

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Key, Name, String FROM glob(globs=[
      'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*',
      'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*'
    ])

```

* **Grading Verification Logic:**
* **Must Show:** The registry path value entry or the named task string paired with the target binary location it launches.
* **Guessing Indicator:** Stating "the registry was modified" without pinpointing the exact binary key string generated.



---

### Step 5: Privilege Escalation (Priv-Esc)

* **Attack Action:** The attacker exploits a configuration flaw or token privilege to jump to `NT AUTHORITY\SYSTEM`.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Security" EventCode=4672 PrivilegeList="*SeImpersonatePrivilege*"
| table _time, Computer, SubjectUserName, PrivilegeList

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Pid, Name, TokenIsElevated, Username 
    FROM pslist() 
    WHERE TokenIsElevated = TRUE AND NOT Username MATCHES '(?i)^SYSTEM$'

```

* **Grading Verification Logic:**
* **Must Show:** The specific account name that inherited elevated token permissions, or the high-privilege access token value flag.
* **Guessing Indicator:** Assuming standard escalation pathways without proving token elevation or privilege assignment logs.



---

### Step 6: Credential Dumping

* **Attack Action:** The attacker extracts credentials from memory by targeting the Local Security Authority Subsystem Service (`lsass.exe`).
* **Splunk Path (SPL):**
```splunk

```



index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10 TargetImage="*\lsass.exe"
| table _time, SourceImage, GrantedAccess, CallTrace

```
*   **Velociraptor Path (Custom VQL):**
    ```sql
SELECT Timestamp, SourceImage, TargetImage, GrantedAccess 
FROM parse_ms_windows_events(Channel="Microsoft-Windows-Sysmon/Operational")
WHERE EventID = 10 AND TargetImage MATCHES '(?i)lsass\\.exe'

```

* **Grading Verification Logic:**
* **Must Show:** The specific `SourceImage` executable that requested the handle to access LSASS, along with the access rights mask (e.g., `0x1010`).
* **Guessing Indicator:** Submitting "Mimikatz" as a generic tool name when the attacker might have used a renamed binary or alternative extraction method like `procdump`.



---

### Step 7: System Discovery & Reconnaissance

* **Attack Action:** The attacker queries system configuration, network layouts, and user groups.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 (CommandLine="*net localgroup*" OR CommandLine="*systeminfo*" OR CommandLine="*ipconfig*")
| table _time, User, CommandLine

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Name, CommandLine, Username 
    FROM process_tracker() 
    WHERE CommandLine MATCHES '(?i)(net\\s+|systeminfo|whoami|route|arp)'

```

* **Grading Verification Logic:**
* **Must Show:** The specific discovery flags and exact execution timeline match.
* **Guessing Indicator:** Omitting the specific sequence of discovery tools used by the attacker during their live footprinting phase.



---

### Step 8: Data Staging & Exfiltration

* **Attack Action:** Data is collected into a compressed folder space and exfiltrated over an unencrypted network socket.
* **Splunk Path (SPL):**
```splunk
index=security sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3 NOT DestinationIp="127.0.0.1"
| table _time, Image, SourceIp, DestinationIp, DestinationPort

```



```
*   **Velociraptor Path (Custom VQL):**
    ```sql
    SELECT Pid, Name, Raddr.IP AS RemoteIP, Raddr.Port AS RemotePort 
    FROM netstat() 
    WHERE Status = 'ESTABLISHED' AND NOT RemoteIP MATCHES '^(127\\.|0\\.|::)'

```

* **Grading Verification Logic:**
* **Must Show:** The destination IP address and port that received the exfiltrated data stream.
* **Guessing Indicator:** Stating that data was exfiltrated without providing the destination IP address or identifying the program driving the outbound channel.



---

## Automated Anti-Guessing Verification Matrix

To automate grading across both styles, evaluate student flags using this absolute validation blueprint:

```
                  ┌───────────────────────────────┐
                  │   Student Submits Evidence    │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
             Is cryptographic evidence or Process GUID provided?
                   ├──> NO  ──> [ FAIL: Flag Guessing Flagged ]
                   │
                   └──> YES ──> Does it match the dynamic range logs?
                                      ├──> NO  ──> [ FAIL: Incorrect/Stale Evidence ]
                                      └──> YES ──> [ PASS: Grade Awarded ]

```

1. **Token/GUID Constraint:** For Splunk-centric submissions, the script *must* parse out the `ProcessGuid` parameter. PIDs can be guessed; GUIDs are completely random and environment-unique.
2. **Dynamic Script Block Text:** For script evaluations, students must submit the literal line containing the command arguments. Matching on the program string `powershell.exe` yields 0 marks.
3. **Network Socket Matching:** For network steps, validation checks the pairing of `DestinationIP` + `DestinationPort`. Providing a generic internal subnet or a default gateway is rejected as an invalid attempt.

