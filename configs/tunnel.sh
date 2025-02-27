#!/bin/bash
#MmD
log_file="/var/log/vpn-service.log"
pidfile="/var/run/vpn-service.pid"

log(){
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$log_file"
}

pbr(){
  ip tuntap add mode tun dev rtx || true
  ip addr add 198.18.0.1/15 dev rtx || true
  ip link set dev rtx up || true

  ip link set dev tap_softether down || true
  ip addr add 198.19.0.1/24 dev tap_softether || true
  ip link set dev tap_softether up || true

  ip route add 192.168.19.0/24 dev rtx table rtx_table || true
  ip route add default dev rtx table rtx_table || true
  ip rule add from 192.168.19.0/24 table rtx_table || true
  ip rule add to 8.8.4.4 table main || true
  ip rule add to 8.8.8.8 table main || true

  log "PBR setup completed"
}

rathole(){
  /opt/rtxvpn_v2/tunnel/rathole /opt/rtxvpn_v2/tunnel/tunnel.toml &
  rathole_pid=$!
  if [ $? -ne 0 ]; then
    log "Error starting rathole"
    exit 1
  fi
  log "Rathole started with PID $rathole_pid"
}

tun2socks(){
  /opt/rtxvpn_v2/tunnel/tun2socks -device rtx -proxy socks5://127.0.0.1:10808 &
  tun2socks_pid=$!
  if [ $? -ne 0 ]; then
    log "Error starting tun2socks"
    exit 1
  fi
  log "Tun2socks started with PID $tun2socks_pid"
}

xray(){
  /opt/rtxvpn_v2/tunnel/xray run -c /opt/rtxvpn_v2/tunnel/tunnel.json &
  xray_pid=$!
  if [ $? -ne 0 ]; then
    log "Error starting xray"
    exit 1
  fi
  log "Xray started with PID $xray_pid"
}

pbr &
rathole &
tun2socks &
xray &

echo "VPN Service Started" > "$log_file"

trap "log 'VPN Service interrupted'; kill $rathole_pid $tun2socks_pid $xray_pid; exit 1" SIGINT SIGTERM

wait

log "VPN Service finished"
