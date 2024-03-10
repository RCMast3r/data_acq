import socket
import asyncio
import json
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
from flask import Flask, request, jsonify
import py_data_acq.common.protobuf_helpers as pb_helpers
from typing import Any
import os

class MCAPServer:
    def __init__(self, host='0.0.0.0', port=6969, mcap_writer=None,path='.'):
        self.host = host
        self.port = port
        self.mcap_writer = mcap_writer
        self.path = path
        if mcap_writer is not None:
            self.mcap_status_message = f"An MCAP file is being written: {self.mcap_writer.writing_file.name}"
        else:
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
            asyncio.create_task(self.start_mcap_generation())
            return "MCAP generation started."
        elif command == '/stop':
            asyncio.create_task(self.stop_mcap_generation())
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

        @app.route('/offload', methods=['POST'])
        def offload_data():
            os.system("rsync -a ~/dir/to/MCAP_file username@192.168.1.101:~/destination/of/data")
            return jsonify()

        return app

    async def start_server(self):
        app = self.create_app()
        app.run(host=self.host, port=self.port)