

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

    def __init__(self, name="my_logger", log_dir="logs"):
        import logging
        import os
        import sys
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Get the script name (without extension)
        script_name = os.path.basename(sys.argv[0]).split(".")[0]

        # Create handlers for different log levels
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        for level in levels:
            log_filename = f"{script_name}_{logging.getLevelName(level).lower()}.log"
            handler = logging.FileHandler(os.path.join(log_dir, log_filename))
            handler.setLevel(level)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)

        # Suppress Pillow logs below WARNING
        pil_logger = logging.getLogger("PIL")
        pil_logger.setLevel(logging.WARNING)

    def get_logger(self):
        return self.logger