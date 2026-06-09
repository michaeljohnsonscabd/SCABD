import sys
import os
import time

def get_resource_heartbeat():
    """
    Returns system resource usage.
    Uses psutil if available, otherwise falls back to basic metrics.
    """
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        return {"cpu_usage": cpu, "memory_usage": mem, "status": "OPTIMAL"}
    except ImportError:
        # Fallback for systems without psutil
        # In a real Ubuntu environment, we could parse /proc/stat or /proc/meminfo
        return {"cpu_usage": 0.0, "memory_usage": 0.0, "status": "MONITORING_LIMITED"}

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
