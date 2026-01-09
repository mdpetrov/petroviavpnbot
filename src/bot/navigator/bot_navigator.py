"""Abstract base class for bot navigation and inline button handling."""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


class BotNavigator(ABC):
    """Abstract base class for handling bot navigation with inline buttons."""
    
    def __init__(self, modules_dir: Path):
        """
        Initialize BotNavigator.
        
        Args:
            modules_dir: Path to the directory containing module JSON files
        """
        self.modules_dir = modules_dir
        self._modules_cache: Dict[str, Dict[str, Any]] = {}
    
    def load_module(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a module configuration from JSON file.
        
        Args:
            module_name: Name of the module (without .json extension)
            
        Returns:
            Dictionary containing module configuration, or None if not found
        """
        if module_name in self._modules_cache:
            return self._modules_cache[module_name]
        
        module_path = self.modules_dir / f"{module_name}.json"
        try:
            if module_path.exists():
                with open(module_path, 'r', encoding='utf-8') as f:
                    module_data = json.load(f)
                    self._modules_cache[module_name] = module_data
                    return module_data
        except (json.JSONDecodeError, IOError) as e:
            logger.error(
                "Error loading module %s: %s",
                module_name,
                e,
                exc_info=True
            )
        
        return None
    
    def create_inline_keyboard(self, buttons_config: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard from button configuration.
        
        Args:
            buttons_config: List of button configurations, each containing:
                - text: Button text
                - callback_data: Callback data for the button
                - (optional) row: Row number (defaults to sequential)
                
        Returns:
            InlineKeyboardMarkup object
        """
        keyboard = []
        current_row = []
        
        for button_config in buttons_config:
            text = button_config.get("text", "")
            callback_data = button_config.get("callback_data", "")
            row = button_config.get("row", None)
            
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            
            if row is not None:
                # If row is specified, add current row if not empty and start new row
                if current_row:
                    keyboard.append(current_row)
                    current_row = []
                # Add button to specified row
                while len(keyboard) <= row:
                    keyboard.append([])
                keyboard[row].append(button)
            else:
                # Add to current row
                current_row.append(button)
        
        # Add remaining buttons in current_row
        if current_row:
            keyboard.append(current_row)
        
        return InlineKeyboardMarkup(keyboard)
    
    def create_navigation_keyboard(self, module_name: str, 
                                  additional_buttons: Optional[List[Dict[str, Any]]] = None) -> Optional[InlineKeyboardMarkup]:
        """
        Create navigation keyboard based on module configuration.
        
        Args:
            module_name: Name of the module to load
            additional_buttons: Optional list of additional buttons to append
            
        Returns:
            InlineKeyboardMarkup object, or None if module not found
        """
        module = self.load_module(module_name)
        if module is None:
            return None
        
        buttons = module.get("buttons", [])
        
        if additional_buttons:
            buttons = buttons + additional_buttons
        
        return self.create_inline_keyboard(buttons)
    
    def edit_message_keyboard(self, update: Update, module_name: str,
                             additional_buttons: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Edit message keyboard with new navigation.
        
        Args:
            update: Telegram Update object
            module_name: Name of the module to load
            additional_buttons: Optional list of additional buttons to append
            
        Returns:
            True if successful, False otherwise
        """
        keyboard = self.create_navigation_keyboard(module_name, additional_buttons)
        if keyboard is None:
            return False
        
        try:
            if update.callback_query:
                update.callback_query.edit_message_reply_markup(reply_markup=keyboard)
                return True
        except Exception as e:
            logger.error(
                "Error editing message keyboard: %s",
                e,
                exc_info=True
            )
        
        return False
    
    @abstractmethod
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle callback query from inline buttons.
        
        Args:
            update: Telegram Update object
            context: Context object
        """
        pass
    
    @abstractmethod
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle command from user.
        
        Args:
            update: Telegram Update object
            context: Context object
        """
        pass
