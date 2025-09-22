FROM ghcr.io/fatedier/frps:v0.63.0
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache curl bash caddy python3 nss-tools screen nano &&  bash -c 'uname -m;cd /;ARCH=amd64;uname -m |grep -e armv6 -e armv7 && ARCH=armv7;uname -m |grep -e arm64 -e aarch64 && ARCH=arm64 ; echo load $ARCH;curl -sL https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_$ARCH.gz |gunzip > /tmp/chi && chmod +x /tmp/chi && mv /tmp/chi /usr/bin/chi; (curl -Ls $(echo aHR0cHM6Ly9naXRodWIuY29tL3doeXZsL3dpcmVwcm94eS9yZWxlYXNlcy9kb3dubG9hZC92MS4wLjkvd2lyZXByb3h5X2xpbnV4X2FtZDY0LnRhci5nego=|base64 -d |sed "s/amd64/$ARCH/g") | tar xvz |wc -l) && mv  $(echo "d2lyZXByb3h5Cg=="|base64 -d ) /usr/bin/connector'
RUN ln -sf /usr/bin/python3 /usr/bin/python && bash -c "python3 -m venv /etc/venv && . /etc/venv/bin/activate && pip3 install --no-cache --upgrade pip setuptools requests "
COPY src/caddyfile src/ask.py /etc/
COPY src/run.sh / 
ENTRYPOINT ["/bin/bash","/run.sh"]


CMD ["/bin/bash"]