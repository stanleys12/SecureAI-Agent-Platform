# Secure AI Agent Execution Platform 🛡️🤖

A system that allows AI agents to use tools autonomously while enforcing strict, enterprise-grade security policies and real-time defense monitoring.

## 🧨 The Problem
Modern AI agents that can interact with the outside world are susceptible to:
- **Prompt Injection:** An attacker overrides instructions to run malicious commands.
- **Tool Abuse / LFI / SSRF:** The agent queries unauthorized databases, internal domains, or sensitive file paths.
- **Data Exfiltration:** Sensitive user data is leaked through URL queries or remote hosts.

## 🛡️ The Solution (Architecture)

1. **Policy Engine:** JSON-based rule system enforcing domain allowlists, accepted HTTP methods, and read-only DB permissions.
2. **Sandbox Layer (Executor):** A sterile execution wrapper preventing direct API calls and filtering requests through the Policy Engine.
3. **Defense Monitor:** Real-time state tracking and anomaly detection. Catches Rate-limit abuses, suspicious SQL payloads, and URL exfiltration signatures before execution.
4. **Adversarial Attack Simulator:** A comprehensive script acting as the "Attacker", validating that the aforementioned defenses hold up against Prompt Injection, SQLi, and DDOS.

## 🛠️ Components

- `agent/`: Simple simulated LLM routing intents to tools.
- `tools/`: Standardized BaseTool interfaces (`HTTP`, `DB`, `File`).
- `policy/`: Configuration (`policies.json`) and the PolicyValidator.
- `sandbox/`: The secure wrapper (`SecureToolExecutor`).
- `defense/`: `AnomalyDetector`, logging, and immediate response triggers.
- `evaluation/`: Generates metrics reports on allowed vs blocked requests.
- `attacks/`: `AttackRunner` that hits the system with malicious payloads to verify robustness.

## 🚀 Usage

**Run the standard benign Agent:**
```bash
python3 main.py
```

**Run the Adversarial Attack Simulator:**
```bash
python3 attacks/runner.py
```

This will run SQL injection attempts, an Exfiltration attempt via URL, and an internal server SSRF attempt, proving that the Sandboxing and Monitoring actively drop the requests.
