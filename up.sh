#!/bin/bash

# Check if can0 is up
if ! ip link show up | grep -q can0; then
    echo "Bringing up can0..."

    # Load CAN related modules
    sudo modprobe can
    sudo modprobe can_raw

    # Set the bitrate for can0
    sudo ip link set can0 type can bitrate 5000000

    # Bring up can0 interface
    sudo ip link set up can0

    echo "can0 setup complete."
else
    echo "can0 is already up."
fi
