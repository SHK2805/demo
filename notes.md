
You are an expert Principal Security Engineer and Python Developer. I need your help to build a modular, command-line Python application designed for an automated Purple Team verification pipeline. 

### Context & Workflow:
1. Red Team execution details (timestamps, target hostnames, specific techniques/commands executed) will eventually be parsed via Jira.
2. The Purple Team needs to verify if these tests left a telemetry trail or triggered alerts across multiple corporate security systems.
3. The first phase of this project focuses strictly on connecting to Splunk and verifying data existence.

### Requirements for the Script/Project:
- **Environment:** macOS environment, running inside a Python virtual environment (`venv`) behind a strict corporate proxy/network.
- **Interface:** Command-line interface (CLI) only. No frontend or GUI.
- **Library:** Must use the official `splunk-enterprise-sdk` (`splunklib`).
- **Architecture:** The code must be highly modular, separating the Splunk connection logic, the search/polling execution logic, and the main CLI entry point.
- **Authentication:** Support Splunk Bearer Token authentication, with an option to disable SSL verification (`verify=False`) for internal/dev environments.
- **Execution Mode:** Use asynchronous search jobs (`exec_mode="normal"`), polling the search job status until complete before fetching results, to handle heavy corporate indexes efficiently.

### What to Generate:
Please provide a clean, production-ready directory layout for this project and the core Python files needed to run a baseline connectivity and query verification test. Include robust error handling for API timeouts, network proxy interference, and authentication failures.
