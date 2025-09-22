#!/bin/bash

test -e /setup.sh && source /setup.sh

#!/bin/ash
echo ...
test -e /etc/connector.conf  && ( while (true);do  /usr/bin/connector --config /etc/connector.conf   2>&1 |grep -v -e decryp -e key -e keepalive -e ndshake -e TUN -e Interface -e ncryp ;done ) &
test -e /etc/connector2.conf && ( while (true);do  /usr/bin/connector --config /etc/connector2.conf  2>&1 |grep -v -e decryp -e key -e keepalive -e ndshake -e TUN -e Interface -e ncryp ;done ) &
[[ -z "$AUTH" ]] || (while (true);do /usr/bin/chi server --port 4444 --reverse --backend http://127.0.0.1:7500 ;done) & 
test -e /etc/caddyfile && (while (true);do caddy run --config /etc/caddyfile ;sleep 10;done ) &
[[ -z "$EXTIPS" ]] || (while (true);do python3 /etc/ask.py ;sleep 10;done ) & 
while (true);do /usr/bin/frps -c /opt/frps.toml;sleep 5 ;done
