from writer_control_grpc_py import writer_control_pb2_grpc


class WriterControlService(writer_control_pb2_grpc.WriterControlServicer):
    def __init__(self):
        self.recording_flag = False
        self.pause_flag = False

    async def record_data(self, filename):
        while self.recording_flag:
            while self.pause_flag:
                await asyncio.sleep(1)
            # Simulate recording data by writing to a file
            with open(filename, 'a') as file:
                file.write("Recording data...\n")
                await asyncio.sleep(1)

    async def ControlRecording(self, request, context):
        if request.start:
            if not self.recording_flag:
                print("Starting recording...")
                self.recording_flag = True
                asyncio.create_task(self.record_data('recorded_data.txt'))
            else:
                print("Recording is already in progress.")
        elif request.pause:
            if self.recording_flag and not self.pause_flag:
                print("Pausing recording...")
                self.pause_flag = True
            elif not self.recording_flag:
                print("No active recording to pause.")
            else:
                print("Recording is already paused.")
        elif request.stop:
            if self.recording_flag:
                print("Stopping recording...")
                self.recording_flag = False
                self.pause_flag = False
            else:
                print("No active recording to stop.")

        return recording_pb2.RecordingControlResponse(status="OK")
