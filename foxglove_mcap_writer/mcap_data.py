import sys
from mcap_protobuf.writer import Writer
import ht_data_pb2
import all_msgs_pb2

def main():
    with open(sys.argv[1], "wb") as f, Writer(f) as mcap_writer:
        # for i in range(1, 11):
            my_message = ht_data_pb2.ht_data()
            my_message.status = "ERROR"
            my_message.shock_fr = 12.23
            my_message.shock_fl = 12.23
            my_message.shock_br = 12.23
            my_message.shock_bl = 12.23

            # Serialize the message to bytes
            an_any = all_msgs_pb2.hytech_msg()
            an_any.message_pack.Pack(my_message)
            an_any.msg_id = my_message.DESCRIPTOR.name
            enc_msg = an_any.SerializeToString()
            # WIRE HERE LOL
           
            
            des_msg = all_msgs_pb2.hytech_msg()
            des_msg.ParseFromString(enc_msg)

            if(des_msg.msg_id == ht_data_pb2.ht_data.DESCRIPTOR.name):
                print("yo")
                msg = ht_data_pb2.ht_data()
                des_msg.message_pack.Unpack(msg)
                print(msg.shock_bl)
            

            # mcap_writer.write_message(
            #     topic="/ht_data",
            #     message=ht_data,
            #     log_time=i * 1000,
            #     publish_time=i * 1000,
            # )


if __name__ == "__main__":
    main()