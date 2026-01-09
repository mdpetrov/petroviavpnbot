"""User repository for managing user data."""

import logging
from datetime import datetime, timezone
from typing import Optional
from .models import User
from .jsonl_handler import JSONLHandler
from ..config.paths import USERS_FILE

logger = logging.getLogger(__name__)


class UserRepo:
    """Repository for user operations."""
    
    def __init__(self):
        """Initialize user repository."""
        self.handler = JSONLHandler(USERS_FILE)
    
    def create(self, user_id: int, username: str, first_name: str, last_name: str) -> Optional[User]:
        """
        Create a new user.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            Created User instance, or None if user already exists
        """
        # Check if user already exists
        if self.find_by_id(user_id):
            logger.debug("User %s already exists", user_id)
            return None
        
        user = User(
            id=user_id,
            created_at=datetime.now(timezone.utc),
            username=username or "",
            first_name=first_name or "",
            last_name=last_name or ""
        )
        
        if self.handler.append(user):
            logger.info("Created user %s", user_id)
            return user
        
        logger.error("Failed to create user %s", user_id)
        return None
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Find user by ID.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User instance if found, None otherwise
        """
        users = self.handler.read_all(User)
        for user in users:
            if user.id == user_id:
                return user
        return None
    
    def remove(self, user_id: int) -> bool:
        """
        Remove a user by ID.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if user was removed, False otherwise
        """
        users = self.handler.read_all(User)
        original_count = len(users)
        users = [u for u in users if u.id != user_id]
        
        if len(users) < original_count:
            if self.handler.write_all(users):
                logger.info("Removed user %s", user_id)
                return True
            logger.error("Failed to remove user %s", user_id)
            return False
        
        logger.debug("User %s not found for removal", user_id)
        return False
    
    def get_or_create(self, user_id: int, username: str, first_name: str, last_name: str) -> User:
        """
        Get existing user or create new one.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            User instance (existing or newly created)
        """
        user = self.find_by_id(user_id)
        if user:
            return user
        
        # Create new user
        user = self.create(user_id, username, first_name, last_name)
        if user:
            return user
        
        # If create failed, try to find again (race condition handling)
        user = self.find_by_id(user_id)
        if user:
            return user
        
        # Last resort: return a temporary user object (shouldn't happen)
        logger.error("Failed to get or create user %s. Returning a temporary user object.", user_id)
        return User(
            id=user_id,
            created_at=datetime.now(timezone.utc),
            username=username or "",
            first_name=first_name or "",
            last_name=last_name or ""
        )
