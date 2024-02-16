from py_data_acq.web_server.mcap_server import MCAPServer

if __name__ == '__main__':
    server = MCAPServer()
    server.start_server()
