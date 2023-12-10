#!/bin/bash
sudo airmon-ng start $1
sudo python3 pnls.py $1
