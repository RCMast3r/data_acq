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
        
        msgs_lists = []
        for topic in topics:
            msgs = []
            for schema, channel, message, proto_msg in reader.iter_decoded_messages(topics=[topic]):
                
                
                res = [f.name for f in proto_msg.DESCRIPTOR.fields]
                msg = {}
                msg["recvd_time"] = message.log_time
                for name in res:    
                    msg[name] = getattr(proto_msg, name)
                msgs.append(msg)
            msgs_lists.append(msgs)
        mdict= {}
        for index, topic in enumerate(topics):
            mdict[topic] = msgs_lists[index]
        out_name = Path(sys.argv[1]).stem
        savemat(out_name+".mat", mdict, long_field_names=True)



if __name__ == "__main__":
    main()