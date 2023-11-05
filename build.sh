#!/bin/sh

g++ -O3 -std=c++20 -fPIC $(python3 -m pybind11 --includes) -shared ./cpp/pvvx_data.cpp -o ./receivers/_pvvx_data$(python3-config --extension-suffix)
