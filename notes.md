
# Role & Context
You are an expert Cybersecurity Knowledge Architect, Senior Python Developer, and Principal Red Team Engineer. I am completely overhauling my disorganized Obsidian vault to serve as my definitive, lifelong "Second Brain" for penetration testing, red team engagements, home labs, work projects, and elite certifications (OSCP, CPTS, OSCE, etc.). 

My current vault consists of unfiltered, raw, duplicated, and partially outdated notes and images compiled from various courses, online labs, and hands-on practice. 

# Environment & Assets
- **OS**: Windows (Local Obsidian Vault)
- **Tooling**: A long-context LLM paired with a local Python script to process and structure my vault.
- **Current State**: I have consolidated my messy, disparate files into a single, massive consolidated markdown file to maximize LLM context efficiency. 
- **Media**: The vault includes local image attachments requiring processing.

# The Ask
I have an existing Python script that handles my local note consolidation, and the internal system prompt for the LLM is embedded directly inside this code. I need you to:
1. Analyze my script for gaps, bugs, or architectural weaknesses on Windows.
2. Review the embedded system prompt inside the script to ensure it aligns perfectly with my goals (lifelong learning, high-level certs, and real-world operations).
3. Deliver the multi-phase execution strategy outlined below, updating my script and its internal prompt based on your code review.

---

# Execution Plan Tasks & Expectations

Please process my raw data and provide a comprehensive blueprint and execution strategy divided into the following phases:

## Phase 1: Ultimate Cybersecurity Taxonomy & Architecture
Propose a comprehensive, future-proof Obsidian folder structure. Do not just cluster roughly; design a strict hierarchical taxonomy optimized for quick navigation during exams or active engagements. It must natively support:
- Offensive Methodologies (Recon, Initial Access, Enumeration, Exploitation, Lateral Movement, Exfiltration).
- Environments (Active Directory, Windows, Linux, Cloud - AWS/Azure, Web Apps, API).
- Target Playbooks (OSCP-style standalone hosts vs. CPTS/OSCE-style enterprise AD environments).
- Professional Operations (Reporting templates, lab write-ups, work projects, tool cheat sheets).

## Phase 2: Content Optimization, Curation & De-confliction
Explain your precise strategy for cleansing the consolidated text file when I feed it to you. Detail how you will:
- Identify and eliminate exact or semantic duplicates.
- Detect deprecated techniques or legacy tools (e.g., outdated Exploit-DB scripts, old SMB exploits) and update them with modern alternatives (e.g., crackmapexec vs. netexec, modern impacket syntax).
- Fact-check technical syntax and commands to eliminate errors.

## Phase 3: Media Pipeline & Script Optimization (Windows)
Based on your review of my provided Python script and its embedded prompt, deliver an optimized, production-grade version that runs natively on Windows. The script must be enhanced to:
1. Parse my local vault and identify embedded images within notes.
2. Perform OCR text extraction and generate smart, contextual auto-captions/descriptions for those images.
3. Append this textual data directly below the image link in the markdown file so it becomes searchable within Obsidian.
4. Optimize the internal system prompt embedded in the code based on your Phase 2 analysis.

## Phase 4: Data Migration & Vault Hygiene Strategy
- Detail exactly what I should do with my legacy source files once the consolidated file is organized (e.g., archiving schemas, verifying file hashes, or safe deletion protocols).
- Provide a strict framework or template for how I should write new notes moving forward so that they seamlessly fit into this system without re-introducing clutter.

---

# Input for Your Review

## My Python Script (Including Embedded System Prompt):
```python
# PASTE YOUR ENTIRE PYTHON SCRIPT HERE
```



--------------

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║         CyberSec Vault Rebuild — Claude API Script               ║
║  Platform : Windows                                              ║
║  Model    : claude-sonnet-4-6                                    ║
║  Features : Resume | Rate Limiting | OCR+Captioning |            ║
║             Auto-Classification | Cost Estimation |              ║
║             Dry Run | Retry Failed | Progress Tracking           ║
╚══════════════════════════════════════════════════════════════════╝

SETUP:
    pip install anthropic
    set ANTHROPIC_API_KEY=your_key_here

USAGE:
    python vault_rebuild.py --estimate-cost          # check cost before running
    python vault_rebuild.py --dry-run --limit 5      # test on 5 files, no API calls
    python vault_rebuild.py --limit 20               # test live on 20 files
    python vault_rebuild.py                          # full run
    python vault_rebuild.py --retry-failed           # retry any failed files
"""

import os
import re
import json
import time
import base64
import argparse
import sys
from pathlib import Path
from anthropic import Anthropic

# ══════════════════════════════════════════════════════════════════
#  CONFIGURATION — EDIT THESE TWO PATHS BEFORE RUNNING
# ══════════════════════════════════════════════════════════════════

VAULT_IN  = Path(r"D:\keys_vault\obsidian\sri_obsidian\certifications\cybersecurity\hacker_blueprint")
VAULT_OUT = Path(r"D:\keys_vault\obsidian\sri_obsidian\certifications\cybersecurity\hacker_blueprint_rebuilt")

# ══════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════

STATE_FILE     = Path("rewrite_state.jsonl")
LOG_FILE       = Path("rewrite_log.txt")
MODEL          = "claude-sonnet-4-6"
MAX_TOKENS     = 4000
MAX_CHARS      = 15000
RETRY_WAIT     = 60
MAX_RETRIES    = 3
SUPPORTED_IMGS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# Cost per million tokens (Sonnet 4.6)
COST_INPUT_PER_M  = 3.00
COST_OUTPUT_PER_M = 15.00

# ══════════════════════════════════════════════════════════════════
#  VAULT TARGET STRUCTURE
# ══════════════════════════════════════════════════════════════════

VAULT_FOLDERS = [
    "00-Home",
    "01-Fundamentals",
    "02-Recon-and-Enumeration",
    "03-Web-Application-Security",
    "04-Network-Exploitation",
    "05-Linux-Privilege-Escalation",
    "06-Windows-Privilege-Escalation",
    "07-Active-Directory",
    "07.1-AD-Enumeration",
    "07.2-AD-Exploitation",
    "07.3-AD-Post-Compromise",
    "08-Post-Exploitation",
    "09-Pivoting-and-Tunnelling",
    "10-Evasion-and-AV-Bypass",
    "11-Cloud-Security",
    "12-Malware-and-Reversing",
    "13-Red-Team-Ops",
    "14-Tools-Reference",
    "15-Cheatsheets",
    "16-Lab-Notes",
    "17-Attachments",
    "98-Templates",
    "99-Archive",
]

# ══════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT
# ══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = f"""You are an advanced cybersecurity research engine, a strict validator, and an expert Obsidian vault architect.

This vault is a permanent, professional-grade cybersecurity knowledge base used across:
- Security certifications (OSCP, CPTS, OSCE, CRTO, PNPT, CEH, CISSP, etc.)
- CTF competitions and lab environments (HTB, THM, PG, VulnHub)
- Professional penetration testing engagements
- Red team operations
- Purple team and detection engineering
- Real-world client projects
- Personal research and tool development

Do not act as an academic tutor. Do not provide long explanations or theoretical background.
Your task is to audit, research, expand, fix errors, and format raw cybersecurity notes into a production-ready, operationally accurate Obsidian markdown note suitable for real-world use.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY PROCESSING INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. AUTOMATED TAGGING
   Begin the very first line with relevant lowercase Obsidian tags.
   Examples: #recon #scanning #nmap | #exploit #privesc #windows | #ad #kerberoasting #redteam

2. EXECUTION LOCATION LABELLING
   Every command or code block must have exactly one execution label as a comment on the
   line immediately above it. If a block contains multiple commands, one label covers the block.

   Attacker Machine:
   - Execution: Attacker (Kali)              → commands run on your attack machine

   Target Machine (OS-Specific):
   - Execution: Target Machine (Linux)       → compromised Linux host
   - Execution: Target Machine (Windows)     → compromised Windows host
   - Execution: Target Machine               → use only when OS is unknown or irrelevant

   Active Directory:
   - Execution: Domain Controller            → commands run on or directly against the DC
   - Execution: Workstation / Client         → domain-joined Windows client machine
   - Execution: Pivot Machine                → internal pivot or relay host

   Servers:
   - Execution: Web Server                   → compromised web server
   - Execution: Database Server              → compromised database server
   - Execution: Mail Server                  → compromised mail server

   Cloud:
   - Execution: Cloud Instance (Linux)       → Linux VM in AWS / Azure / GCP
   - Execution: Cloud Instance (Windows)     → Windows VM in AWS / Azure / GCP
   - Execution: Cloud Control Plane          → cloud CLI or API calls (aws, az, gcloud)

   Isolated Environments:
   - Execution: Sandbox Environment          → isolated payload testing environment
   - Execution: Container (Docker)           → Dockerised malware or reversing environment

   Offline / Local Analysis:
   - Execution: Offline Analysis             → local machine only, no network target
                                               (hashcat, ghidra, strings, jq, log parsing,
                                               BloodHound dump analysis, payload decoding)

   General:
   - Execution: Either (Attacker / Target)   → commands valid in both contexts

3. AUDIT, VERIFY AND FIX COMMANDS
   Review every command against current documentation, CVE databases, tool changelogs,
   and real-world operational standards. Fix all of the following:
   - Deprecated tools      : crackmapexec → netexec | python → python3
   - Outdated flags        : update to current syntax from official man pages
   - Incorrect assumptions : commands that only work in lab/CTF but fail in real engagements
   - Scope violations      : add > [!WARNING] for commands requiring explicit written
                             authorisation before use in a real engagement
   - Wordlist paths        : standardise to current SecLists (/usr/share/seclists/)
   - Retired tools         : replace with current maintained equivalents
   - Lab-only techniques   : flag techniques that work in labs but are easily detected
                             or blocked in hardened real-world environments

4. INJECT AND EXPAND COMMANDS
   Do not rely only on the input. Actively research and inject across all use cases:
   - Standard commands for any tool or technique mentioned but not demonstrated
   - Alternative commands achieving the same goal via a different tool or method
   - The next logical command in a workflow (enumeration → exploitation → post-ex)
   - Commands for common variations (authenticated vs unauthenticated, Linux vs Windows)
   - Detection-evasion variants (quiet scans alongside aggressive, OPSEC-safe alternatives)
   - One-liners combining multiple steps for speed in exams and live ops
   - Post-exploitation follow-up commands after any initial access technique
   - Cleanup and OPSEC commands (clearing logs, removing artefacts, timestomping)
   - Commands for edge cases (non-standard ports, IPv6, legacy systems, cloud-hosted targets)
   - Real-world engagement commands with proper output handling and logging flags
   - Commands for both automated tooling and manual verification
   - Proof-of-concept commands for reporting and evidence collection

   Priority tools to always include when topic is relevant:
   - Recon / OSINT     : nmap, netexec, enum4linux-ng, ldapdomaindump, BloodHound,
                         amass, subfinder, httpx, nuclei, shodan, theHarvester
   - Web               : ffuf, gobuster, nikto, sqlmap, burp, whatweb, wfuzz,
                         dalfox, arjun, feroxbuster, katana
   - PrivEsc           : linpeas, winpeas, pspy, PowerUp, BeRoot, PEASS-ng
   - Active Directory  : BloodHound, impacket suite, netexec, Rubeus, mimikatz,
                         ldapsearch, ADExplorer, PingCastle, Certipy
   - Exploitation      : msfvenom, searchsploit, metasploit, pwncat-cs, sliver
   - Pivoting          : ligolo-ng, chisel, ssh tunnelling, sshuttle, rpivot
   - Passwords         : hashcat, john, hydra, medusa, kerbrute, sprayhound
   - Evasion           : AMSI bypass, obfuscation, process injection, living-off-the-land
   - Red Team / C2     : Cobalt Strike concepts, Sliver, Havoc, Mythic
   - Cloud             : aws cli, az cli, gcloud, pacu, ScoutSuite, Prowler, CloudMapper
   - Reversing         : ghidra, gdb, pwndbg, radare2, strings, ltrace, strace
   - Blue Team         : sigma rules, yara rules, splunk SPL, KQL for Sentinel
   - Reporting         : screenshot commands, evidence capture, output logging flags

5. FIX ERRORS AND ADD OPERATIONAL CONTEXT
   - Correct all factual errors, wrong assumptions, incorrect flags
   - Add > [!WARNING] for techniques that no longer work on modern patched systems
   - Add > [!WARNING] for commands that require written authorisation before use
   - Add > [!TIP] for OPSEC considerations in real engagements vs lab environments
   - Add > [!IMPORTANT] for steps critical to avoid detection or data loss
   - Flag differences in behaviour between lab environments and hardened production systems
   - Note where techniques may trigger EDR, AV, or SIEM alerts in real engagements
   - Add reporting notes where evidence should be captured for client deliverables

6. OBSIDIAN INTEGRATION
   - Use ## Headers for section grouping
   - Use > [!NOTE], > [!WARNING], > [!TIP], > [!IMPORTANT] callouts
   - Use fenced code blocks with syntax highlighting:
     ```bash ```powershell ```python ```cmd ```sql ```yaml ```json
   - Add [[Backlinks]] to related notes where relevant

7. VARIABLE STANDARDS — use exactly these placeholders in every command, no exceptions:

   Network / Hosts:
   ${{attacker}}            → attacker / Kali machine IP
   ${{target}}              → target machine IP (generic)
   ${{domain_controller}}   → domain controller IP
   ${{client}}              → domain-joined workstation IP
   ${{pivot}}               → internal pivot machine IP
   ${{subnet}}              → target subnet (e.g. 192.168.1.0/24)
   ${{port}}                → target port number

   Active Directory:
   ${{domain}}              → AD domain name (e.g. corp.local)
   ${{domain_short}}        → NetBIOS domain name (e.g. CORP)
   ${{dc_hostname}}         → domain controller hostname (e.g. DC01)
   ${{base_dn}}             → LDAP base DN (e.g. DC=corp,DC=local)

   Credentials:
   ${{user}}                → target username
   ${{password}}            → target plaintext password
   ${{hash}}                → NTLM or other hash value
   ${{ticket}}              → Kerberos ticket path (.ccache or .kirbi)
   ${{domain_user}}         → DOMAIN\\username format
   ${{admin_user}}          → privileged or admin username

   Files / Listener:
   ${{lhost}}               → listener / callback IP (usually same as ${{attacker}})
   ${{lport}}               → listener port
   ${{payload}}             → payload filename
   ${{wordlist}}            → wordlist path
   ${{output}}              → output file path

8. EXTREME CONDENSATION
   Maximum one sentence explanation per tool or phase.
   Zero explanation if the command is self-explanatory.
   Focus 100% on execution context.

9. OPERATIONAL NOTES
   Where relevant, add a brief operational context block covering:
   - Difference between lab/exam use and real-world engagement use
   - Known detection signatures for the technique (what blue team sees)
   - OPSEC risk level: Low / Medium / High
   - Whether written authorisation is required before executing
   - Evidence capture recommendation for reporting purposes

10. ZERO CONVERSATIONAL FILLER
    Output only raw Obsidian Markdown.
    No greetings, no closing remarks, no "I have updated..." statements.

11. FOLDER CLASSIFICATION
    The very last line of your output must be exactly:
    VAULT_FOLDER: <folder_name>

    Choose only from: {", ".join(VAULT_FOLDERS)}

    Classification rules:
    - Technique-based notes  → most specific relevant folder
    - Tool reference notes   → 14-Tools-Reference
    - Lab / machine writeups → 16-Lab-Notes
    - Engagement templates   → 15-Cheatsheets
    - Outdated or unclear    → 99-Archive
    - AD enumeration         → 07.1-AD-Enumeration
    - AD attacks             → 07.2-AD-Exploitation
    - AD post-compromise     → 07.3-AD-Post-Compromise
"""

IMAGE_CAPTION_PROMPT = """You are analysing a cybersecurity screenshot or diagram.
Respond with exactly these two lines and nothing else:
CAPTION: <one sentence describing what this image shows>
EXTRACTED: <any visible commands, IPs, usernames, hashes, flags, or tool output — or write 'none'>"""

# ══════════════════════════════════════════════════════════════════
#  STATE MANAGEMENT
# ══════════════════════════════════════════════════════════════════

def load_state() -> dict:
    """Load all state records into a dict keyed by file path (last entry wins)."""
    state = {}
    if not STATE_FILE.exists():
        return state
    with STATE_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rec = json.loads(line)
                    state[rec["path"]] = rec
                except json.JSONDecodeError:
                    pass
    return state


def log_status(path: Path, status: str, error: str = None, out_path: str = None):
    """Append a status record to the state file and the human log."""
    record = {
        "path"     : str(path),
        "status"   : status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    if error:
        record["error"] = error
    if out_path:
        record["out_path"] = out_path

    with STATE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    with LOG_FILE.open("a", encoding="utf-8") as f:
        msg = f"[{record['timestamp']}] {status.upper():10} {path.name}"
        if error:
            msg += f" | {error[:120]}"
        f.write(msg + "\n")

# ══════════════════════════════════════════════════════════════════
#  FILE DISCOVERY
# ══════════════════════════════════════════════════════════════════

def iter_markdown_files(root: Path):
    """Walk vault, yield all .md files excluding system folders."""
    for p in sorted(root.rglob("*.md")):
        parts = p.parts
        if ".obsidian" in parts or "_RAW_UNPROCESSED" in parts or ".trash" in parts:
            continue
        yield p


def find_image_file(image_name: str, note_path: Path, vault_root: Path):
    """
    Search for an image file by name. Checks in order:
    1. Same directory as the note
    2. Common attachment folder names near the note
    3. Anywhere in the vault (fallback)
    """
    candidate = note_path.parent / image_name
    if candidate.exists():
        return candidate

    for folder_name in ("attachments", "_attachments", "assets", "images", "media", "files"):
        candidate = note_path.parent / folder_name / image_name
        if candidate.exists():
            return candidate
        candidate = vault_root / folder_name / image_name
        if candidate.exists():
            return candidate

    for found in vault_root.rglob(image_name):
        if found.is_file():
            return found

    return None


def extract_image_refs(content: str) -> list:
    """
    Extract image references from markdown content.
    Returns list of (original_ref, filename) tuples.
    Handles Obsidian wikilinks and standard markdown image syntax.
    """
    refs = []

    for match in re.finditer(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp))\]\]', content, re.IGNORECASE):
        full_ref  = match.group(0)
        file_name = Path(match.group(1)).name
        refs.append((full_ref, file_name))

    for match in re.finditer(r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|webp))\)', content, re.IGNORECASE):
        full_ref  = match.group(0)
        file_name = Path(match.group(2)).name
        refs.append((full_ref, file_name))

    seen   = set()
    unique = []
    for ref in refs:
        if ref[0] not in seen:
            seen.add(ref[0])
            unique.append(ref)
    return unique

# ══════════════════════════════════════════════════════════════════
#  IMAGE CAPTIONING (OCR + DESCRIPTION)
# ══════════════════════════════════════════════════════════════════

def caption_image(client: Anthropic, image_path: Path) -> tuple:
    """Send image to Claude Vision for OCR + captioning."""
    media_map = {
        ".jpg" : "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png" : "image/png",
        ".gif" : "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_map.get(image_path.suffix.lower(), "image/png")

    with image_path.open("rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model      = MODEL,
        max_tokens = 500,
        messages   = [
            {
                "role": "user",
                "content": [
                    {
                        "type"  : "image",
                        "source": {
                            "type"      : "base64",
                            "media_type": media_type,
                            "data"      : image_data,
                        },
                    },
                    {"type": "text", "text": IMAGE_CAPTION_PROMPT},
                ],
            }
        ],
    )

    raw       = response.content[0].text.strip()
    caption   = ""
    extracted = ""

    for line in raw.splitlines():
        if line.startswith("CAPTION:"):
            caption = line[len("CAPTION:"):].strip()
        elif line.startswith("EXTRACTED:"):
            extracted = line[len("EXTRACTED:"):].strip()

    if not caption:
        caption = "Image — could not generate caption"

    return caption, extracted


def process_images_in_note(client: Anthropic, content: str, note_path: Path, dry_run: bool) -> str:
    """
    Find all images in a note, caption them via Claude Vision,
    and inject captions below each image reference.
    """
    refs = extract_image_refs(content)
    if not refs:
        return content

    for original_ref, file_name in refs:
        if f"<!-- caption:{file_name} -->" in content:
            continue

        image_path = find_image_file(file_name, note_path, VAULT_IN)

        if image_path is None:
            replacement = (
                f"{original_ref}\n"
                f"> [!WARNING] Image file `{file_name}` not found in vault.\n"
            )
            content = content.replace(original_ref, replacement, 1)
            continue

        if dry_run:
            replacement = (
                f"{original_ref}\n"
                f"> [!NOTE] <!-- caption: DRY RUN — would caption `{file_name}` -->\n"
            )
            content = content.replace(original_ref, replacement, 1)
            continue

        try:
            caption, extracted = caption_image(client, image_path)
            caption_block = f"> [!NOTE] **Image:** {caption}"
            if extracted and extracted.lower() != "none":
                caption_block += f"\n> **Extracted:** `{extracted}`"

            replacement = (
                f"{original_ref}\n"
                f"{caption_block}\n"
                f"<!-- caption:{file_name} -->\n"
            )
            content = content.replace(original_ref, replacement, 1)

        except Exception as e:
            replacement = (
                f"{original_ref}\n"
                f"> [!WARNING] Caption failed for `{file_name}`: {str(e)[:80]}\n"
            )
            content = content.replace(original_ref, replacement, 1)

    return content

# ══════════════════════════════════════════════════════════════════
#  CLAUDE API — NOTE REWRITING
# ══════════════════════════════════════════════════════════════════

def call_claude(client: Anthropic, raw_note: str) -> str:
    """Send note to Claude for rewriting. Retries automatically on rate limit."""
    user_message = (
        f"Input:\n{raw_note}\n\n"
        f"Output: A verified, optimised, expanded, and error-corrected Obsidian markdown note."
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model      = MODEL,
                max_tokens = MAX_TOKENS,
                system     = SYSTEM_PROMPT,
                messages   = [{"role": "user", "content": user_message}],
            )
            return response.content[0].text

        except Exception as e:
            err_str = str(e).lower()
            if "rate_limit" in err_str or "529" in err_str or "overloaded" in err_str:
                if attempt < MAX_RETRIES:
                    print(f"\n     ⏳ Rate limited — waiting {RETRY_WAIT}s (attempt {attempt}/{MAX_RETRIES})")
                    time.sleep(RETRY_WAIT)
                else:
                    raise
            else:
                raise

# ══════════════════════════════════════════════════════════════════
#  FOLDER CLASSIFICATION
# ══════════════════════════════════════════════════════════════════

def extract_vault_folder(rewritten: str) -> tuple:
    """
    Extract the VAULT_FOLDER line from the rewritten note.
    Returns (cleaned_note, folder_name). Falls back to 99-Archive.
    """
    lines       = rewritten.strip().splitlines()
    folder      = "99-Archive"
    clean_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("VAULT_FOLDER:"):
            raw_folder = stripped[len("VAULT_FOLDER:"):].strip()
            if raw_folder in VAULT_FOLDERS:
                folder = raw_folder
            else:
                for vf in VAULT_FOLDERS:
                    if raw_folder.lower() in vf.lower() or vf.lower() in raw_folder.lower():
                        folder = vf
                        break
        else:
            clean_lines.append(line)

    return "\n".join(clean_lines).strip(), folder

# ══════════════════════════════════════════════════════════════════
#  COST ESTIMATOR
# ══════════════════════════════════════════════════════════════════

def estimate_cost(root: Path):
    """Pre-flight cost estimate — no API calls made."""
    print("\n📊 Cost Estimation (no API calls will be made)\n")

    total_chars   = 0
    total_files   = 0
    skipped_large = 0
    skipped_empty = 0

    for p in iter_markdown_files(root):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if not text.strip():
            skipped_empty += 1
            continue

        if len(text) > MAX_CHARS:
            skipped_large += 1
            print(f"   ⚠️  Large file (will be flagged): {p.name} ({len(text):,} chars)")
            continue

        total_chars += len(text)
        total_files += 1

    input_tokens  = total_chars / 4
    output_tokens = input_tokens * 1.5

    input_cost  = (input_tokens  / 1_000_000) * COST_INPUT_PER_M
    output_cost = (output_tokens / 1_000_000) * COST_OUTPUT_PER_M
    total_cost  = input_cost + output_cost
    batch_cost  = total_cost * 0.5

    print(f"   Files to process    : {total_files:,}")
    print(f"   Skipped (empty)     : {skipped_empty:,}")
    print(f"   Flagged (too large) : {skipped_large:,}")
    print(f"   Total input chars   : {total_chars:,}")
    print(f"   Est. input tokens   : {int(input_tokens):,}")
    print(f"   Est. output tokens  : {int(output_tokens):,}")
    print(f"\n   💰 Standard API cost  : ~${total_cost:.2f} USD")
    print(f"   💰 Batch API cost     : ~${batch_cost:.2f} USD (50% discount)")
    print(f"\n   ℹ️  Image captioning adds ~$0.01–0.05 per image (not included above)")
    print(f"   ℹ️  Your $20 budget is {'✅ sufficient' if total_cost < 18 else '⚠️  tight — monitor usage'}\n")

# ══════════════════════════════════════════════════════════════════
#  MAIN FILE PROCESSOR
# ══════════════════════════════════════════════════════════════════

def rewrite_file(client: Anthropic, path: Path, state: dict, dry_run: bool, retry_failed: bool) -> str:
    """Process a single markdown file through the full pipeline."""
    path_str = str(path)

    # ── Check existing state ───────────────────────────────────────
    existing = state.get(path_str)
    if existing:
        status = existing.get("status")
        if status == "processed":
            return "skip"
        if status == "failed" and not retry_failed:
            return "skip"
        if status == "skipped":
            return "skip"

    # ── Read file ──────────────────────────────────────────────────
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        log_status(path, "failed", f"Read error: {e}")
        return "failed"

    if not raw.strip():
        log_status(path, "skipped", "empty file")
        return "skipped"

    if len(raw) > MAX_CHARS:
        log_status(path, "skipped", f"File too large ({len(raw):,} chars) — split manually")
        print(f"\n   ⚠️  SKIPPED (too large — {len(raw):,} chars): {path.name}")
        return "skipped"

    if dry_run:
        print(f"\n   🔍 DRY RUN: Would process {path.name} ({len(raw):,} chars)")
        return "dry_run"

    # ── Step 1: Process images ─────────────────────────────────────
    try:
        raw_with_captions = process_images_in_note(client, raw, path, dry_run)
    except Exception as e:
        print(f"\n   ⚠️  Image processing failed for {path.name}: {e}")
        raw_with_captions = raw

    # ── Step 2: Rewrite with Claude ────────────────────────────────
    try:
        rewritten = call_claude(client, raw_with_captions)
    except Exception as e:
        log_status(path, "failed", f"Claude API error: {str(e)[:200]}")
        return "failed"

    # ── Step 3: Extract folder classification ──────────────────────
    clean_note, target_folder = extract_vault_folder(rewritten)

    # ── Step 4: Write output ───────────────────────────────────────
    try:
        out_path = VAULT_OUT / target_folder / path.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(clean_note, encoding="utf-8")
        log_status(path, "processed", out_path=str(out_path))
        return "processed"
    except Exception as e:
        log_status(path, "failed", f"Write error: {e}")
        return "failed"

# ══════════════════════════════════════════════════════════════════
#  ARGUMENT PARSER
# ══════════════════════════════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser(
        description="CyberSec Vault Rebuild — Claude API Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vault_rebuild.py --estimate-cost
  python vault_rebuild.py --dry-run --limit 5
  python vault_rebuild.py --limit 20
  python vault_rebuild.py
  python vault_rebuild.py --retry-failed
        """
    )
    parser.add_argument("--estimate-cost", action="store_true",
                        help="Estimate API cost without making any calls")
    parser.add_argument("--dry-run",       action="store_true",
                        help="Walk vault and show what would be processed — no API calls")
    parser.add_argument("--limit",         type=int, default=None,
                        help="Process only N files (for testing)")
    parser.add_argument("--retry-failed",  action="store_true",
                        help="Retry files that previously failed")
    parser.add_argument("--vault-in",      type=str, default=None,
                        help="Override VAULT_IN path")
    parser.add_argument("--vault-out",     type=str, default=None,
                        help="Override VAULT_OUT path")
    return parser.parse_args()

# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main():
    args = parse_args()

    global VAULT_IN, VAULT_OUT
    if args.vault_in:
        VAULT_IN  = Path(args.vault_in)
    if args.vault_out:
        VAULT_OUT = Path(args.vault_out)

    if not VAULT_IN.exists():
        print(f"\n❌ VAULT_IN path does not exist: {VAULT_IN}")
        print("   Edit the VAULT_IN variable at the top of this script.\n")
        sys.exit(1)

    if args.estimate_cost:
        estimate_cost(VAULT_IN)
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY environment variable not set.")
        print("   Run: set ANTHROPIC_API_KEY=your_key_here\n")
        sys.exit(1)

    client     = Anthropic(api_key=api_key)
    state      = load_state()
    all_files  = list(iter_markdown_files(VAULT_IN))

    if args.limit:
        all_files = all_files[:args.limit]

    total  = len(all_files)
    counts = {"processed": 0, "skipped": 0, "failed": 0, "dry_run": 0, "skip": 0}

    print(f"\n{'═'*60}")
    print(f"  CyberSec Vault Rebuild")
    print(f"  Vault IN  : {VAULT_IN}")
    print(f"  Vault OUT : {VAULT_OUT}")
    print(f"  Files     : {total:,}")
    print(f"  Mode      : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'═'*60}\n")

    for i, path in enumerate(all_files, 1):
        rel = path.relative_to(VAULT_IN)
        print(f"  [{i:4}/{total}] {rel} ...", end="", flush=True)

        result = rewrite_file(
            client       = client,
            path         = path,
            state        = state,
            dry_run      = args.dry_run,
            retry_failed = args.retry_failed,
        )

        icon = {
            "processed": "✅",
            "skipped"  : "⏭️ ",
            "failed"   : "❌",
            "dry_run"  : "🔍",
            "skip"     : "⏭️ ",
        }.get(result, "❓")

        print(f" {icon}")
        counts[result] = counts.get(result, 0) + 1

        if i % 10 == 0:
            state = load_state()

        if result == "processed":
            time.sleep(1)

    print(f"\n{'═'*60}")
    print(f"  ✅ Processed  : {counts.get('processed', 0):,}")
    print(f"  ⏭️  Skipped    : {counts.get('skipped', 0) + counts.get('skip', 0):,}")
    print(f"  ❌ Failed     : {counts.get('failed', 0):,}")
    if args.dry_run:
        print(f"  🔍 Dry run    : {counts.get('dry_run', 0):,}")
    print(f"\n  📁 Output vault : {VAULT_OUT}")
    print(f"  📋 State file   : {STATE_FILE}")
    print(f"  📝 Log file     : {LOG_FILE}")

    if counts.get("failed", 0) > 0:
        print(f"\n  ⚠️  Re-run with --retry-failed to retry {counts['failed']} failed files")
    if counts.get("skipped", 0) > 0:
        print(f"  ℹ️  Large or empty files logged — review manually")

    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()

