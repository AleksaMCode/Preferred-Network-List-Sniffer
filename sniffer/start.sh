#!/bin/bash
airmon-ng start $1
python3 sniffer.py $1
