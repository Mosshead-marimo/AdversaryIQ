# 🧨 PyDetonator

### Dynamic Malware Detonation & Behavioral Threat Intelligence Engine

------------------------------------------------------------------------

## 🚀 Overview

**PyDetonator** is a container-isolated dynamic malware analysis engine
that transforms raw execution behavior into structured threat
intelligence.

It detonates suspicious files inside a controlled Docker sandbox,
reconstructs execution flow, maps behavior to the full MITRE ATT&CK
framework, applies heuristic detection, and produces intelligence-grade
reports.

PyDetonator is built as a modular, API-first behavioral analysis
platform designed for research, blue teams, and security automation.

------------------------------------------------------------------------

## 🎯 Problem Statement

Modern malware evades static detection using:

-   Obfuscation\
-   Multi-stage payload delivery\
-   Delayed execution\
-   Living-off-the-land binaries\
-   Encrypted command-and-control\
-   Process chaining and injection

Signature-based scanning is no longer sufficient.

PyDetonator focuses on **behavior**, not appearance.

------------------------------------------------------------------------

## 🧠 Core Capabilities

### 🔹 Isolated Dynamic Execution

-   Docker-based sandbox
-   Non-root execution
-   Memory and PID limits
-   Linux capability dropping
-   Read-only container filesystem
-   Automatic container teardown

### 🔹 Behavioral Monitoring

-   Full syscall tracing (`strace`)
-   Network traffic capture (`tcpdump`)
-   Process creation tracking
-   File system interaction logging
-   Execution timeline reconstruction

### 🔹 Process Intelligence

-   Parent-child PID reconstruction
-   Execution hierarchy mapping
-   Multi-stage execution detection
-   Fork storm identification
-   Dropper pattern analysis

### 🔹 Execution Timeline Engine

-   Chronological event sequencing
-   File-write → execute correlation
-   Network-after-execution detection
-   Behavioral flow reconstruction

### 🔹 Heuristic Detection Engine

Pattern-based intelligence including: - Dropper behavior\
- Temp directory execution\
- Network beaconing patterns\
- Mass process spawning\
- Staged payload chains

### 🔹 Full MITRE ATT&CK Integration

-   Uses official MITRE Enterprise ATT&CK dataset (STIX)
-   Dynamic technique mapping
-   Tactic distribution analysis
-   Evidence correlation
-   ATT&CK-aligned threat profiling

### 🔹 Risk Scoring & Classification

Final classifications: - **Benign** - **Suspicious** - **Malicious**

### 🔹 Structured Intelligence Reporting

Each analysis produces a comprehensive JSON report including: - Analysis
metadata - SHA256 file hash - Behavioral summary - Process tree
reconstruction - Execution timeline - MITRE technique mapping -
Heuristic flags - Indicators of compromise - Risk assessment

------------------------------------------------------------------------

## 🏗️ System Architecture

### High-Level Execution Flow

Sample Input\
↓\
Sandbox Execution (Docker)\
↓\
Monitoring Layer\
↓\
Analyzer Layer\
↓\
Heuristic Engine\
↓\
MITRE Mapping\
↓\
Scoring Engine\
↓\
Reporting Engine\
↓\
Structured Intelligence Output

------------------------------------------------------------------------

## 📁 Project Structure

    app/
    ├── core/              # Configuration, constants, MITRE loader
    ├── sandbox/           # Docker sandbox environment
    ├── monitoring/        # Syscall & execution parsers
    ├── analyzer/          # Behavior, heuristics, scoring
    ├── reporting/         # Report generation
    ├── orchestrator/      # Pipeline controller
    └── api/               # FastAPI backend

------------------------------------------------------------------------

## 🔒 Security Model

-   Non-root container execution\
-   Capability dropping\
-   Memory & PID limiting\
-   Read-only filesystem\
-   Automatic container removal\
-   No host privilege escalation

------------------------------------------------------------------------

## ⚙️ Running the System

### Build Sandbox Image

docker build -t pydetonator-sandbox ./app/sandbox

### Start API Server

uvicorn app.api.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 🎓 Intended Audience

-   Malware researchers\
-   SOC engineers\
-   Blue team developers\
-   Cybersecurity students\
-   Threat intelligence analysts\
-   Security automation engineers

------------------------------------------------------------------------

## 🧨 PyDetonator

Behavior-first. Intelligence-driven. Modular by design.
