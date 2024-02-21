#!/bin/bash

# Check if vcan0 is already down
if ! ip link show up | grep -q vcan0; then
    echo "vcan0 is already down."
else
    echo "Bringing down vcan0..."

    # Bring down can0 interface
    sudo ip link set down vcan0

    echo "vcan0 has been brought down."
fi
