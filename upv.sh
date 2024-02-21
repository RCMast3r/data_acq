#!/bin/bash

# Check if can0 is up
if ! ip link show up | grep -q can0; then
    echo "Bringing up vcan0..."

    # Load CAN related modules
    sudo modprobe vcan

    # Setup the faux can
    sudo ip link add dev vcan0 type vcan

    # Bring up can0 interface
    sudo ip link set up vcan0

    echo "vcan0 setup complete."
else
    echo "vcan0 is already up."
fi
