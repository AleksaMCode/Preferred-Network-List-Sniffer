<img width="150" align="right" src="./resources/rpis_logo.png"></img>
# Preffered Network List Sniffer
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> :warning: **Disclaimer**: All content in this project is intended for security research purpose only.

## Table of contents
- [Preffered Network List Sniffer](#preffered-network-list-sniffer)
  - [Table of contents](#table-of-contents)
  - [Requirements - What you'll need](#requirements---what-youll-need)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Using Docker](#using-docker)
    - [Using Prebuild Docker Image](#using-prebuild-docker-image)
    - [Without Docker](#without-docker)
  - [References](#references)



## Requirements - What you'll need

- Raspberry Pi
- Micro SD card
- USB Wi-Fi adapter (optional)
  - Used to achieve bigger range when capturing packets.
- HDMI cable (optional)

## Prerequisites

- Kali Linux OS
  - Needed in order to use monitoring mode and [aircrack-ng](https://github.com/aircrack-ng/aircrack-ng) tool. You can download Kali Linux ARM image [here](https://www.kali.org/get-kali/#kali-arm).
    - Alternatively, you could use another OS, but you will need to patch[^1] the kernel using the Nexmon or use a wireless adapter that supports monitoring mode. Here is a [link](https://elinux.org/RPi_USB_Wi-Fi_Adapters) for supported USB adapters by Raspberry Pi.
    - You will also have to install the *aircrack-ng* tool, as it only comes preinstalled on the Kali Linux.
- Start your network interface in a monitoring mode with: `airmon-ng start wlan0` [2].

[^1]: Broadcom never officially supported monitor mode, which limited the usefulness of the wireless cards in Raspberry Pi devices [3]. The Nexmon project is a firmware patch for the Broadcom chips in use within Raspberry Pi devices [1]. This patch will allow you to use the monitoring mode on your RPi device.

## Setup

### Using Docker

<p align="justify">Quickly setup a development instance, featuring hot-reloading on both the backend and the frontend:</p>

```bash
# First clone this repo.
git clone https://github.com/AleksaMCode/Preferred-Network-List-Sniffer.git
# Move to the project root folder.
cd Preferred-Network-List-Sniffer
# Bring up the backend:
docker compose up
# Move into the web folder.
cd web
# Install npm dependencies.
npm install --force
# Start hot-reloading web server:
npm run serve
# This will spawn a tab on `localhost:3000`.
```

### Using Prebuild Docker Image

<p align="justify">Download the prebuild image from the GitHub Container Registry and run it locally.</p>

```bash
docker run ghcr.io/aleksamcode/pnls-ghcr:latest
```

### Without Docker


## References

1. [Nexmon Git repository](https://github.com/seemoo-lab/nexmon)
2. [Aircrack-ng documentation](https://www.aircrack-ng.org/doku.php?id=airmon-ng)
3. [Enable Monitor Mode & Packet Injection on the Raspberry Pi](https://null-byte.wonderhowto.com/how-to/enable-monitor-mode-packet-injection-raspberry-pi-0189378/)