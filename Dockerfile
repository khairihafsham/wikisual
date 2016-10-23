FROM python:3.5.2

WORKDIR /opt/wikisual

ADD . /opt/wikisual

RUN pip install -U pip

RUN pip install -r /opt/wikisual/requirements.txt
