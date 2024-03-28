
class QueueData():
    def __init__(self, schema_name: str, msg):
        self.name = schema_name
        self.data = msg.SerializeToString()
        self.pb_msg = msg

class MCAPServerStatusQueueData():
    def __init__(self, writing_status: bool, writing_file: str):
        self.is_writing = writing_status
        self.writing_file = writing_file 

class MCAPFileWriterCommand():
    def __init__(self, write: bool, metadata=None):
        self.writing = write
        self.pb_metadata = metadata