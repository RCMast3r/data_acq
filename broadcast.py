import socket
import time
import py_data_acq.foxglove_live.ht_data_pb2 as ht_data_pb2 # Import the generated Python code from your .proto file


# Define the IP and port for the UDP socket
UDP_IP = "127.0.0.1"
UDP_PORT = 12345

def main():
    # Create an instance of your message
    my_message = ht_data_pb2.ht_data()
    my_message.status = "ERROR"
    my_message.shock_fr = 12.23
    my_message.shock_fl = 12.23
    my_message.shock_br = 12.23
    my_message.shock_bl = 12.23

    # Serialize the message to bytes
    serialized_message = my_message.SerializeToString()
     
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while(1):
        time.sleep(0.2)
        try:
            # Send the serialized message over the UDP socket
            my_message.shock_fr += 0.3
            serialized_message = my_message.SerializeToString()
            sock.sendto(serialized_message, (UDP_IP, UDP_PORT))
            print(f"Message sent to {UDP_IP}:{UDP_PORT}")
        except KeyboardInterrupt:
            # Handle Ctrl+C to exit the loop gracefully
            sock.close()
            break
        except Exception as e:
            print(f"Error sending message: {e}")
        # finally:
            # sock.close()

if __name__ == "__main__":
    main()
   