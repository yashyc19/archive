import logging
import colorlog
import sys
import os

# Define a custom log level
PING_LEVEL = 25
logging.addLevelName(PING_LEVEL, "PING")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class LogGen:
    @staticmethod
    def loggen():
        log_file_path = resource_path("..\\Logs\\Automation.log")
        
        # Check if the log file exists and create it if it doesn't
        if not os.path.isfile(log_file_path):
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            with open(log_file_path, 'w'): pass

        # Configure the logging format
        logging.basicConfig(filename=log_file_path,
                            format='%(asctime)s: %(levelname)s: %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p', 
                            force=True)

        # Create a logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Define a custom log handler for the custom level
        class PingHandler(logging.StreamHandler):
            def emit(self, record):
                if record.levelno == PING_LEVEL:
                    # Customize the format for the PING level log messages with color
                    self.formatter = colorlog.ColoredFormatter('PING: %(message)s', log_colors={'PING': 'purple'})
                super().emit(record)

        # Add the custom log handler to the logger
        logger.addHandler(PingHandler())

        return logger
