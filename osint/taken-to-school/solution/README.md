# Taken to School - Solve Scripts

This directory contains solve scripts for the "Taken to School" challenge, which is based on the recent PowerSchool breach where a student pleaded guilty to attempted data extortion.

## Challenge Overview

The challenge involves analyzing a network log file (`network-log.cef`) to find an anomalous entry related to the PowerSchool breach. Based on open-source intelligence (OSINT), participants need to identify the malicious entry using known Indicators of Compromise (IOCs).

### Known IOCs from PowerSchool Breach:
- **Malicious IP**: `91.218.50.11`
- **Date**: December 22, 2024
- **Context**: Student data extortion scheme

## Available Solve Scripts

### 1. Python Script (`solve.py`)
```bash
# Run with default log file (network-log.cef)
python3 solve.py

# Run with custom log file path
python3 solve.py /path/to/logfile.cef
```

### 2. Bash Script (`solve.sh`)
```bash
# Run with default log file (network-log.cef)
./solve.sh

# Run with custom log file path
./solve.sh /path/to/logfile.cef
```

## What the Scripts Do

1. **Search for IOCs**: Look for the malicious IP address `91.218.50.11` in the network log
2. **Identify Anomalous Entry**: Find the log entry containing the breach indicators
3. **Extract Flag**: Parse the `eventHash` field from the anomalous entry
4. **Format Result**: Present the flag in the required format: `flag{hash}`

## Expected Output

Both scripts will display:
- Background information about the PowerSchool breach
- The anomalous log entry found
- IOC analysis explaining why this entry is suspicious
- The extracted eventHash
- The final flag

## Flag Format

The flag follows the format: `flag{5b16c7044a22ed3845a0ff408da8afa9}`

Where `5b16c7044a22ed3845a0ff408da8afa9` is the MD5 hash from the `eventHash` field of the anomalous log entry.

## Requirements

- **Python script**: Python 3.x (uses standard library only)
- **Bash script**: Standard Unix/Linux shell with `grep` and `cut` utilities
- **Log file**: `network-log.cef` (should be in the same directory or specify path)

## Challenge Solution Methodology

This challenge demonstrates real-world incident response techniques:

1. **OSINT Research**: Finding information about recent security breaches
2. **IOC Identification**: Extracting actionable indicators from threat reports
3. **Log Analysis**: Searching through security logs for known bad indicators
4. **Evidence Correlation**: Matching log entries to known attack patterns

The PowerSchool breach serves as a realistic scenario where participants must research current events and apply that knowledge to identify malicious activity in network logs. 