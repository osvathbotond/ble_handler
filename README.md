The purpose of this program is to catch BLE-advertised data from Xiaomi Mi Temperature and Humidity Monitor 2 devices with [pvxx's firmware](https://github.com/pvvx/ATC_MiThermometer) and send out the measured data as mqtt messages and/or insert them into databases. However, it is created with modularity in mind, as it has a plugin system for both the receivers (i.e. the binary message to data converters) and the senders (i.e. the data "broadcasters").

# How to use
## Installing the dependencies
The program requires `python3` with `pip`, `libbluetooth-dev` fir the bluetooth header and `git` for the `pybluez` pip package. Currently, the following python packages are required (they are listed in the requirements.txt as well):
- pybluez: To access bluetooth utilities from python
- paho-mqtt (optional): To send messages over mqtt
- pybind11 (optional): To build the optionel c++ python binding(s). Without building it, the code will fall back to pure python implementation.

Finally, the `build.sh` can build the optional c++ python binding(s).

## Docker container (optional)
Optionally, you can build the Docker container by running
```
docker build -t ble_handler .
```
and start it by running
```
docker run --rm -ti --net=host ble_handler:latest bash
```

Note that `sudo` might be neccessary (for both `docker build` and `docker run`) to have access to the bluetooth of your device.

## Getting the devices' MAC address and receiver type
Both from the container or your machine, you can discover the visible devices and their type (provided that there is a receiver for them) with the `main.py`. It can be run in discovery mode with
```
python3 main.py -d
```

Note that `sudo` might be neccessary to have access to the bluetooth of your device.

## Setting up the `config.json`
There are two parts of the `config.json` file: `devices` and `senders`. In the `senders` section, you need to set up all of the senders you want to use. In the `devices` section, you need to set up all of your devices. Note that you can different senders for each device.

## Running the program
Both from the container or your machine, you can start the program by running
```
python3 main.py
```
Note that `sudo` might be neccessary to have access to the bluetooth of your device.

## Setting up a custom receiver and sender

You can create your own receiver and sender by creating the python code similar to the existing ones in the appropriate folder. `receivers/pvvx_data.py` and `cpp/pvvx_data.cpp` provides an example of how to setup a c++ python binding as well.

