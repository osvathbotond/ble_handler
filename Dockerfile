FROM ubuntu:jammy

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 \
                                                         python3-pip \
                                                         git \
                                                         libbluetooth-dev \
    && rm -rf /var/lib/apt/lists/* \
    && :

COPY requirements.txt /tmp/
RUN python3 -m pip --no-cache-dir --disable-pip-version-check install -r /tmp/requirements.txt

COPY build.sh /tmp/
COPY src /src

WORKDIR /
RUN /tmp/build.sh

COPY config.json /src/config.json

CMD ["python3", "/src/main.py"]
