FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-pip
RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

USER ctf
WORKDIR /home/ctf

COPY dev /home/ctf

USER root
RUN mkdir -p session_databases
RUN chown -R ctf:ctf session_databases

USER ctf
RUN pip3 install -r requirements.txt
RUN python3 gen_database.py

EXPOSE 5000
CMD python3 main.py
