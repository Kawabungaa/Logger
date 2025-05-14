This is a class that builds on top of logging. It creates a log folder in the current directory with separate file for every log level. 
    
    Examples:

        import Logger
        log = Logger.get_logger().
        
        log.debug("Hello").
        log.info(f"Creating 'x' variable").
        log.warning(f"Current value of x: {x}").
        log.error("Invalid. Enter valid integer.").
        log.critical(f"We're not insured for this...").
