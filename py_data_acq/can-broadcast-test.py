#!/usr/bin/env python
import time
import can
import cantools
import os

# Define the IP and port for the UDP socket
bus1 = can.Bus(channel="vcan0", interface="socketcan")


def main():
    path_to_dbc = os.environ.get("DBC_PATH")
    full_path = os.path.join(path_to_dbc, "hytech.dbc")
    db = cantools.database.load_file(full_path)

    # Setup fake messages
    msg = db.get_message_by_name("MC1_TORQUE_COMMAND")
    rpm = db.get_message_by_name("MC4_SETPOINTS_COMMAND")

    # Serialize the message to bytes
    data = msg.encode({"torque_command": 100})
    msg = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)

    rpm_set = 100
    while 1:
        try:
            # Iterate example vals
            rpm_set = rpm_set + 1

            # Send the guy
            bus1.send(msg)

            # Serialize the message to bytes
            rpm_data = rpm.encode(
                {
                    "negative_torque_limit": 1,
                    "positive_torque_limit": 1,
                    "speed_setpoint_rpm": rpm_set,
                    "remove_error": 1,
                    "driver_enable": 1,
                    "hv_enable": 1,
                    "inverter_enable": 1,
                }
            )
            rpm_msg = can.Message(
                arbitration_id=rpm.frame_id, is_extended_id=False, data=rpm_data
            )
            bus1.send(rpm_msg)

            print("Message sent on {}".format(bus1.channel_info))
        except can.CanError:
            print("Message NOT sent!  Please verify can0 is working first")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
