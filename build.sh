#!/bin/sh
set -e

if command -v python3 >/dev/null 2>&1; then
    python3 -m venv ./.buildenv
else
    export PATH=/opt/runtime/python-3.6.3/bin:$PATH
    python3 -m venv ./.buildenv
fi
source ./.buildenv/bin/activate
./build.py $@
deactivate
