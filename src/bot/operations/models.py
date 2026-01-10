"""Data models for users and transactions."""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Literal

class BaseModel:
    """Base data model."""
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BaseModel':
        """Create BaseModel from dictionary."""
        # Parse ISO format datetime
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        return cls(**data)

@dataclass
class User(BaseModel):
    """User data model."""
    id: int  # Telegram user ID
    created_at: datetime
    username: str
    first_name: str
    last_name: str
    

@dataclass
class VPNKey(BaseModel):
    """Key data model."""
    id: str
    user_id: int
    type: Literal["vless", "outline"]
    value: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True

@dataclass
class Transaction(BaseModel):
    """Transaction data model."""
    id: str
    user_id: int
    created_at: datetime
    
