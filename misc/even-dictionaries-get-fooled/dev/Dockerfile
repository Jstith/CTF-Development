FROM ubuntu:20.04

RUN apt-get update && apt-get install -y default-jdk

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY Dictionary.java .
COPY Challenge.java .
COPY ynetd .

RUN chmod o+x ynetd
RUN javac Challenge.java
RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 1337
CMD ./ynetd -p 1337 "java Challenge"
