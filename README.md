## [English](/README.md) | [فارسی](/README_fa.md)
# RTX-VPN v2 + SoftEther
# L2TP/OpenVPN/SSTP Server with Rathole + Tun2socks + Xray + Tunnel + SoftEther
# RTX-VPN = (Rathole-tun2socks-Xray) VPN
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/menu.png)

## What Does this script do?
This script provides a solution for setting up L2TP/OpenVPN/SSTP server via "SoftEther" and tunnel via "Rathole+Tun2socks+Xray" in restricted locations (e.g., Iran, China).

## Supported Protocols
- L2TP
- L2TP/IPSec
- OpenVPN
- SSTP
- Radius (For Advanced Account Management)

## Diagram
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/diagram.png)

## How does it work?
We need two servers: one for incoming L2TP/OpenVPN/SSTP connections and SoftEther to deploy and the other as the endpoint of our connection. The first server (Tunnel Server) will be considered a server with no limit on incoming L2TP/OpenVPN/SSTP traffic, unlike the Edge Server, which we cannot connect to directly.

The Edge Server establishes the first connection to the Tunnel Server in reverse tunnel(rathole) via a VLESS + WebSocket (WS) configuration from Xray-core, exposing a SOCKS5 proxy on the Tunnel Server. We then use tun2socks to route traffic from the SOCKS5 proxy into a virtual interface.

Finally, we use Policy-Based Routing (PBR) to route SoftEther incoming connections to the tun2socks interface.

## Donate
🔹USDT-TRC20: ```THuvCFh7Epk926fs23ew6NPFShMrnagVxx```

🔹TRX: ```THuvCFh7Epk926fs23ew6NPFShMrnagVxx```

🔹LTC: ```ltc1quah8ej7ukez53wykehpeew7spya0kzx59r6nfk```

🔹BTC: ```bc1qe7z26fhd47xwezp25vk44e8e925ee43txdnfdp```

🔹ETH: ```0x7Bb6CfF428F75b468Ea49657D345Efc45C7104C9```

## Installation Tutorial
SOON

## Installation
```bash
sh -c "$(wget https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/v2/rtxvpn_v2.sh -O -)"
```

## Supported OS
This script can be run on all Debian-based distributions that use systemd

## Speedtest
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/speedtest.jpg)

## Fix OpenVPN Connection Error
The OpenVPN client configuration file provided by SoftEther uses an outdated cipher. To fix this issue, please add the following line below ```cipher AES-128-CBC``` in your configuration file:
```bash
data-ciphers AES-128-CBC:AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305
```
Additionally, it is recommended to replace ```remote address``` with your actual IP or personal domain

## Recommended SoftEther Configuration
- Disable DDNS: ```declare DDnsClient: bool Disabled true```
- Disable WebUI: ```bool DisableJsonRpcWebApi true```
- Remove Unnecessary Ports
  
## Tunnel Tweaking: Xray-Core
This script uses 'VLESS + WS' as the default connection for Xray-core. You can configure your desired settings in ```/opt/rtxvpn_v2/edge/edge.json``` for the Edge Server and ```/opt/rtxvpn_v2/tunnel/tunnel.json``` for the Tunnel Server

## Tunnel Tweaking: Rathole
You can also modify the Rathole configuration in ```/opt/rtxvpn_v2/edge/edge.toml``` for the Edge Server and ```/opt/rtxvpn_v2/tunnel/tunnel.toml``` for the Tunnel Server."

## Systemd Services: Edge Server
RTX-VPN (Rathole + Xray): ```rtxvpn.service```

## Systemd Services: Tunnel Server
RTX-VPN (Rathole + Tun2socks + Xray + PBR): ```rtxvpn.service```

SoftEther: ```softether.service```

Dnsmasq: ```dnsmasq.service```

## CopyRight
SoftEther: https://www.softether.org

Rathole: https://github.com/rapiz1/rathole

Tun2socks: https://github.com/bedefaced/vpn-install

Xray-Core: https://github.com/XTLS/Xray-core
