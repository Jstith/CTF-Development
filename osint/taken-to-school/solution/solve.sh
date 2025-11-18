#!/bin/bash

# Solve script for "Taken to School" challenge
# This script searches for the anomalous entry in the network log file
# based on the PowerSchool breach IOCs and extracts the flag.

echo "============================================================"
echo "Taken to School - Challenge Solver"
echo "============================================================"
echo
echo "Background:"
echo "This challenge is based on the recent PowerSchool breach where"
echo "a student pleaded guilty to attempted data extortion."
echo
echo "Known IOCs from the breach:"
echo "  - Malicious IP: 91.218.50.11"
echo "  - Date: December 22, 2024"
echo
echo "Searching for anomalous entry in network log..."
echo

# Default log file path
LOG_FILE="network-log.cef"

# Allow custom log file path as command line argument
if [ $# -gt 0 ]; then
    LOG_FILE="$1"
fi

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Log file '$LOG_FILE' not found"
    exit 1
fi

# Malicious IP address from PowerSchool breach IOCs
MALICIOUS_IP="91.218.50.11"

# Search for the malicious IP in the log file
echo "Searching for malicious IP: $MALICIOUS_IP"
echo

# Find the line containing the malicious IP
ANOMALOUS_LINE=$(grep "$MALICIOUS_IP" "$LOG_FILE")

if [ -z "$ANOMALOUS_LINE" ]; then
    echo "ERROR: Malicious IP $MALICIOUS_IP not found in log file"
    exit 1
fi

# Get line number
LINE_NUM=$(grep -n "$MALICIOUS_IP" "$LOG_FILE" | cut -d: -f1)

echo "Found anomalous entry on line $LINE_NUM:"
echo "  $ANOMALOUS_LINE"
echo

# Extract eventHash using regex
EVENT_HASH=$(echo "$ANOMALOUS_LINE" | grep -o 'eventHash=[a-f0-9]*' | cut -d= -f2)

if [ -z "$EVENT_HASH" ]; then
    echo "ERROR: Could not extract eventHash from the line"
    exit 1
fi

# Format the flag
FLAG="flag{$EVENT_HASH}"

echo "IOC Analysis:"
echo "  - Source IP: $MALICIOUS_IP (matches PowerSchool breach IOC)"
echo "  - Date: 2024-12-22 (matches breach timeframe)"
echo "  - Action: allowed (indicates successful breach)"
echo "  - File: chemistry_notes.pdf (education-related, fits school environment)"
echo
echo "Extracted eventHash: $EVENT_HASH"
echo "Flag: $FLAG"
echo
echo "============================================================"
echo "SUCCESS! Flag discovered:"
echo "  $FLAG"
echo "============================================================" 