import sys
import os

def run_all():
    print("==================================================")
    print("[+] RUNNING SCABD INTERNAL DIAGNOSTICS MODULE")
    print("==================================================")
    
    # 1. Verify Python Version
    print(f"    [->] Python Runtime Engine: Version {sys.version.split()[0]}")
    
    # 2. Check for Absolute Core Files
    required_files = ['main.py', 'config/settings.py', 'core/engine.py']
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"    [✓] Component Verified: {file_path}")
        else:
            print(f"    [X] CRITICAL ERROR: Missing {file_path}")
            print("[!] Diagnostics Failed. Halting System Execution.")
            sys.exit(1)
            
    print("--------------------------------------------------")
    print("[✓] ALL SYSTEMS OPERATIONAL: SCABD Core Status: CLEAN")
    print("==================================================\n")
