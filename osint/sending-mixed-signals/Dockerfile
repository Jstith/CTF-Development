FROM python:slim

RUN useradd -d /home/challenge -m -s /bin/bash challenge
RUN pip3 install flask
RUN apt -y update

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY app .

EXPOSE 8080
CMD ["python3", "app.py"]
