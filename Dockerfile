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
RUN /tmp/build.sh

COPY src /src

COPY config.json /src/config.json

WORKDIR /src

CMD ["python3", "/src/main.py"]
