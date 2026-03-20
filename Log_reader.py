
import subprocess

def get_log_stream():
    process = subprocess.Popen(
        ["journalctl", "-f"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process
