#!/usr/bin/env python
import time
import cantools
import os
import serial, pty


# TODO: Make this real (currently does not actually send data(?))
def main():
    # Open fake serial port
    snd, rev = pty.openpty()
    p_name = os.ttyname(snd)
    print("Opening on {}".format(p_name))
    ser = serial.Serial(p_name)

    print("Opened for on {}".format(ser))

    # Load DBC
    path_to_dbc = os.environ.get("DBC_PATH")
    full_path = os.path.join(path_to_dbc, "hytech.dbc")
    db = cantools.database.load_file(full_path)

    # Setup fake messages
    msg = db.get_message_by_name("MC1_TORQUE_COMMAND")
    rpm = db.get_message_by_name("MC4_SETPOINTS_COMMAND")

    # Serialize the message to bytes
    data = msg.encode({"torque_command": 100})
    rpm_set = 100

    while 1:
        # Iterate example vals
        rpm_set = rpm_set + 1

        # Send the guy
        ser.write(bytearray(msg.frame_id) + b"," + data)

        # make new message with new data
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
        ser.write(bytearray(rpm.frame_id) + b"," + rpm_data)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
