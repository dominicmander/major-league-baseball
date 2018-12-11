import logging
import sys
import time

def setup_logging(log):
    """Set up logging for INFO verbosity to write to stdout"""

    # Configure logging settings
    format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    formatter = logging.Formatter(format)
    formatter.convert = time.gmtime
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Set verbosity
    log.setLevel(logging.INFO)

    # Set hander
    log.addHandler(stream_handler)

    log.info('Logger configured')
