#!/usr/bin/env python
import signal
import time
import logging

from runner import *
from systemd.journal import JournalHandler

logger = logging.getLogger('data_acq_service')
logger.addHandler(JournalHandler())
logger.setLevel(logging.INFO)

def shutdown_handler(signum, frame):
    # Perform actions before shutdown (e.g., save data, close connections)
    
    logger.info("shutting down data acq system")
    # TODO enable communication with all of the tasks from here to enable clean shutdown
    

# Register the signal handler
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    asyncio.run(run(logger))