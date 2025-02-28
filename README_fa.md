## [English](/README.md) | [فارسی](/README_fa.md)
# RTX-VPN v2 + SoftEther
# L2TP/OpenVPN/SSTP Server with Xray + Rathole + tun2socks Tunnel + SoftEther
# RTX-VPN = (Rathole-tun2socks-Xray) VPN
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/menu.png)

## What Does this script do?
This script provides a solution for setting up L2TP/OpenVPN/SSTP server via "SoftEther" and tunnel via "Rathole+Tun2socks+Xray" in restricted locations (e.g., Iran, China).

## پروتکل های پشتیبانی شده
- L2TP
- L2TP/IPSec
- OpenVPN
- SSTP
- Radius (برای مدیریت اکانت حرفه ای)

## دیاگرام
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/diagram.png)

## چجوری کار میکنه؟
به دو سرور نیاز داریم: یک سرور برای کانکشن ورودی ترافیک L2TP/OpenVPN/SSTP به همراه SoftEther (سرور ایران) و یکی برای سرور Edge (سرور خارج). سرور اول (سرور تانل) سروری هستش که محدودیتی در اتصال ورودی L2TP/OpenVPN/SSTP در اون برخلاف سرور Edge (سرور خارج) که نمیشه بصورت مستقیم بهش متصل شد وجود نداره.

سرور Edge اولین کانکشن رو به سرور تانل بصورت Reverse (توسط Rathole) با استفاده از VLESS + WebSocket(WS) توسط Xray-Core ایجاد میکنه، که یک پروکسی SOCKS5 روی سرور تانل (ایران) مهیا میشه. حالا با استفاده از tun2socks ترافیک این پروکسی SOCKS5 رو به یک کارت شبکه مجازی انتقال میدیم.

و در آخر با استفاده از Policy-Based Routing (PBR) ترافیک ورودی L2TP/OpenVPN/SSTP رو به کارت شبکه مجازی که توسط tun2socks ایجاد شده بود هدایت میکنیم.

## دونیت
🔹USDT-TRC20: ```THuvCFh7Epk926fs23ew6NPFShMrnagVxx```

🔹TRX: ```THuvCFh7Epk926fs23ew6NPFShMrnagVxx```

🔹LTC: ```ltc1quah8ej7ukez53wykehpeew7spya0kzx59r6nfk```

🔹BTC: ```bc1qe7z26fhd47xwezp25vk44e8e925ee43txdnfdp```

🔹ETH: ```0x7Bb6CfF428F75b468Ea49657D345Efc45C7104C9```

## آموزش نصب
SOON

## نصب
```bash
sh -c "$(wget https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/v2/rtxvpn_v2.sh -O -)"
```

## سیستم عامل های پشتیبانی شده
این اسکریپت از تمامی سیستم عامل های Debian بیس که از systemd استفاده میکنند پشتیبانی میکنه

## تست سرعت
![App Screenshot](https://raw.githubusercontent.com/Sir-MmD/RTX-VPN/refs/heads/v2/speedtest.jpg)
## تنظیمات تانل: Xray-core
این اسکریپت بصورت پیشفرض از کانفیگ 'VLESS + WS' برای Xray-Core استفاده میکنه. میتونید کانفیگ دلخواهتون رو در ```/opt/rtxvpn_v2/edge/edge.json``` برای سرور Edge (خارج) و ```/opt/rtxvpn_v2/tunnel/tunnel.json``` برای سرور تانل (ایران) اعمال کنید

## تنظیمات تانل: rathole
شما همچنین میتونید تنظیمات مربوط به تانل rathole رو در مسیر ```/opt/rtxvpn_v2/edge/edge.toml``` برای سرور Edge (خارج) و ```/opt/rtxvpn_v2/tunnel/tunnel.toml``` برای سرور تانل (ایران) اعمال کنید

## سرویس های Systemd: سرور Edge (خارج)
RTX-VPN (Rathole + Xray): ```rtxvpn.service```

## سرویس های Systemd: سرور تانل (ایران)
RTX-VPN (Rathole + Tun2socks + Xray + PBR): ```rtxvpn.service```

SoftEther: ```softether.service```

Dnsmasq: ```dnsmasq.service```

## CopyRight
SoftEther: https://www.softether.org

Rathole: https://github.com/rapiz1/rathole

Tun2socks: https://github.com/bedefaced/vpn-install

Xray-Core: https://github.com/XTLS/Xray-core
