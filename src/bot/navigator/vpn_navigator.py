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
        
        # Handle specific callbacks
        handlers = {
            "keys_view": self.handle_keys_view,
            "keys_new": self.handle_keys_new,
            "keys_revoke": self.handle_keys_revoke,
        }
        handler = handlers.get(callback_data)
        if handler:
            await handler(update, context)
            return

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
    
    async def handle_keys_view(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle keys view command."""
        user = update.effective_user
        user_repo = UserRepo()
        user_repo.get_or_create(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        # keys = user_repo.get_keys(user_id=user.id)
        # await update.message.reply_text(
        #     text=f"🔑 Active Keys:\n\n{keys}"
        # )
        await update.message.reply_text(
            text="🔑 Active Keys:\n\nUnder development."
        )
    
    async def handle_keys_new(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle keys new command."""
        user = update.effective_user
        user_repo = UserRepo()
        user_repo.get_or_create(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        await update.message.reply_text(
            text="🔑 Add New Key:\n\nUnder development."
        )
    
    async def handle_keys_revoke(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle keys revoke command."""
        user = update.effective_user
        user_repo = UserRepo()
        user_repo.get_or_create(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
        await update.message.reply_text(
            text="🔑 Revoke Key:\n\nUnder development."
        )