import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Telegram Settings ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6049120581"))
CHANNEL_USERNAME = "@BrahMosAI"

# --- AI Settings ---
AI_API_URL = os.getenv("AI_API_URL", "https://api.gptnix.online/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-4o")

# --- GitHub Settings ---
GITHUB_PAT = os.getenv("GITHUB_PAT", "")

# --- VPS Access (Main Space) ---
VPS_LOGIN = os.getenv("VPS_LOGIN", "admin_root") # Placeholder for primary VPS identity

# --- Community & Support ---
DEV_LINK = "https://t.me/ankurslys"
COMMUNITY_LINK = "https://t.me/brahmosai"

# --- Resource Limits (Free Tier) ---
FREE_TIER_RAM = 100  # MB
FREE_TIER_DISK = 1024  # MB (1GB)

# --- Resource Limits (Pro Tier) ---
PRO_TIER_RAM = 512  # MB
PRO_TIER_DISK = 5120  # MB (5GB)

# --- System Prompt ---
SYSTEM_PROMPT = """
You are the BrahMos Cloud Security & Deployment Agent for a PaaS service. 
You must evaluate codebases and interact strictly via provided Tools (Function Calling).

RULES:
1. Scan for MALWARE or ILLEGAL SCRIPTS (crypto miners, stressers, phishing). If found, you MUST call the `reject_user_file` tool with a clear reason.
2. If the code is SAFE and healthy, you MUST call the `deploy_project` tool.
3. For deployments, analyze the structure, figure out the dependencies, and generate a `requirements.txt`.
4. Generate a `start.sh` script to run the bot.
5. EXPOSED SECRETS POLICY: If you find hardcoded Telegram bot tokens or API keys, DO NOT REJECT the file. Extract them, provide them in the `env_file` parameter, and ensure `start.sh` expects them as environment variables.
"""
