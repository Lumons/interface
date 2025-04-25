#!/usr/bin/env python3

import os
import time
import signal
import sys
from datetime import datetime
import subprocess

user_home = os.path.expanduser('~')

# Construct the path to the 'interface/audio_notes' directory within the user's home directory

# Dynamic path based on script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_OUTPUT_DIR = os.path.join(user_home, "repos/interface/audio_notes/logs/local")
STATE_FILE = os.path.join(SCRIPT_DIR, "recording_state.txt")
RECORDING_PROCESS = None  # Placeholder for the recording subprocess

def start_recording():
    """Starts the audio recording."""
    global RECORDING_PROCESS

    # Ensure the output directory exists
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.makedirs(AUDIO_OUTPUT_DIR)

    # File to save the recording
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio_file = os.path.join(AUDIO_OUTPUT_DIR, f"{timestamp}.wav")

    # Start the audio recording process (using `arecord` as an example)
    RECORDING_PROCESS = subprocess.Popen(
        ["arecord", "-f", "cd", "-t", "wav", "-d", "0", "-q", audio_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Save the recording state
    with open(STATE_FILE, "w") as f:
        f.write(str(RECORDING_PROCESS.pid))  # Save the PID of the recording process

    print(f"Recording started. Saving to {audio_file}.")

def stop_recording():
    """Stops the audio recording."""
    global RECORDING_PROCESS

    # Check if a recording process exists
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            pid = int(f.read().strip())  # Read the PID from the state file

        # Attempt to terminate the process
        try:
            os.kill(pid, signal.SIGTERM)
            print("Recording stopped.")
        except ProcessLookupError:
            print("Recording process not found. It may have already stopped.")

        # Clean up
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    else:
        print("No active recording to stop.")

def close_terminal():
    """Closes the terminal by sending SIGTERM to the parent process."""
    os.kill(os.getppid(), signal.SIGTERM)

def main():
    # Check if the script is currently recording
    if os.path.exists(STATE_FILE):
        # If recording, stop recording and close terminal
        stop_recording()
        close_terminal()
    else:
        # If not recording, start recording
        start_recording()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        stop_recording()
        sys.exit(0)
