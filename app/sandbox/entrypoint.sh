#!/bin/bash

LOG_DIR="/analysis/logs"
SAMPLE="/analysis/sample"

mkdir -p $LOG_DIR

echo "[*] Starting sandbox analysis..."

if [ ! -f "$SAMPLE" ]; then
    echo "Sample not found"
    exit 1
fi

chmod +x "$SAMPLE" 2>/dev/null || true

# Start network capture (background)
tcpdump -i any -w $LOG_DIR/network.pcap > /dev/null 2>&1 &
TCPDUMP_PID=$!

# Start syscall tracing with timestamps
strace -ff -tt -o $LOG_DIR/strace.log "$SAMPLE" > $LOG_DIR/stdout.log 2>&1

# Stop tcpdump
kill $TCPDUMP_PID 2>/dev/null || true

echo "[*] Sandbox execution complete."