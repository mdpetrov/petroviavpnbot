"""Environment variable configuration."""

import os
from dotenv import load_dotenv
from .paths import BASE_DIR

# Load environment variables from .secret/env/bot.env
ENV_FILE = BASE_DIR / ".secret" / "env" / "bot.env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Fallback: try to load from .env in project root (for development)
    fallback_env = BASE_DIR / ".env"
    if fallback_env.exists():
        load_dotenv(fallback_env)

# Bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN not found in environment variables. "
        f"Please set it in {ENV_FILE} or create a .env file in the project root."
    )
