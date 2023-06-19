FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#RUN apk add bash curl iptables iperf3
COPY power-stat-telegraf.py  .

# docker build -t scottmsilver/powerstat:1.0 .
# docker push scottmsilver/powerstat:1.0 
# Mapp the pwrstatd.ipc file for use inside the container
# docker run -v /var/pwrstatd.ipc:/var/pwrstatd.ipc scottmsilver/powerstat:1.0 python3 power-stat-telegraf.py 
# sudo usermod -aG docker telegraf
# newgrp docker
# now test with:
# become telegraf
# sudo -u telegraf bash
# telegraf -test