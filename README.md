<img width="150" align="right" src="./resources/rpis_logo.png"></img>
# Preferred Network List Sniffer - PNLS
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![](https://img.shields.io/github/v/release/AleksaMCode/Preferred-Network-List-Sniffer)

**Preferred Network List Sniffer** (PNLS) is a Red Team Wi-Fi auditing tool with a simple web interface that is capable of intercepting SSIDs[^1] from the device's preferred network list (PNL)[^2]. This is achieved by sniffing out [Probe Requests](#probe-request) in the nearby vicinity, which are then parsed for SSID and other information and finally propagated to the web UI. The primary motivation for this project was to look into 802.11 Probe Requests and the privacy risks associated with the data they transmit.

<p align="center">
<img
src="./resources/overview.gif?raw=true"
alt="PNLS system overview"
width="70%"
class="center"
/>
<p align="center">
    <label><b>Fig. 1</b>: PNLS system overview</label>
    </p>
</p>

> [!WARNING]
> All content in this project is intended for security research purposes only.

> [!NOTE]
> <ul>
> <li><p align="justify">This project is part of my ongoing research into <i>Privacy Protection in Wi-Fi Networks</i>.</p></li>
>     <ul><li><a href="https://drive.google.com/file/d/1pYm6buyRmGwN5MY7c8_tj93C0iddurI3">Scope of work presentation</a></li></ul>
> <li><p align="justify">To monitor the ongoing work on the PNLS, see the <a href="https://github.com/users/AleksaMCode/projects/1">project's board</a>.</p></li>

## Table of contents
- [Preferred Network List Sniffer - PNLS](#preferred-network-list-sniffer---pnls)
  - [Table of contents](#table-of-contents)
  - [How to build the PNLS](#how-to-build-the-pnls)
    - [Requirements](#requirements)
    - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Using Docker](#using-docker)
    - [Using Prebuild Docker Image](#using-prebuild-docker-image)
    - [Without Docker](#without-docker)
  - [Probe Requests](#probe-requests)
  - [SSID Filtering](#ssid-filtering)
  - [Architecture](#architecture)
    - [Why Asynchronous Server Gateway Interface?](#why-asynchronous-server-gateway-interface)
    - [Why WebSockets?](#why-websockets)
    - [Pub-Sub Model](#pub-sub-model)
  - [Screenshots](#screenshots)
  - [Acronyms](#acronyms)
  - [References](#references)

## How to build the PNLS 

<p align="justify">Here is what you will need in order to duplicate and deploy this project, including both the hardware and software components. Once you have your working environment ready, head over to the <a href="#setup">setup sections</a>.</p>

### Requirements

- Raspberry Pi (RPi)
- Suitable RPi power supply (see [the power supply documentation for details](https://www.raspberrypi.com/documentation/computers/getting-started.html#power-supply))
- Micro SD card (see [the SD card documentation for details](https://www.raspberrypi.com/documentation/computers/getting-started.html#sd-cards))
- USB Wi-Fi adapter (optional)
  - Used to achieve a bigger range when capturing packets.
- HDMI cable (optional)
  - Used to display the web UI from the RPi instead of connecting to it remotely using your computer.

### Prerequisites

- Kali Linux OS
  - Needed in order to use monitoring mode and [aircrack-ng](https://github.com/aircrack-ng/aircrack-ng) tool. You can download the Kali Linux ARM image from [here](https://www.kali.org/get-kali/#kali-arm).
    - Alternatively, you could use another OS, but you will need to patch[^3] the kernel using the [nexmon](https://github.com/seemoo-lab/nexmon)[^4] or use a wireless adapter that supports monitoring mode. Here is a [link](https://elinux.org/RPi_USB_Wi-Fi_Adapters) for supported USB adapters by Raspberry Pi.
    - You will also have to install the *aircrack-ng* tool, as it only comes preinstalled on Kali Linux.
- Start your network interface in monitoring mode with: `sudo airmon-ng start wlan0` [2].

> [!NOTE]
> <p align="justify">The Kali image uses <a href="https://re4son-kernel.com/">Re4son</a>'s kernel, which includes the drivers for external Wi-Fi cards and the Nexmon firmware for the built-in wireless card on the RPi 3 and 4 [3].</p>

<p align="center">
<img
src="./resources/pnls-device -1.jpg?raw=true"
alt="PNLS RPi 4 device"
class="center"
/>
<p align="center">
    <label><b>Fig. 2:</b>
     PNLS running on a RPi 4 with an external antena and a battery bank</label>
    </p>
</p>

<p align="center">
<img
src="./resources/pnls-device -2.jpg?raw=true"
alt="PNLS RPi 4 device AWUS036ACS"
class="center"
/>
<p align="center">
    <label><b>Fig. 3:</b>
     PNLS running on a RPi 4 with a case with an <a href="https://alfa-network.eu/awus036acs">AWUS036ACS</a> antena</label>
    </p>
</p>

<p align="center">
<img
src="./resources/pnls-device -3.jpg?raw=true"
alt="PNLS RPi 4 device AWUS036ACM"
class="center"
/>
<p align="center">
    <label><b>Fig. 4:</b>
     PNLS running on a RPi 4 with an <a href="https://alfa-network.eu/awus036acs">AWUS036ACM</a> antena</label>
    </p>
</p>

## Setup

If you don't want to use `Docker`, head over to [setup without Docker](#without-docker).

### Using Docker

<p align="justify">Quickly setup a development instance:</p>

```bash
# First clone this repo.
git clone https://github.com/AleksaMCode/Preferred-Network-List-Sniffer.git
# Move to the project root folder.
cd Preferred-Network-List-Sniffer
# Build backend and frontend image.
docker compose build
# Bring up both the backend and the frontend server.
docker compose up
# Move into the sniffer folder.
cd sniffer
# Run the Sniffer service.
sudo python3 sniffer.py
```

### Using Prebuild Docker Image

<p align="justify">Currently, multi-platform images are not available, and the project only supports the <code>ARM64v8</code> architecture. Download the latest prebuild images from the GitHub Container Registry and run them locally.</p>

```bash
# First clone this repo.
git clone https://github.com/AleksaMCode/Preferred-Network-List-Sniffer.git
# Move to the project root folder.
cd Preferred-Network-List-Sniffer
# Download the prebuild images.
docker pull ghcr.io/aleksamcode/pnls-backend-ghcr:latest
docker pull ghcr.io/aleksamcode/pnls-frontend-ghcr:latest
# Bring up both the backend and the frontend server.
docker compose up
# Move into the sniffer folder.
cd sniffer
# Run the Sniffer service.
sudo python3 sniffer.py
```

### Without Docker

- <p align="justify">Backend: to start the ASGI and Redis servers and to run needed services, see <a href="./sniffer/README.md">these instructions</a>.</p>
- <p align="justify">Frontend: to run the React server, see <a href="./web/README.md">these instructions</a>.</p>


Here is a screenshot when everything was ran "manually":

- Top Left: Redis server
- Top Right: ASGI server
- Bottom Left: *Sniffer* service
- Bottom Right: React server

<p align="center">
<img
src="./resources/kali_screenshot.png?raw=true"
alt="PNLS Kali screenshot"
class="center"
/>
<p align="center">
    <label><b>Fig. 3</b>: PNLS screenshot</label>
    </p>
</p>

## Probe Requests

<p align="justify">Probe Requests are management 802.11 frames that are used to connect devices to the previously associated wireless Access Points (AP). Whenever a device has enabled Wi-Fi but isn't connected to a network, it is periodically sending a burst of Probe Requests containing SSIDs from its PNL. These frames are sent unencrypted, and anyone who is Radio Frequency (RF) monitoring can capture and read them. Probes are sent to the broadcast DA address (<code>ff:ff:ff:ff:ff:ff</code>). Once they are sent, the device starts the Probe Timer. At the end of the timer, the device processes the received answer. If the device hasn't received an answer, it will go to the next channel and repeat the process. There are two types of Probe Requests:</p>
<ul>
  <li><p align="justify"><i>Directed Probe Requests</i>: using specific SSID from device's PNL</p></li>
  <li><p align="justify"><i>Null Probe Requests</i>: using Wildcard SSID (empty SSID)</p></li>
  <ul>
    <li><p align="justify">Blank Requests are sent in order to get a response from all available APs that are in range.</p></li>
    <li><p align="justify">In addition to filtering 802.11 Probe Request frames from all the captured packets, <i>Sniffer</i> will also filter out the Wildcard SSIDs.</p></li>
  </ul>
</ul>

## SSID Filtering

<p align="justify">When capturing Probe Requests at places where there is a large local network with a lot of Wi-Fi clients, PNLS will inevitably capture a lot of Probe Requests that contain the SSID of the said network. The filtering of such SSIDs might be advantageous, as they are of no value to us and can cause an increase in socket load. Filtering out these SSIDs will not only reduce the load on socket connections, but it will also prevent the spam of the aforementioned SSIDs on the web UI.</p>

<p align="justify">When using this feature, you will need to make slight adjustments to the source code. Precisely, you will need to update the <code>SSID_FILTER</code> list in the <a href="./sniffer/settings.py"><code>settings.py</code></a> file with the value you want the </i>Sniffer</i> to ignore. Once updated, rebuild the project and start the PNLS.</p>

## Architecture

<p align="justify">This project uses Event-Driven architecture (EDA), which is designed atop of message-driven architectures. While this project uses a centralized solution (everything is run from the RPi), due to loosely coupled components as a result of the usage of EDA, it is possible to create a decentralized solution if needed. PNLS consists of an event publisher (sniffer), an event consumer (web application), and an event channel. Here, the event channel is implemented as Message-Oriented Middleware (MOM).</p>

<p align="center">
<img
src="./resources/pnls-system-diagram.svg?raw=true"
alt="PNLS system deployment diagram"
class="center"
/>
<p align="center">
    <label><b>Fig. 4</b>: PNLS system deployment diagram</label>
    </p>
</p>

### Why Asynchronous Server Gateway Interface?

<p align="justify">The Asynchronous Server Gateway Interface (ASGI) provides a standardized interface between async-capable Python web servers and services [4]. The ASGI was chosen due to the project's need for a long-lived WebSocket connection in order to facilitate async communications between different clients. In addition, it also allows for the utilization of background coroutines during API calls. The PNLS uses the <a href="https://github.com/encode/uvicorn">uvicorn</a> implementation for Python in order to use the ASGI web server.</p>

### Why WebSockets?
<p align="justify">Through the utilization of WebSocket communication protocol, we are able to facilitate full-duplex, two-way communication. While this project doesn't have the need for two-way communication, it does have a need for real-time interaction between the system components. This way, the sniffed data will be available to the end-user as soon as it is captured.</p>

### Pub-Sub Model
<p align="justify">The project's MOM is realized through the Message Broker using Redis. In the publish-subscribe (pub-sub) model, the <i>Sniffer</i> is responsible for producing messages, while the web application (subscriber) registers for the specific Topic (Redis channel). When the <i>Sniffer</i> sends a message to a Topic, it is distributed to all subscribed consumers, allowing for asynchronous and scalable communication. PNLS uses the lightweight messaging protocol <i>Redis Pub/Sub</i> for message broadcasting in order to propagate short-lived messages with low latency and large throughput [5][6]. In this way, overheads associated with encoding data structures in a form that can be written to a disk have been avoided. In doing so, this solution will have potentially better performance [7]. The figure below displays the simplified system activity through the event-driven workflow.</p>

<p align="center">
<img
src="./resources/pub-sub_seq_diagram.svg?raw=true"
alt="pub-sub sequence diagram"
class="center"
/>
<p align="center">
    <label><b>Fig. 5</b>: PNLS Pub-Sub model sequence diagram</label>
    </p>
</p>

> [!NOTE]
> Implemented MOM does not provide persistent storage or a message queue for data accumulation, which means messages will be lost if they are published to a Topic without subscribers.

## Screenshots

<p align="justify">Below is an example of a web UI displaying published test SSIDs.</p>

<p align="center">
<img
src="./resources/pnls_web.gif?raw=true"
alt="PNLS web - example with test SSIDs"
width="90%"
class="center"
/>
<p align="center">
    <label><b>Fig. 6</b>: PNLS web - example with test SSIDs</label>
    </p>
</p>

## Acronyms
 <table>
  <tr>    <td>PNL</td>    <td>Preferred Network List</td>  </tr>
  <tr>    <td>PNLS</td>   <td>Preferred Network List Sniffer</td> </tr>
  <tr>    <td>SSID</td>    <td>Service Set Identifier</td>  </tr>
  <tr>    <td>UI</td>    <td>User Interface</td>  </tr>
  <tr>    <td>RPi</td>    <td>Raspberry Pi</td>  </tr>
  <tr>    <td>OS</td>    <td>Operating System</td>  </tr>
  <tr>    <td>AP</td>    <td>Access Points</td>  </tr>
  <tr>    <td>RF</td>    <td>Radio Frequency </td>  </tr>
  <tr>    <td>EDA</td>    <td>Event-Driven Architecture</td>  </tr>
  <tr>    <td>MOM</td>    <td>Message-Oriented Middleware</td>  </tr>
  <tr>    <td>ASGI</td>    <td>Asynchronous Server Gateway Interface</td>  </tr>
  <tr>    <td>pub-sub</td>    <td>publish-subscribe</td>  </tr>
</table>

## References

1. [Nexmon Git repository](https://github.com/seemoo-lab/nexmon)
2. [Aircrack-ng documentation](https://www.aircrack-ng.org/doku.php?id=airmon-ng)
3. [Kali On ARM documentation](https://www.kali.org/docs/arm/raspberry-pi-4/)
4. [ASGI Documentation](https://asgi.readthedocs.io/en/latest/introduction.html)
5. [Low-latency message queue & broker software](https://redis.com/solutions/use-cases/messaging/)
6. [Redis - Pub/Sub Defined](https://redis.com/glossary/pub-sub/)
7. [Stephen M. Rumble, Ankita Kejriwal, and John K. Ousterhout, “Log-Structured
Memory for DRAM-Based Storage,” at 12th USENIX Conference on File and Storage
Technologies (FAST)](https://www.usenix.org/system/files/conference/fast14/fast14-paper_rumble.pdf)
8. [Enable Monitor Mode & Packet Injection on the Raspberry Pi](https://null-byte.wonderhowto.com/how-to/enable-monitor-mode-packet-injection-raspberry-pi-0189378/)

[^1]: A Service Set Identifier (SSID) is an 802.11 ID used to name a Wi-Fi network that consists of a maximum of 32 characters that can contain case-sensitive letters, numbers, and special characters no longer than 32 characters.
[^2]: A Preferred Network List is a collection of saved SSIDs with additional settings that you created the first time you connected your device to those networks.
[^3]: Broadcom never officially supported monitor mode, which limited the usefulness of the wireless cards in Raspberry Pi devices [8]. The Nexmon project is a firmware patch for the Broadcom chips in use within RPi devices. [1]. This patch will allow you to use the monitoring mode on your RPi device.
[^4]: The C-based Firmware Patching Framework for Broadcom/Cypress Wi-Fi Chips that enables Monitor Mode, Frame Injection and much more.