"""Configuration file for defining paths used throughout the application."""

from pathlib import Path

# Base directory for the project (project root)
# This file is in src/bot/config/, so we go up 3 levels to reach project root
BASE_DIR = Path(__file__).parent.parent.parent.parent

# Data directory for storing JSONL files
DATA_DIR = BASE_DIR / "data"

# User data file (JSONL format)
USERS_FILE = DATA_DIR / "users.jsonl"

# Transactions data file (JSONL format)
TRANSACTIONS_FILE = DATA_DIR / "transactions.jsonl"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
