"""Message handler for auto-creating users."""

import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from ..operations import UserRepo

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming messages and auto-create users.
    
    This ensures every user who sends a message is automatically
    created in the database.
    """
    if not update.message or not update.effective_user:
        return
    
    user = update.effective_user
    user_repo = UserRepo()
    
    # Get or create user (creates if doesn't exist)
    user_repo.get_or_create(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        last_name=user.last_name or ""
    )
    
    logger.debug("Ensured user %s exists in database", user.id)


def get_message_handler() -> MessageHandler:
    """Get message handler for auto-creating users."""
    return MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
