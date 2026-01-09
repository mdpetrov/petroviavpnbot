"""JSONL file handler with file locking for concurrent access."""

import fcntl
import json
import logging
import os
from pathlib import Path
from typing import List, TypeVar, Type, Optional

logger = logging.getLogger(__name__)

T = TypeVar('T')


class JSONLHandler:
    """Handles JSONL file operations with file locking."""
    
    def __init__(self, file_path: Path):
        """
        Initialize JSONL handler.
        
        Args:
            file_path: Path to the JSONL file
        """
        self.file_path = file_path
        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def read_all(self, model_class: Type[T]) -> List[T]:
        """
        Read all records from JSONL file.
        
        Args:
            model_class: Data class to deserialize into
            
        Returns:
            List of model instances
        """
        records = []
        if not self.file_path.exists():
            return records
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                try:
                    # Shared lock for concurrent reads
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    data = json.loads(line)
                                    records.append(model_class.from_dict(data))
                                except (json.JSONDecodeError, KeyError, TypeError) as e:
                                    logger.error(
                                        "Error parsing line in %s: %s",
                                        self.file_path,
                                        e,
                                        exc_info=True
                                    )
                                    continue
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (IOError, OSError) as e:
                    logger.warning(
                        "Could not acquire read lock for %s: %s",
                        self.file_path,
                        e
                    )
                    # Fallback: read without lock
                    f.seek(0)
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                data = json.loads(line)
                                records.append(model_class.from_dict(data))
                            except (json.JSONDecodeError, KeyError, TypeError) as e:
                                logger.error(
                                    "Error parsing line in %s: %s",
                                    self.file_path,
                                    e,
                                    exc_info=True
                                )
                                continue
        except IOError as e:
            logger.error(
                "Error reading JSONL file %s: %s",
                self.file_path,
                e,
                exc_info=True
            )
        
        return records
    
    def write_all(self, records: List[T]) -> bool:
        """
        Write all records to JSONL file (overwrites existing).
        
        Args:
            records: List of model instances to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Write to temp file first for atomic operation
            temp_file = self.file_path.with_suffix(self.file_path.suffix + '.tmp')
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                try:
                    # Exclusive lock for writes
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        for record in records:
                            if hasattr(record, 'to_dict'):
                                json_line = json.dumps(record.to_dict(), ensure_ascii=False)
                            else:
                                json_line = json.dumps(record, ensure_ascii=False)
                            f.write(json_line + '\n')
                        f.flush()
                        os.fsync(f.fileno())
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (IOError, OSError) as e:
                    logger.error(
                        "Could not acquire write lock for %s: %s",
                        temp_file,
                        e,
                        exc_info=True
                    )
                    # Fallback: write without lock
                    for record in records:
                        if hasattr(record, 'to_dict'):
                            json_line = json.dumps(record.to_dict(), ensure_ascii=False)
                        else:
                            json_line = json.dumps(record, ensure_ascii=False)
                        f.write(json_line + '\n')
                    f.flush()
                    os.fsync(f.fileno())
            
            # Atomic rename
            temp_file.replace(self.file_path)
            return True
        except (IOError, OSError, TypeError) as e:
            logger.error(
                "Error writing JSONL file %s: %s",
                self.file_path,
                e,
                exc_info=True
            )
            # Clean up temp file
            temp_file = self.file_path.with_suffix(self.file_path.suffix + '.tmp')
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass
            return False
    
    def append(self, record: T) -> bool:
        """
        Append a single record to JSONL file.
        
        Args:
            record: Model instance to append
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                try:
                    # Exclusive lock for append
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        if hasattr(record, 'to_dict'):
                            json_line = json.dumps(record.to_dict(), ensure_ascii=False)
                        else:
                            json_line = json.dumps(record, ensure_ascii=False)
                        f.write(json_line + '\n')
                        f.flush()
                        os.fsync(f.fileno())
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (IOError, OSError) as e:
                    logger.error(
                        "Could not acquire append lock for %s: %s",
                        self.file_path,
                        e,
                        exc_info=True
                    )
                    # Fallback: append without lock
                    if hasattr(record, 'to_dict'):
                        json_line = json.dumps(record.to_dict(), ensure_ascii=False)
                    else:
                        json_line = json.dumps(record, ensure_ascii=False)
                    f.write(json_line + '\n')
                    f.flush()
                    os.fsync(f.fileno())
            return True
        except (IOError, OSError, TypeError) as e:
            logger.error(
                "Error appending to JSONL file %s: %s",
                self.file_path,
                e,
                exc_info=True
            )
            return False
