#!/usr/bin/env python
import time
import can
import math
import os
from cantools import database

# Define the bus to yap on
bus1 = can.Bus(channel="vcan0", interface="socketcan")


def generate_sine_wave(amplitude, frequency, phase_shift, time_variable):
    return amplitude * math.sin(2 * math.pi * frequency * time_variable + phase_shift)


def main():
    # Load DBC into
    path_to_dbc = os.environ.get("DBC_PATH")
    full_path = os.path.join(path_to_dbc, "car.dbc")
    db = database.load_file(full_path)

    # Setup fake message
    rpm = db.get_message_by_name("M165_Motor_Position_Info")

    rpm_set = 100
    while 1:
        try:
            # Iterate example vals
            rpm_set = rpm_set + 1

            # Serialize the message to bytes
            rpm_set = generate_sine_wave(3000, 1, 90, time.time()) + 3000
            rpm_data = rpm.encode(
                {
                    "D4_Delta_Resolver_Filtered": int(1),
                    "D3_Electrical_Output_Frequency": int(1),
                    "D2_Motor_Speed": rpm_set,
                    "D1_Motor_Angle_Electrical": int(1),
                }
            )
            rpm_msg = can.Message(
                arbitration_id=rpm.frame_id, is_extended_id=False, data=rpm_data
            )
            bus1.send(rpm_msg)

            # print("Message sent on {}".format(bus1.channel_info))
        except can.CanError:
            print("Message NOT sent!  Please verify can0 is working first")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
