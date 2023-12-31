import time
class QueueData():
    def __init__(self, schema_name: str, msg):
        self.name = schema_name
        self.data = msg.SerializeToString()
        self.pb_msg = msg
        self.time_received = int(time.time_ns())