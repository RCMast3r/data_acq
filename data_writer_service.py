import signal
import time
import logging
from systemd.journal import JournalHandler

log = logging.getLogger('demo')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

def shutdown_handler(signum, frame):
    # Perform actions before shutdown (e.g., save data, close connections)
    
    log.info("shutting down")
    # Your shutdown logic here

# Register the signal handler
signal.signal(signal.SIGINT, shutdown_handler)

# Your main script logic here
while True:
    # Service main loop
    time.sleep(1)
    log.info("sent to journal")