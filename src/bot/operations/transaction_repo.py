"""Transaction repository for managing transaction data."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional, List
from .models import Transaction
from .jsonl_handler import JSONLHandler
from ..config.paths import TRANSACTIONS_FILE

logger = logging.getLogger(__name__)


class TransactionRepo:
    """Repository for transaction operations."""
    
    def __init__(self):
        """Initialize transaction repository."""
        self.handler = JSONLHandler(TRANSACTIONS_FILE)
    
    def create(self, user_id: int, transaction_id: Optional[str] = None) -> Optional[Transaction]:
        """
        Create a new transaction.
        
        Args:
            user_id: Telegram user ID
            transaction_id: Optional transaction ID (auto-generated if not provided)
            
        Returns:
            Created Transaction instance, or None on failure
        """
        if transaction_id is None:
            transaction_id = str(uuid.uuid4())
        
        transaction = Transaction(
            id=transaction_id,
            user_id=user_id,
            created_at=datetime.now(timezone.utc)
        )
        
        if self.handler.append(transaction):
            logger.info("Created transaction %s for user %s", transaction_id, user_id)
            return transaction
        
        logger.error("Failed to create transaction %s", transaction_id)
        return None
    
    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """
        Find transaction by ID.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Transaction instance if found, None otherwise
        """
        transactions = self.handler.read_all(Transaction)
        for transaction in transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def find_by_user_id(self, user_id: int) -> List[Transaction]:
        """
        Find all transactions for a user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            List of Transaction instances
        """
        transactions = self.handler.read_all(Transaction)
        return [t for t in transactions if t.user_id == user_id]
    
    def remove(self, transaction_id: str) -> bool:
        """
        Remove a transaction by ID.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            True if transaction was removed, False otherwise
        """
        transactions = self.handler.read_all(Transaction)
        original_count = len(transactions)
        transactions = [t for t in transactions if t.id != transaction_id]
        
        if len(transactions) < original_count:
            if self.handler.write_all(transactions):
                logger.info("Removed transaction %s", transaction_id)
                return True
            logger.error("Failed to remove transaction %s", transaction_id)
            return False
        
        logger.debug("Transaction %s not found for removal", transaction_id)
        return False
