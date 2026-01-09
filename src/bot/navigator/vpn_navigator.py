"""Concrete implementation of BotNavigator for VPN bot."""

from telegram import Update
from telegram.ext import ContextTypes
from .bot_navigator import BotNavigator
from ..operations import UserRepo


class VPNBotNavigator(BotNavigator):
    """Concrete implementation of BotNavigator for VPN bot."""
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries from inline buttons."""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        
        # Ensure user exists (handled by message handler, but ensure it exists)
        user_repo = UserRepo()
        user_repo.get_or_create(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        
        callback_data = query.data
        
        # Handle module navigation
        if callback_data.startswith("module_"):
            module_name = callback_data.replace("module_", "")
            keyboard = self.create_navigation_keyboard(module_name)
            
            if keyboard:
                await query.edit_message_text(
                    text=f"📋 {module_name.capitalize()} Menu",
                    reply_markup=keyboard
                )
            else:
                await query.edit_message_text(
                    text="❌ Module not found"
                )
        
        # Handle specific callbacks (to be implemented)
        else:
            await query.edit_message_text(
                text=f"Callback: {callback_data}\n\nThis feature is under development."
            )
    
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle commands from users."""
        user = update.effective_user
        
        # Ensure user exists (handled by message handler, but ensure it exists)
        user_repo = UserRepo()
        user_repo.get_or_create(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
