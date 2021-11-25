FROM ubuntu:20.04

ENV DEBIAN_FRONTED noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Setting timezone 
ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


LABEL maintainer "TheWorldOfCode"
LABEL version "0.1"

RUN apt update && apt install -y python3 \
                                 python3-pip \
                                 python3-matplotlib \
                                 python3-pygraphviz \
                                 ffmpeg \
               && rm -rf /var/lib/apt/lists/*


RUN ln -s /usr/bin/python3 /usr/bin/python


RUN mkdir -p /home/swarm && useradd swarm && chown swarm:swarm /home/swarm

# Setup user 
RUN useradd -m swarm -p "$(openssl passwd -1 swarm)"; \
    usermod -aG sudo swarm; \
    mkdir -p /home/swarm

WORKDIR /home/swarm
USER swarm
ENV PATH="/home/swarm/.local/bin:$PATH"

# Installing dependices
COPY --chown=swarm:swarm . /home/swarm
RUN python -m pip  install -r requirement.txt && python -m pip install .
RUN rm -r /home/swarm/*

ENTRYPOINT ["python", "-m", "swarm"]
# vim: filetype=dockerfile
