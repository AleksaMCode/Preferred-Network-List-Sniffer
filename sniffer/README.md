# pnls-sniffer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.11.4](https://img.shields.io/badge/python-3.11.4-blue.svg)](https://www.python.org/downloads/release/python-3114/)

<p align="justify">PNLS Backend is written using Python. All of the needed packages are stored inside of the <i>requirements.txt</i>.</p>

> [!NOTE]
> <p align="justify">Code is formatted using <b>Black</b> and linted with <b>flake8</b>. You can use <code>sh formatter.sh</code> command to format you code.

## Run

First start the `Redis` server by running the following command in the terminal:

```shell
redis-server
```

This will start the Redis server in the default configuration at port 6379.

After, clone the project and move to the backend root folder.

```shell
cd Preferred-Network-List-Sniffer/sniffer
```

Create a virtual environment and install packages.

```shell
virtualenv -p python3 venv
source venv/bin/active
pip3 install -r requirements.txt
```

<p align="justify">Run your Backend API written using FastAPI with Uvicorn. Because the uvicorn is called from inside the code, you only need to run following:</p>

```shell
python3 pnls.py
```
Server without hot reload will be available on `localhost:3001/`.

> [!WARNING]
> In order to have ASGI server running, you first need to run a Redis server, otherwise the server will not start.

To start the sniffer microservice, run the following:

```shell
sudo python3 sniffer.py
```

Yes, for now, you need to run the sniffer with `sudo` because the [`scapy`](https://github.com/secdev/scapy) library, which is used for sniffing, needs the admin privilege in order to capture packets.