"""Data models for users and transactions."""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class User:
    """User data model."""
    id: int  # Telegram user ID
    created_at: datetime
    username: str
    first_name: str
    last_name: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User from dictionary."""
        # Parse ISO format datetime
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        return cls(**data)


@dataclass
class Transaction:
    """Transaction data model."""
    id: str
    user_id: int
    created_at: datetime
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Create Transaction from dictionary."""
        # Parse ISO format datetime
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        return cls(**data)
