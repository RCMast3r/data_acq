import sys

from mcap_protobuf.reader import read_protobuf_messages

def main():
    for msg in read_protobuf_messages(sys.argv[1], log_time_order=False):
        print(f"{msg.topic}: {msg.proto_msg}")

if __name__ == "__main__":
    main()