FROM python:slim
# https://stackoverflow.com/questions/3373995/usr-bin-ld-cannot-find-lz
RUN apt-get update && apt-get -y install cron vim gcc libxml2-dev libxslt-dev libz-dev  python-lxml
WORKDIR /app

ENV TZ="Europe/Bratislava"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY alert_system ./alert_system
COPY requirements.txt .
COPY crontab.txt .
RUN pip3 install -r requirements.txt
RUN /usr/bin/crontab crontab.txt
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log



