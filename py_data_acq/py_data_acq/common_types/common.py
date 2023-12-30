class QueueData():
    def __init__(self, schema_name: str, data: bytes):
        self.name = schema_name
        self.data = data