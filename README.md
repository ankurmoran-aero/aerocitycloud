# ☁️ BrahMos Cloud: AI-Driven PaaS Orchestrator

BrahMos Cloud is a sophisticated, lightweight **Platform as a Service (PaaS)** solution engineered to bridge the gap between AI intelligence and containerized hosting. Designed for speed, security, and developer convenience, it enables users to deploy full-stack bots, web applications, and scripts directly through a Telegram interface.

By leveraging **OpenAI's Function Calling** and **Docker Engine SDK**, BrahMos Cloud automates the entire DevOps lifecycle—from security auditing and dependency resolution to isolated deployment and real-time resource monitoring.

---

## 🚀 Enterprise-Grade Features

### 🛡️ AI-Native Security Guardrails
BrahMos Cloud doesn't just run code; it understands it. Every deployment undergoes a mandatory security scan by a specialized LLM agent. 
- **Malware Interdiction:** Detects miners, stressers, and malicious scripts before they reach the VPS.
- **Auto-Secret Extraction:** Beginners often expose tokens; our AI automatically identifies and migrates them into secure `.env` files, rewriting deployment scripts on the fly to ensure security compliance.

### 🐳 Robust Container Orchestration
- **Full Isolation:** Every project runs in a dedicated, non-root Docker container, ensuring a multi-tenant environment where workloads are strictly separated.
- **Dynamic Resource Enforcement:** A built-in **Watchdog Sniper** monitors RAM and Disk usage in real-time, instantly isolating or terminating processes that exceed their allocated quota.
- **System-Level Dependency Resolution:** Automatically detects project requirements and installs necessary system libraries (`ffmpeg`, `gcc`, `python-dev`, etc.) to ensure successful builds.

### 🔄 Zero-Friction CI/CD
- **Native Webhooks:** Integrated FastAPI-powered webhook listener for GitHub.
- **Auto-Redeployment:** Push to your repository, and BrahMos Cloud will automatically pull the latest changes, rebuild the image, and cycle the container without human intervention.

### 📊 Modern UI/UX
- **Telegram Dashboard:** A high-performance, OSINT-inspired grid interface for managing applications.
- **Real-Time Analytics:** View live uptime (Runtime) and memory consumption metrics for every active project.

---

## 🛠️ Technical Architecture

- **Backend:** Python 3.10+
- **Orchestration:** Docker SDK for Python
- **AI Integration:** OpenAI GPT-4o with Native Tool Calling
- **Web Layer:** FastAPI & Uvicorn
- **UI Framework:** pyTelegramBotAPI
- **Process Management:** PM2 (for core bot stability)

---

## 📦 Getting Started

### 1. Prerequisites
- Linux VPS (Ubuntu 22.04+ recommended)
- Docker Engine installed and running
- Python 3.10+

### 2. Installation
```bash
git clone https://github.com/ankurmoran96-openai/brahmoscloud.git
cd brahmoscloud
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory. **BrahMos Cloud is highly configurable.** You must define your own `SYSTEM_PROMPT` to guide the AI's deployment logic.
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_id
AI_API_KEY=your_openai_api_key
GITHUB_PAT=your_github_personal_access_token (optional)
SYSTEM_PROMPT=Read the code and define your security/deployment rules here.
```

---

## 🛡️ License

This project is open-source and licensed under the **MIT License**. We encourage community contributions and forks for innovation.

---
*Developed with grit and vision by a 14-year-old on a mobile device.*
