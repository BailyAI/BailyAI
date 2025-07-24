import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE, ENABLE_LOGGING

def setup_logging():
    """Setup logging configuration for the bot"""
    if not ENABLE_LOGGING:
        return
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set up file handler
    log_file_path = os.path.join(log_dir, LOG_FILE)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True) 
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        handlers=[file_handler, console_handler],
        format=log_format,
        datefmt=date_format
    )
    
    # Set specific loggers
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("="*50)
    logger.info(f"Baily Bot logging initialized at {datetime.now().strftime(date_format)}")
    logger.info("="*50)

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)
