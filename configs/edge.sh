#!/bin/bash
#MmD
log_file="/var/log/vpn-service.log"
pidfile="/var/run/vpn-service.pid"

log(){
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$log_file"
}

rathole(){
  /opt/rtxvpn_v2/edge/rathole /opt/rtxvpn_v2/edge/edge.toml &
  rathole_pid=$!
  if [ $? -ne 0 ]; then
    log "Error starting rathole"
    exit 1
  fi
  log "Rathole started with PID $rathole_pid"
}

xray(){
  /opt/rtxvpn_v2/edge/xray run -c /opt/rtxvpn_v2/edge/edge.json &
  xray_pid=$!
  if [ $? -ne 0 ]; then
    log "Error starting xray"
    exit 1
  fi
  log "Xray started with PID $xray_pid"
}

rathole &
xray &

echo "VPN Service Started" > "$log_file"

trap "log 'VPN Service interrupted'; kill $rathole_pid $tun2socks_pid $xray_pid; exit 1" SIGINT SIGTERM

wait

log "VPN Service finished"
