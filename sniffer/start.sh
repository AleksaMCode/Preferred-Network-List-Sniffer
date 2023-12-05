#!/bin/bash
sudo airmon-ng start $1
python3 pnls.py $1
