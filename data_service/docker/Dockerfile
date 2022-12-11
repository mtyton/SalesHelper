FROM ubuntu:22.04

RUN mkdir /data
WORKDIR /data

ADD ./ /data

# install python
RUN apt update -y
RUN apt install -y python3 python3-dev python3-pip python3-pip
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

ENV PYTHONPATH "${PYTHONPATH}:/data"
# run cronjobs
RUN apt-get install -y cron vim

