"""Logging configuration for SAP Discovery with file rotation."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Configuration
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "sap_discovery.log"
MAX_BYTES = 10 * 1024 * 1024  # 10MB per file
BACKUP_COUNT = 5               # Keep 5 old files (50MB total max)


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create a configured logger with file and console handlers.

    Features:
    - Console output (stdout)
    - File output with automatic rotation
    - FIFO deletion when size limit reached

    Args:
        name: Logger name (usually __name__)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only add handlers if not already configured
    if not logger.handlers:
        # Create logs directory if it doesn't exist
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler (unchanged)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler with rotation (NEW!)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(level)

    return logger
