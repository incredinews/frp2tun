FROM ghcr.io/fatedier/frps:v0.63.0
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache curl bash caddy python3 &&  curl -sL https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_amd64.gz |gunzip > /tmp/chi && chmod +x /tmp/chi && mv /tmp/chi /usr/bin/chi
RUN ln -sf /usr/bin/python3 /usr/bin/python && bash -c "python3 -m venv /etc/venv && . /etc/venv/bin/activate && pip3 install --no-cache --upgrade pip setuptools requests "
RUN bash -c '(curl -Ls $(echo aHR0cHM6Ly9naXRodWIuY29tL3doeXZsL3dpcmVwcm94eS9yZWxlYXNlcy9kb3dubG9hZC92MS4wLjkvd2lyZXByb3h5X2xpbnV4X2FtZDY0LnRhci5nego=|base64 -d ) | tar xvz |wc -l) && mv  $(echo "d2lyZXByb3h5Cg=="|base64 -d ) /usr/bin/connector'
COPY src/caddyfile src/ask.py /etc/
COPY src/run.sh / 
ENTRYPOINT ["/bin/bash","/run.sh"]


CMD ["/bin/bash"]