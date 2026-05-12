#!/bin/bash
export LD_LIBRARY_PATH="/home/bolla/.local/lib/python3.12/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH}"
exec python3 /home/bolla/workspace/scripts/mission_control_api.py "$@"
