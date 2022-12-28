FROM ubuntu:20.04
RUN apt update
RUN apt install -y python3-pip freeradius-python3
CMD ["freeradius", "-X"]
EXPOSE 1812/tcp
EXPOSE 1812/udp