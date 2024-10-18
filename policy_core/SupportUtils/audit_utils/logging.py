import logging

logging.getLogger("py4j.java_gateway").setLevel(logging.ERROR)

class CustomLogger:
    """
    A custom logging utility class to create and configure Python loggers with a specified 
    log level and format.

    Attributes:
    -----------
    name : str
        The name of the logger, typically the module's `__name__`.
    level : str
        The log level to be set for the logger. It must be one of "INFO", "DEBUG", "WARNING", or "ERROR".
    format : str, optional
        The format string for log messages, which defines how the log entries will appear. 
        Default format: "%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s | %(message)s".
    """
    
    def __init__(self, name: str, level: str, format: str = "%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s | %(message)s"):
        """
        Initializes the CustomLogger instance with a name, log level, and log message format.

        Parameters:
        -----------
        name : str
            The name of the logger, usually the name of the module.
        level : str
            The log level to use for the logger. Must be one of: "INFO", "DEBUG", "WARNING", or "ERROR".
        format : str, optional
            A string representing the format for log messages. The default format includes
            timestamp, log level, filename, function name, and the log message.
        """
        self.name = name
        self.level = level
        self.format = format
        
    def create_logger(self):
        """
        Creates and configures a logger instance based on the provided log level and format.

        The method validates the log level, sets up a stream handler, applies the custom log format, 
        and returns the configured logger.

        Returns:
        --------
        logger : logging.Logger
            A logger instance configured with the specified name, level, and message format.

        Raises:
        -------
        AssertionError:
            If the log level is not one of "INFO", "DEBUG", "WARNING", or "ERROR".
        """
        assert self.level in ["INFO", "DEBUG", "WARNING", "ERROR"], "Illegal log level"
        
        logger = logging.getLogger(self.name)
        
        # Set log level based on the user's input
        if self.level == "DEBUG":
            logger.setLevel(logging.DEBUG)
        elif self.level == "INFO":
            logger.setLevel(logging.INFO)
        elif self.level == "WARNING":
            logger.setLevel(logging.WARNING)
        elif self.level == "ERROR":
            logger.setLevel(logging.ERROR)

        # Add a stream handler for outputting logs to the console
        ch = logging.StreamHandler()
        logger.addHandler(ch)
        
        # Set the custom format for the logger
        formatter = logging.Formatter(self.format)
        ch.setFormatter(formatter)

        return logger

# Example of usage
logger_cls = CustomLogger(__name__, "INFO")
logger = logger_cls.create_logger()
