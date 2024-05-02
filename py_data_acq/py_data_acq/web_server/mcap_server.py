import logging
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
from hypercorn.config import Config
from hypercorn.asyncio import serve
import requests

awsServerURL = 'http://54.243.4.174:8080'

class MCAPServer:
    def __init__(self, writer_command_queue: asyncio.Queue, writer_status_queue: asyncio.Queue, init_writing= True, init_filename = '.',host='192.168.203.1', port=6969, metadata_filepath=''):
        self.host = host
        self.port = port
        
        self.is_writing = init_writing
        self.cmd_queue = writer_command_queue
        self.status_queue = writer_status_queue
        self.metadata_filepath = metadata_filepath
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

    async def start_stop_mcap_generation(self, input_cmd: bool, metadata=None):
        # logging.log("Starting/Stopping MCAP generation")
        await self.cmd_queue.put(MCAPFileWriterCommand(input_cmd, metadata))
        # logging.log("MCAP command put in queue")
        while True:
            # Wait for the next message from the queue
            # logging.log("getting start stop")
            message = await self.status_queue.get()
            if message.is_writing:
                # logging.log("Writing message to MCAP file")
                self.is_writing = True
                self.mcap_status_message = f"An MCAP file is being written: {message.writing_file}"
            else:
                # logging.log("Not Writing message to MCAP file")
                self.is_writing = False
                self.mcap_status_message = f"No MCAP file is being written."
                # Important: Mark the current task as done to allow the queue to proceed
            self.status_queue.task_done()

    def create_app(self):
        print("App Created")
        app = Flask(__name__)
        CORS(app)
        loop = asyncio.get_event_loop()


        @app.route('/start', methods=['POST'])
        def start_recording():
            print("Start route called")
            requestData = request.get_json()
            loop.create_task(self.start_stop_mcap_generation(input_cmd=True, metadata=requestData))
            return jsonify(message='success')

        @app.route('/stop', methods=['POST'])
        def stop_recording():
            loop.create_task(self.start_stop_mcap_generation(input_cmd=False))
            return jsonify(message='success')

        @app.route('/offload', methods=['POST'])
        def offload_data():
            path_to_mcap = "."
            if os.path.exists("/etc/nixos"):
                path_to_mcap = "/home/nixos/recordings"
            offload_data = checkOffloadedMCAPS()
            not_offloaded = (offload_data["not_offloaded"])
            print(not_offloaded)
            for filename in not_offloaded:
                if (os.path.exists(path_to_mcap + "/" + filename)):
                    MCAPfile = {'file': open(path_to_mcap + "/" + filename, 'rb')}
                    response = requests.post(awsServerURL + '/save_run', files = MCAPfile)
                    #print(response)
                    print(filename + " uploaded")
                else:
                    print("MCAP File directory , " + path_to_mcap + "/" + filename + " not found.")
            return jsonify(message='success')

        @app.route('/delete', methods=['POST'])
        def delete_data():
            path_to_mcap = "."
            if os.path.exists("/etc/nixos"):
                path_to_mcap = "/home/nixos/recordings"
            offload_data = checkOffloadedMCAPS()
            offloaded = (offload_data["offloaded"])
            for filename in offloaded:
                filePath = path_to_mcap + "/" + filename
                if os.path.exists(filePath):
                    os.remove(filePath) # one file at a time
                    print("Deleted " + filename)
                else:
                    print("MCAP File directory , " + filePath + " not found.")
            return jsonify(message='success')


        def checkOffloadedMCAPS():
            path_to_mcap = "."
            if os.path.exists("/etc/nixos"):
                path_to_mcap = "/home/nixos/recordings"
            queryParams = []
            for filename in os.listdir(path_to_mcap):
                if filename.endswith(".mcap"):
                    queryParams.append(filename)
            #queryParams = ["03_26_2024_23_10_23 1.mcap", "file2.mcap", "file3.mcap"] #for testing only
            queryString = ""
            for fileName in queryParams:
                queryString += "file=" + fileName + "&"
            queryString = queryString[:-1]
            response = requests.get(awsServerURL + '/get_offloaded_mcaps?' + queryString)
            return response.json()

        
        @app.route('/fields', methods=['GET'])
        def getJSON():
            try:
                if os.path.exists("/etc/nixos"):
                    with open (os.path.join(self.metadata_filepath, "metadata.json"), "r") as f:
                        data = json.load(f)
                    return jsonify(data)
                else:
                    with open (os.getcwd() +"/frontend_config/metadata.json", "r") as f:
                        data = json.load(f)
                    return jsonify(data)
            except FileNotFoundError:
                return jsonify({'error': 'File not found'}), 404

        return app

    async def start_server(self):
        print("Starting webserver")
        app = self.create_app()
        config = Config()
        config.bind = [f"{self.host}:{self.port}"]  # Set the bind address
        await serve(app, config)