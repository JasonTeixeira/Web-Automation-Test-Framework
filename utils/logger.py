"""
Custom logger with color-coded output and file logging.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

import colorlog

from config import settings


class TestLogger:
    """Custom logger for test framework with color support."""
    
    _loggers: dict[str, logging.Logger] = {}
    
    @classmethod
    def get_logger(cls, name: str = "test_framework") -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, settings.log_level))
        logger.propagate = False
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.log_level))
        
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)-8s]%(reset)s %(blue)s%(name)s%(reset)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = settings.logs_path
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / f"{name}.log", mode='a')
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s - %(message)s (%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger


# Convenience function
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (defaults to caller's module name)
        
    Returns:
        Configured logger instance
    """
    if name is None:
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get('__name__', 'test_framework')
    
    return TestLogger.get_logger(name or 'test_framework')
