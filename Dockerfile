FROM    python:3.6
MAINTAINER      yanbenny "a0912542800@gmail.com"

RUN mkdir /LineBot
WORKDIR /LineBot

ADD . /LineBot/
RUN pip install -r requirements.txt

EXPOSE 3000
CMD python main.py
