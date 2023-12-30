#!/usr/bin/env python
import socket
import time

from hytech_np_proto_py import hytech_pb2

# Define the IP and port for the UDP socket
UDP_IP = "127.0.0.1"
UDP_PORT = 12345


def main():
    # Create an instance of your message
    my_message = hytech_pb2.id_dashboard_status()
    my_message.start_button = True
    my_message.buzzer_active = False
    my_message.ssok_above_threshold = True
    my_message.shutdown_h_above_threshold = True
    my_message.mark_button = True
    my_message.mode_button = True
    my_message.motor_controller_cycle_button = True
    my_message.launch_ctrl_button_ = True
    my_message.torque_mode_button = True
    my_message.led_dimmer_button = True

    my_message.dial_state = "yo"
    my_message.ams_led = "yo"
    my_message.imd_led = "yo"
    my_message.mode_led = "yo"
    my_message.motor_controller_error_led = "yo"
    my_message.start_status_led = "yo"
    my_message.inertia_status_led = "yo"
    my_message.mechanical_brake_led = "yo"
    my_message.gen_purp_led = "yo"
    my_message.bots_led = "yo"
    my_message.cockpit_brb_led = "yo"
    my_message.crit_charge_led = "yo"
    my_message.glv_led = "yo"
    my_message.launch_control_led = "yo"

    # Serialize the message to bytes
    serialized_message = my_message.SerializeToString()

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while 1:
        time.sleep(0.2)
        try:
            # Send the serialized message over the UDP socket
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
