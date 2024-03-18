import socket
import asyncio
import json
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
import py_data_acq.common.protobuf_helpers as pb_helpers
from py_data_acq.common.common_types import MCAPServerStatusQueueData, MCAPFileWriterCommand
from typing import Any

class MCAPServer:
    def __init__(self, writer_command_queue: asyncio.Queue, writer_status_queue: asyncio.Queue, init_writing= True, init_filename = '.',host='0.0.0.0', port=6969):
        self.host = host
        self.port = port
        
        self.is_writing = init_writing
        self.cmd_queue = writer_command_queue
        self.status_queue = writer_status_queue
        
        if(init_writing):
            self.is_writing = True
            self.mcap_status_message = f"An MCAP file is being written: {init_filename}"
        else:
            self.is_writing = False
            self.mcap_status_message = "No MCAP file is being written."
        self.html_content = b"""<!DOCTYPE html>    
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCAP &#128064;</title>
    <script>
        function sendCommand(command) {
        fetch('/' + command, { method: 'POST' })
            .then(response => response.text())
            .then(data => {
                alert(data);
                setTimeout(updateStatus, 1000)
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Error sending command: ' + command);
            });
        }
        function updateStatus() {
            fetch('/status') // Assume '/status' endpoint returns the current MCAP status
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mcapStatus').innerText = data.statusMessage;
                    document.getElementById('startBtn').disabled = data.isRecording;
                    document.getElementById('stopBtn').disabled = !data.isRecording;
                });
        }
        document.addEventListener('DOMContentLoaded', function() {
            updateStatus();
        }, false);
    </script>
</head>
<body>
    <h1>MCAP Control Panel</h1>
    <button id="startBtn" onclick="sendCommand('start')">Start</button>
    <button id="stopBtn" onclick="sendCommand('stop')">Stop</button>
    <div id="mcapStatus">{{mcap_status}}</div>
</body>
</html>"""

    def __await__(self):
        async def closure():
            return self
        return closure().__await__()
    def __enter__(self):
        return self
    def __exit__(self, exc_, exc_type_, tb_):
        pass
    def __aenter__(self):
        return self
    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any):
        return self.stop_mcap_generation()
    
    # Creates page from inline html and updates with mcap_status
    async def serve_file(self):
        current_html_content = self.html_content.replace(b'{{mcap_status}}', self.mcap_status_message.encode())
        header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        return header + current_html_content
        
    async def start_stop_mcap_generation(self, input_cmd: bool):
        await self.cmd_queue.put(MCAPFileWriterCommand(input_cmd))
        while True:
            # Wait for the next message from the queue
            message = await self.status_queue.get()
            if message.is_writing:
                self.is_writing = True
                self.mcap_status_message = f"An MCAP file is being written: {message.writing_file}"
            else:
                self.is_writing = False
                self.mcap_status_message = f"No MCAP file is being written."
                # Important: Mark the current task as done to allow the queue to proceed
            self.status_queue.task_done()

    def handle_command(self, command):
        if command == '/start':
            asyncio.create_task(self.start_stop_mcap_generation(True))
            return "MCAP generation started."
        elif command == '/stop':
            asyncio.create_task(self.start_stop_mcap_generation(False))
            return "MCAP generation stopped."
        else:
            return "Command not recognized."

    # Checks if client connected and updates them on different actions
    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected with {addr}")
        
        data = await reader.read(1024)
        request = data.decode('utf-8').strip()
        method, url, _ = request.split(' ', 2)

        if method == 'POST':
            response_text = self.handle_command(url)
            response = (f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: text/plain\r\n\r\n"
                        f"{response_text}").encode('utf-8')
        elif url == '/status':
            status_response = {
                "statusMessage": self.mcap_status_message,
                "isRecording": self.is_writing 
            }
            response_bytes = json.dumps(status_response).encode('utf-8')
            response = (f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: application/json\r\n\r\n").encode('utf-8') + response_bytes
        else:
            response = await self.serve_file()

        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        
    async def start_server(self):
        url = f"http://{self.host}:{self.port}"
        print(f"MCAP Server started on {url}")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        async with server:
            await server.serve_forever()