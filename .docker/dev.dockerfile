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
                                 vim \
                                 git \
                                 universal-ctags  \
                                 python3-venv \
                                 python3-matplotlib \
                                 python3-pygraphviz \
                                 ffmpeg \
               && rm -rf /var/lib/apt/lists/*


RUN ln -s /usr/bin/python3 /usr/bin/python


RUN mkdir -p /home/swarm && useradd swarm && chown swarm:swarm /home/swarm

WORKDIR /home/swarm
USER swarm
ENV PATH="/home/swarm/.local/bin:$PATH"

# Development installment
RUN python -m pip install flake8
RUN python -m pip install PyQt5




# Installing dependices
COPY requirement.txt /home/swarm
RUN python -m pip install -r requirement.txt



COPY entrypoint.sh /home/swarm
CMD ["vim", "+Explore"]
ENTRYPOINT ["/home/swarm/entrypoint.sh"]

# vim: filetype=dockerfile
