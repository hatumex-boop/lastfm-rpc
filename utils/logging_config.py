import logging
import sys
import os

class ColoredFormatter(logging.Formatter):
    """Custom logging formatter for vibrant and readable terminal output."""
    
    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': '\033[38;5;244m',    # Steel Grey
        'INFO': '\033[38;5;82m',      # Vibrant Green
        'WARNING': '\033[38;5;214m',   # Orange/Yellow
        'ERROR': '\033[38;5;196m',     # Bright Red
        'CRITICAL': '\033[1;37;41m',   # White on Red background
    }
    
    # Symbols for each level
    LEVEL_SYMBOLS = {
        'DEBUG': '[#]',
        'INFO': '[+]',
        'WARNING': '[!]',
        'ERROR': '[-]',
        'CRITICAL': '[X]',
    }
    
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def format(self, record):
        # Determine color and symbol
        level_color = self.COLORS.get(record.levelname, self.RESET)
        level_symbol = self.LEVEL_SYMBOLS.get(record.levelname, '[•]')
        
        # Format timestamp safely
        time_str = self.formatTime(record, "%H:%M:%S")
        
        # Truncate extremely long messages (like XML dumps) for terminal readability
        message = record.getMessage()
        if len(message) > 500:
            message = message[:500] + "... [TRUNCATED]"
            
        # Color certain parts of the message for better scanning
        log_fmt = (
            f"{self.COLORS['DEBUG']}[{time_str}]{self.RESET} "
            f"{level_color}{self.BOLD}{level_symbol} {record.levelname:<8}{self.RESET} "
            f"{self.COLORS['DEBUG']}[{record.name}]{self.RESET} "
            f"- {message}"
        )
        
        # Handle exceptions if they exist
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        
        if record.exc_text:
            log_fmt += f"\n{self.COLORS['ERROR']}{record.exc_text}{self.RESET}"
            
        return log_fmt

def setup_logging(level=logging.INFO):
    """Configures the enhanced logging for the application."""
    
    # Enable ANSI escape sequences on Windows if possible
    if sys.platform == 'win32':
        os.system('') # This is a trick to enable ANSI support in Windows CMD
    
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove existing handlers to avoid double logging
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    # Create console handler with our custom formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    
    # Silence noisy external libraries
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("pylast").setLevel(logging.WARNING)
    logging.getLogger("pypresence").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pystray").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logger
