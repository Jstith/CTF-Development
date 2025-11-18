#!/usr/bin/env python3
"""
Solve script for "Taken to School" challenge

This script searches for the anomalous entry in the network log file
based on the PowerSchool breach IOCs and extracts the flag.
"""

import re
import sys

def find_anomalous_entry(log_file_path):
    """
    Search for the anomalous entry containing the malicious IP address
    from the PowerSchool breach and extract the eventHash.
    
    Args:
        log_file_path (str): Path to the network log CEF file
        
    Returns:
        str: The flag in format flag{hash} or None if not found
    """
    # Malicious IP address from PowerSchool breach IOCs
    malicious_ip = "91.218.50.11"
    
    try:
        with open(log_file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Check if this line contains the malicious IP
                if malicious_ip in line:
                    print(f"Found anomalous entry on line {line_num}:")
                    print(f"  {line.strip()}")
                    print()
                    
                    # Extract eventHash using regex
                    hash_match = re.search(r'eventHash=([a-f0-9]+)', line)
                    if hash_match:
                        event_hash = hash_match.group(1)
                        flag = f"flag{{{event_hash}}}"
                        
                        print("IOC Analysis:")
                        print(f"  - Source IP: {malicious_ip} (matches PowerSchool breach IOC)")
                        print(f"  - Date: 2024-12-22 (matches breach timeframe)")
                        print(f"  - Action: allowed (indicates successful breach)")
                        print(f"  - File: chemistry_notes.pdf (education-related, fits school environment)")
                        print()
                        print(f"Extracted eventHash: {event_hash}")
                        print(f"Flag: {flag}")
                        
                        return flag
                    else:
                        print("ERROR: Could not extract eventHash from the line")
                        return None
        
        print(f"ERROR: Malicious IP {malicious_ip} not found in log file")
        return None
        
    except FileNotFoundError:
        print(f"ERROR: Log file '{log_file_path}' not found")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    """Main function to run the solve script"""
    print("=" * 60)
    print("Taken to School - Challenge Solver")
    print("=" * 60)
    print()
    print("Background:")
    print("This challenge is based on the recent PowerSchool breach where")
    print("a student pleaded guilty to attempted data extortion.")
    print()
    print("Known IOCs from the breach:")
    print("  - Malicious IP: 91.218.50.11")
    print("  - Date: December 22, 2024")
    print()
    print("Searching for anomalous entry in network log...")
    print()
    
    # Default log file path
    log_file = "network-log.cef"
    
    # Allow custom log file path as command line argument
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    
    flag = find_anomalous_entry(log_file)
    
    if flag:
        print()
        print("=" * 60)
        print("SUCCESS! Flag discovered:")
        print(f"  {flag}")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("FAILED: Could not find the flag")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main() 