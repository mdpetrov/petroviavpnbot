"""Main entry point for the Petrovia VPN Telegram Bot."""

import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from .config.env import BOT_TOKEN
from .navigator.vpn_navigator import VPNBotNavigator
from .handlers.commands import start_command, help_command
from .handlers.messages import get_message_handler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to start the bot."""
    # Initialize bot navigator
    # Modules directory is relative to this file's location
    modules_dir = Path(__file__).parent / "navigator" / "modules"
    navigator = VPNBotNavigator(modules_dir)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Store navigator in bot_data
    application.bot_data['navigator'] = navigator
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(navigator.handle_callback))
    # Message handler for auto-creating users (must be last to not interfere with commands)
    application.add_handler(get_message_handler())
    
    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
