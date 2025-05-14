




import logging
import os
import sys
import json
import threading
from functools import wraps
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

# Initialize colorama for colored console output
init(autoreset=True)

class Logger:
    """This is a class that builds on top of logging. It creates a log folder in the current directory with separate file for every log level. 
    
    Examples:
     
        log = Logger.get_logger().
        log.debug("Hello").
        log.info(f"Creating 'x' variable").
        log.warning(f"Current value of x: {x}").
        log.error("Invalid. Enter valid integer.").
        log.critical(f"We're not insured for this...").

    """
    def __init__(self, name="my_logger", log_dir="logs", max_size=5_000_000, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Get the script name (without extension)
        script_name = os.path.basename(sys.argv[0]).split(".")[0]

        # Define log levels and colors
        self.levels = {
            "debug": (logging.DEBUG, Fore.BLUE),
            "info": (logging.INFO, Fore.GREEN),
            "warning": (logging.WARNING, Fore.YELLOW),
            "error": (logging.ERROR, Fore.RED),
            "critical": (logging.CRITICAL, Fore.MAGENTA)
        }

        # Create handlers for different log levels with rotation
        for level_name, (level, _) in self.levels.items():
            log_filename = f"{script_name}_{level_name}.log"
            handler = RotatingFileHandler(os.path.join(log_dir, log_filename), maxBytes=max_size, backupCount=backup_count)
            handler.setLevel(level)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)

        # Console Handler with color
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)

    def _log_async(self, level, msg):
        """Logs messages asynchronously."""
        threading.Thread(target=lambda: self.logger.log(level, msg), daemon=True).start()

    def _log_json(self, level, msg):
        """Logs messages in JSON format."""
        log_entry = json.dumps({"level": logging.getLevelName(level), "message": msg})
        self._log_async(level, log_entry)

    def _log_colored(self, level, msg):
        """Logs messages with color in the console."""
        color = self.levels[logging.getLevelName(level).lower()][1]
        self._log_async(level, f"{color}{msg}{Style.RESET_ALL}")

    # Shortened logging methods with JSON and color support
    def d(self, msg): self._log_json(logging.DEBUG, msg); self._log_colored(logging.DEBUG, msg)
    def i(self, msg): self._log_json(logging.INFO, msg); self._log_colored(logging.INFO, msg)
    def w(self, msg): self._log_json(logging.WARNING, msg); self._log_colored(logging.WARNING, msg)
    def e(self, msg): self._log_json(logging.ERROR, msg); self._log_colored(logging.ERROR, msg)
    def c(self, msg): self._log_json(logging.CRITICAL, msg); self._log_colored(logging.CRITICAL, msg)

    # Decorator for logging function calls
    def __call__(self, level="info"):
        """Decorator to log function entry, exit, and errors."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self._log_json(getattr(logging, level.upper()), f"Entering: {func.__name__} with args={args}, kwargs={kwargs}")
                try:
                    result = func(*args, **kwargs)
                    self._log_json(getattr(logging, level.upper()), f"Exiting: {func.__name__} with result={result}")
                    return result
                except Exception as e:
                    self._log_json(logging.ERROR, f"Error in {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator

# Global logger instance
log = Logger()