#!/bin/bash

SAMPLE_PATH="/analysis/sample"
LOG_DIR="/analysis/logs"

mkdir -p $LOG_DIR

if [ ! -f "$SAMPLE_PATH" ]; then
    echo "[-] No sample provided at $SAMPLE_PATH"
    exit 1
fi

FILE_TYPE=$(file $SAMPLE_PATH)

echo "[*] Sample type: $FILE_TYPE"

echo "[*] Starting strace monitoring..."

if [[ $FILE_TYPE == *"ELF"* ]]; then
    strace -ff -o $LOG_DIR/strace.log $SAMPLE_PATH &
elif [[ $FILE_TYPE == *"shell script"* ]]; then
    strace -ff -o $LOG_DIR/strace.log bash $SAMPLE_PATH &
else
    echo "[!] Unsupported file type for execution."
    exit 1
fi

TRACE_PID=$!

echo "[*] Monitoring for 30 seconds..."
sleep 30

echo "[*] Stopping monitoring..."
kill -9 $TRACE_PID 2>/dev/null

echo "[*] Analysis complete."

exit 0