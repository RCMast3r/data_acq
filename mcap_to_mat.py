import sys
from pathlib import Path
from mcap.reader import make_reader
from mcap_protobuf.reader import read_protobuf_messages
from mcap_protobuf.decoder import DecoderFactory
from scipy.io import savemat
 
def main():
    with open(sys.argv[1], "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        topics = []
        for channel in reader.get_summary().channels:
            topics.append(reader.get_summary().channels[channel].topic)
 
        mdict = {}
        for topic in topics:
            msg_dict = {}
            for schema, channel, message, proto_msg in reader.iter_decoded_messages(topics=[topic]):
                res = [f.name for f in proto_msg.DESCRIPTOR.fields]
                for name in res:
                    if name not in msg_dict:
                        msg_dict[name] = []
                    signal_data = [message.log_time, getattr(proto_msg, name)]  # No need for res[name], as name is already the field name
                    msg_dict[name].append(signal_data)
            mdict[topic] = msg_dict
 
        mdict = {"data": mdict}
 
        out_name = Path(sys.argv[1]).stem
        savemat(out_name+".mat", mdict, long_field_names=True)
 
 
 
if __name__ == "__main__":
    main()