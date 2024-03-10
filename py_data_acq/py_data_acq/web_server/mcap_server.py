import socket
import asyncio
import json
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
from flask import Flask, request, jsonify
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

    async def start_mcap_generation(self, driver, trackName, eventType, carSetupId, drivetrainType, mass, wheelbase, firmwareRev):
        if self.mcap_writer is None:
            list_of_msg_names, msg_pb_classes = pb_helpers.get_msg_names_and_classes()
            self.mcap_writer = HTPBMcapWriter(self.path, list_of_msg_names, msg_pb_classes)
        self.mcap_status_message = f"An MCAP file is being written: {self.mcap_writer.writing_file.name}"

        await self.mcap_writer.write_metadata('driver', driver)
        await self.mcap_writer.write_metadata('trackName', trackName)
        await self.mcap_writer.write_metadata('eventType', eventType)
        await self.mcap_writer.write_metadata('carSetupId', carSetupId)
        await self.mcap_writer.write_metadata('drivetrainType', drivetrainType)
        await self.mcap_writer.write_metadata('mass', mass)
        await self.mcap_writer.write_metadata('wheelbase', wheelbase)
        await self.mcap_writer.write_metadata('firmwareRev', firmwareRev)

    async def stop_mcap_generation(self):
        if self.mcap_writer is not None:
            await self.mcap_writer.__aexit__(None, None, None)
            self.mcap_status_message = "No MCAP file is being written."
            self.mcap_writer = None

    def handle_command(self, command):
        if command == '/start':
            asyncio.create_task(self.start_stop_mcap_generation(True))
            return "MCAP generation started."
        elif command == '/stop':
            asyncio.create_task(self.start_stop_mcap_generation(False))
            return "MCAP generation stopped."
        else:
            return "Command not recognized."

    def create_app(self):
        app = Flask(__name__)

        @app.route('/start', methods=['POST'])
        def start_recording():

            requestData = request.get_json()
            driver = requestData['driver']
            trackName = requestData['trackName']
            eventType = requestData['eventType']
            carSetupId = requestData['carSetupId']
            drivetrainType = requestData['drivetrainType']
            mass = requestData['mass']
            wheelbase = requestData['wheelbase']
            firmwareRev = requestData['firmwareRev']

            asyncio.create_task(self.start_mcap_generation(driver, trackName, eventType, carSetupId, drivetrainType, mass, wheelbase, firmwareRev))
            return jsonify(message='success')

        @app.route('/stop', methods=['POST'])
        def stop_recording():
            return jsonify()

        return app

    async def start_server(self):
        app = self.create_app()
        app.run(host=self.host, port=self.port)