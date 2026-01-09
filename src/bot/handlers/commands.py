"""Command handlers for the bot."""

from telegram import Update
from telegram.ext import ContextTypes
from ..operations import UserRepo
from ..navigator.bot_navigator import BotNavigator


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    
    # Get or create user (handled by message handler, but ensure it exists)
    user_repo = UserRepo()
    user_repo.get_or_create(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        last_name=user.last_name or ""
    )
    
    # Get bot navigator from context
    navigator: BotNavigator = context.bot_data.get('navigator')
    
    if navigator:
        keyboard = navigator.create_navigation_keyboard("basic")
        await update.message.reply_text(
            text=f"👋 Welcome, {user.first_name}!\n\n"
                 f"Welcome to Petrovia VPN Bot. Use the menu below to navigate:",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text="👋 Welcome! Bot navigator not initialized."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = """
🤖 Petrovia VPN Bot Help

Available commands:
/start - Start the bot and show main menu
/help - Show this help message

Use the inline buttons to navigate through:
• ⚙️ Settings - Manage your account settings
• 💳 Transactions - View your payment transactions
• 📦 Subscriptions - Manage your VPN subscriptions
"""
    await update.message.reply_text(help_text)
