FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    xinetd \
    libc6 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m challenge

WORKDIR /home/challenge


COPY ./dbm /home/challenge/
COPY ./xinetd.conf /etc/xinetd.d/challenge
COPY ./flag.txt .

RUN chown -R root:challenge /home/challenge && \
    chmod 750 /home/challenge/dbm

RUN mkdir -p /var/log/xinetd && chmod 777 /var/log/xinetd


CMD ["/usr/sbin/xinetd", "-stayalive", "-dontfork"]
