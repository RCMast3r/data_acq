#!/usr/bin/env bash
# You need to re-run this file anytime your package/package-lock.json changes
node2nix -16 --development \
    --input package.json \
    --lock package-lock.json \
    --node-env ./nix/node-env.nix \
    --composition ./nix/default.nix \
    --output ./nix/node-package.nix