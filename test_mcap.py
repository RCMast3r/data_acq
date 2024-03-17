import sys

from mcap_protobuf.reader import read_protobuf_messages

def main():
    for msg in read_protobuf_messages("/home/ben/hytech_mcaps/recordings/03_17_2024_01_34_00_fixed.mcap", log_time_order=False):
        print(f"{msg.topic}: {msg.proto_msg}")

if __name__ == "__main__":
    main()