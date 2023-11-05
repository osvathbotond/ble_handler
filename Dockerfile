from ubuntu:jammy

COPY . /app

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 \
                                                         python3-pip \
                                                         git \
                                                         libbluetooth-dev \
    && :

RUN python3 -m pip --no-cache-dir --disable-pip-version-check install -r /app/requirements.txt

WORKDIR /app

RUN sh build.sh
