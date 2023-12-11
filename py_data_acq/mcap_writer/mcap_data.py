import sys
from mcap_protobuf.writer import Writer
import ht_data_pb2
import all_msgs_pb2
import google.protobuf.message_factory
def main():
    with open(sys.argv[1], "wb") as f, Writer(f) as mcap_writer:
        # for i in range(1, 11):
            # creation of the pre-encode message that we are about to send
            my_message = ht_data_pb2.ht_data()
            my_message.status = "ERROR"
            my_message.shock_fr = 12.23
            my_message.shock_fl = 12.23
            my_message.shock_br = 12.23
            my_message.shock_bl = 12.2

            # creation of the any message envelope that will hold each one of the packed messages
            an_any = all_msgs_pb2.hytech_msg()
            # pack pre-encode message
            an_any.message_pack.Pack(my_message)
            # create the id that will be used to differentiate between the messages to decode
            an_any.msg_id = my_message.DESCRIPTOR.name
            enc_msg = an_any.SerializeToString()
            # WIRE HERE LOL
            
            # creation of the receiver side any message that gets used to decode the messages into
            des_msg = all_msgs_pb2.hytech_msg()
            # decode msg from over the wire into generic message
            
            des_msg.ParseFromString(enc_msg)
            
            # go from decoded generic message into specific message based on the id
            
            # create a message class from the name of the message
            asdf = google.protobuf.message_factory.GetMessageClass(ht_data_pb2.DESCRIPTOR.message_types_by_name.get('ht_data'))
            
            if(des_msg.msg_id == ht_data_pb2.ht_data.DESCRIPTOR.name):
                msg = ht_data_pb2.ht_data()
                # the value in the message_pack is the binary encoded data which we can use for the foxglove webserver socket api
                print(des_msg.message_pack.value)
                # this unpacking will unpack the message into its container
                des_msg.message_pack.Unpack(msg)
            

            # mcap_writer.write_message(
            #     topic="/ht_data",
            #     message=ht_data,
            #     log_time=i * 1000,
            #     publish_time=i * 1000,
            # )


if __name__ == "__main__":
    main()