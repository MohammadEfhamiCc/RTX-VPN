#!/usr/bin/env python3
#MmD
import os
import subprocess
import signal
import time
import sys

log_file = "/var/log/vpn-service.log"
pidfile = "/var/run/vpn-service.pid"

def log(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {command} - {e}")

rathole_process = start_process("/opt/rtxvpn_v2/edge/rathole /opt/rtxvpn_v2/edge/edge.toml", "Rathole")
xray_process = start_process("/opt/rtxvpn_v2/edge/xray run -c /opt/rtxvpn_v2/edge/edge.json", "Xray")

log("VPN Service Started")

def shutdown_handler(signum, frame):
    """Handle shutdown signals."""
    log("VPN Service interrupted")
    for process in [rathole_process, tun2socks_process, xray_process]:
        if process:
            process.terminate()
    sys.exit(1)

# Register signal handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# Wait for processes
rathole_process.wait()
tun2socks_process.wait()
xray_process.wait()

log("VPN Service finished")
