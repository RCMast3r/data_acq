import socket
import asyncio
import json
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
from flask import Flask, request, jsonify
from flask_cors import CORS
import py_data_acq.common.protobuf_helpers as pb_helpers
from py_data_acq.common.common_types import MCAPServerStatusQueueData, MCAPFileWriterCommand
from typing import Any
import os

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

    def create_app(self):
        app = Flask(__name__)
        CORS(app)

        @app.route('/start', methods=['POST'])
        def start_recording():

            requestData = request.get_json()
            driver = requestData['driver']
            trackName = requestData['trackName']
            eventType = requestData['eventType']
            drivetrainType = requestData['drivetrainType']
            mass = requestData['mass']
            wheelbase = requestData['wheelbase']
            firmwareRev = requestData['firmwareRev']

            asyncio.create_task(self.start_stop_mcap_generation(True))
            return jsonify(message='success')

        @app.route('/stop', methods=['POST'])
        def stop_recording():
            asyncio.create_task(self.start_stop_mcap_generation(False))
            return jsonify()

        @app.route('/offload', methods=['POST'])
        def offload_data():
            # os.system("rsync -a ~/recordings urname@192.168.1.101:~/destination/of/data")
            return jsonify()

        return app

    async def start_server(self):
        app = self.create_app()
        app.run(host=self.host, port=self.port)