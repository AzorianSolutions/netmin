FROM ubuntu:20.04
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive \
    TZ=America/Indiana/Indianpolis \
    apt install -y python3-pip freeradius-python3
RUN pip install requests
CMD ["PYTHONPATH=/usr/local/lib/python3.8/dist-packages", "freeradius", "-X"]
EXPOSE 1812/tcp
EXPOSE 1812/udp