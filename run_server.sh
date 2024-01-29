#! /bin/bash
# nix develop --extra-experimental-features nix-command --extra-experimental-features flakes
sh -c 'python3 ./py_data_acq/broadcast-test.py' &
python3 ./py_data_acq/runner.py