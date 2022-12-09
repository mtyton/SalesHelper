FROM ubuntu:22.04

RUN mkdir /app
WORKDIR /app

ADD ./ /app

# install python
RUN apt update -y
RUN apt install -y python3 python3-dev python3-pip python3-pip
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/data"
# run cronjobs
RUN apt-get install -y cron vim

# run api
CMD ["python3", "main.py"]
