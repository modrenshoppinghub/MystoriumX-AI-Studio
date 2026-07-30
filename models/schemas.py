"""
Utility functions and logging configuration for MystoriumX AI Studio.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "mystoriumx",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configures and returns a unified logger instance for studio engines.
    
    Args:
        name: Name of the logger module.
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
        log_file: Optional path to append log entries.

    Returns:
        logging.Logger: Pre-configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is instantiated multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
