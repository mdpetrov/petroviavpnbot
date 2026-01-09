# Petrovia VPN Telegram Bot

Telegram bot for managing user payments and subscriptions for a custom VPN server.

## Project Structure

```
petroviavpnbot/
├── src/
│   └── bot/                    # All bot executable code
│       ├── main.py             # Entry point - run this to start the bot
│       ├── config/             # Configuration files
│       │   ├── paths.py        # File path definitions
│       │   └── env.py          # Environment variable loading
│       ├── operations/         # Data file operations
│       │   ├── operation.py    # Abstract base class for JSONL operations
│       │   ├── user_param_operation.py      # User data operations
│       │   └── user_transaction_operation.py # Transaction operations
│       ├── navigator/          # Bot navigation system
│       │   ├── bot_navigator.py    # Abstract navigator class
│       │   ├── vpn_navigator.py    # Concrete VPN bot navigator
│       │   └── modules/        # Navigation module JSON files
│       │       ├── basic.json
│       │       ├── settings.json
│       │       ├── transactions.json
│       │       └── subscriptions.json
│       └── handlers/           # Command and callback handlers
│           └── commands.py     # Command handlers (/start, /help)
├── data/                       # Data files (JSONL format)
│   ├── users.jsonl            # All user data
│   └── transactions.jsonl     # All transaction data
├── .secret/                    # Secret files (NEVER commit!)
│   └── env/
│       ├── bot.env             # Your bot token (create this)
│       └── bot.env.example     # Example file
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Bot Token

1. Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram
2. Copy the example environment file:
   ```bash
   cp .secret/env/bot.env.example .secret/env/bot.env
   ```
3. Edit `.secret/env/bot.env` and add your bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ```

### 3. Run the Bot

```bash
python -m src.bot.main
```

Or if you're in the `src/bot/` directory:
```bash
python main.py
```

## Data Storage

### JSONL Format

The bot uses **JSONL (JSON Lines)** format for data storage:
- Each line is a separate JSON object
- More efficient for large datasets
- Allows append-only writes for new records
- Files: `data/users.jsonl` and `data/transactions.jsonl`

### Example JSONL Structure

**users.jsonl:**
```jsonl
{"user_id": 123456, "username": "john_doe", "first_name": "John", "last_name": "Doe", "active_subscriptions": []}
{"user_id": 789012, "username": "jane_smith", "first_name": "Jane", "last_name": "Smith", "active_subscriptions": [{"id": "sub1", "plan": "premium"}]}
```

**transactions.jsonl:**
```jsonl
{"user_id": 123456, "id": "txn1", "amount": 9.99, "status": "completed", "timestamp": "2024-01-01T00:00:00Z"}
{"user_id": 789012, "id": "txn2", "amount": 19.99, "status": "pending", "timestamp": "2024-01-02T00:00:00Z"}
```

## Key Design Decisions

### Why `src/bot/` structure?
- **Separation of concerns**: All bot code in one place
- **Scalability**: Easy to add other components (e.g., `src/api/`, `src/admin/`)
- **Best practice**: Common Python project structure

### Why JSONL instead of individual JSON files?
- **Efficiency**: Better for datasets with many users
- **Simplicity**: Single file per data type
- **Performance**: Append-only writes are faster
- **Note**: For very large datasets (10k+ users), consider a database later

### Why `.secret/` folder?
- **Security**: Keeps secrets separate from code
- **Git safety**: `.gitignore` prevents accidental commits
- **Organization**: Clear separation of sensitive data

## Development

### Adding New Commands

1. Add handler function in `src/bot/handlers/commands.py`
2. Register in `src/bot/main.py`:
   ```python
   application.add_handler(CommandHandler("command", command_handler))
   ```

### Adding New Navigation Modules

1. Create JSON file in `src/bot/navigator/modules/`
2. Define buttons structure
3. Handle callbacks in `VPNBotNavigator.handle_callback()`

## License

[Your License Here]
