FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip install sympy
RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY dev/RSA_Encryption_Server.py .
COPY dev/flag.txt .
COPY dev/ynetd .
RUN chmod +x ynetd
RUn chmod +x RSA_Encryption_Server.py
RUN chown -R root:root /home/ctf

USER root
EXPOSE 7754
CMD ./ynetd -p 7754 ./RSA_Encryption_Server.py
