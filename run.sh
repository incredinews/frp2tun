#!/bin/bash

test -e /setup.sh && source /setup.sh

#!/bin/ash

echo starting
test -e /etc/connector.conf  && /usr/bin/connector --config /etc/connector.conf   2>&1 |grep -v -e decryp -e key -e keepalive -e ndshake -e TUN -e Interface -e ncryp &
test -e /etc/connector2.conf && /usr/bin/connector --config /etc/connector2.conf  2>&1 |grep -v -e decryp -e key -e keepalive -e ndshake -e TUN -e Interface -e ncryp &
[[ -z "$AUTH" ]] || /usr/bin/chi server --port 4444 --reverse --backend http://127.0.0.1:8000 & 
test -e /etc/caddyfile && caddy run --config /etc/caddyfile &
/usr/bin/frps -c /opt/frps.toml