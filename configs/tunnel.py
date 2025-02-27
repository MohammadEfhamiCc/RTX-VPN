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

def pbr():
    commands = [
        "ip tuntap add mode tun dev rtx || true",
        "ip addr add 198.18.0.1/15 dev rtx || true",
        "ip link set dev rtx up || true",
        "ip link set dev tap_softether down || true",
        "ip addr add 198.19.0.1/24 dev tap_softether || true",
        "ip link set dev tap_softether up || true",
        "ip route add 198.19.0.0/24 dev rtx table rtx_table || true",
        "ip route add default dev rtx table rtx_table || true",
        "ip rule add from 198.19.0.0/24 table rtx_table priority 10 || true",
        "ip rule add to 8.8.8.8 table main priority 11 || true",
        "ip rule add to 8.8.4.4 table main priority 12 || true",
    ]
    for cmd in commands:
        run_command(cmd)
    log("PBR setup completed")

def start_process(command, name):
    try:
        process = subprocess.Popen(command, shell=True)
        log(f"{name} started with PID {process.pid}")
        return process
    except Exception as e:
        log(f"Error starting {name}: {e}")
        sys.exit(1)

pbr()
rathole_process = start_process("/opt/rtxvpn_v2/tunnel/rathole /opt/rtxvpn_v2/tunnel/tunnel.toml", "Rathole")
tun2socks_process = start_process("/opt/rtxvpn_v2/tunnel/tun2socks -device rtx -proxy socks5://127.0.0.1:10808", "Tun2socks")
xray_process = start_process("/opt/rtxvpn_v2/tunnel/xray run -c /opt/rtxvpn_v2/tunnel/tunnel.json", "Xray")

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
