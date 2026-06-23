# srsRAN Open5GS

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** January 15, 2026

This repository documents a complete **end-to-end 5G standalone (SA) setup** using:

- **Open5GS** as the 5G Core (Docker-based)
- **srsRAN Project** as the 5G gNB
- **srsRAN 4G (srsUE)** as the UE
- **ZeroMQ** as a virtual RF interface (no SDR required)

![srsran open5gs](../images/srsran/srsran-open5gs.png)

This setup is intended for testing, learning, and research, and runs entirely on a single Ubuntu VM.

> **Note:** This documentation is a replica of the README available at the [github/ngkore/Open5GS-srsRAN](https://github.com/ngkore/Open5GS-srsRAN). Please refer to the original repository for the most up-to-date information.

## Reference Documentation

- srsUE with srsRAN gNB (ZMQ):
  [https://docs.srsran.com/projects/project/en/latest/tutorials/source/srsUE/source/index.html](https://docs.srsran.com/projects/project/en/latest/tutorials/source/srsUE/source/index.html)

## Architecture Overview

```text
+-----------------------------+
|        Ubuntu 22.04 VM      |
|                             |
|  +----------------------+   |
|  |  Open5GS 5G Core     |   |
|  |  (Docker Compose)    |   |
|  +----------+-----------+   |
|             | N2 / N3       |
|  +----------v-----------+   |
|  |   srsRAN gNB         |   |
|  |   (ZMQ RF)           |   |
|  +----------+-----------+   |
|             | ZMQ           |
|  +----------v------------+  |
|  |   srsUE               |  |
|  |   (Network Namespace) |  |
|  +-----------------------+  |
+-----------------------------+
```

## Hardware and Software Requirements

### System

- Ubuntu **22.04.1 LTS**
- Single VM or bare-metal system
- Internet access

### Software Components

- **Open5GS** (Docker-based 5G Core)
- **srsRAN Project** (5G gNB)
- **srsRAN 4G (23.11 or later)** (srsUE)
- **ZeroMQ** (virtual RF transport)

## Prerequisites

### System Packages

```bash
sudo apt update
sudo apt install -y git net-tools build-essential cmake \
                   libfftw3-dev libmbedtls-dev \
                   libboost-program-options-dev \
                   libconfig++-dev libsctp-dev \
                   libyaml-cpp-dev libgtest-dev \
                   libzmq3-dev
```

### Docker Installation (for Open5GS)

```bash
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) \
signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli \
                   containerd.io docker-buildx-plugin \
                   docker-compose-plugin
```

Add your user to the Docker group:

```bash
sudo usermod -aG docker $(whoami)
newgrp docker
```

## Build srsRAN 4G (for srsUE)

```bash
cd ~
git clone https://github.com/srsRAN/srsRAN_4G.git
cd srsRAN_4G
mkdir build && cd build

cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON
make -j$(nproc)
make test   # optional
```

## Build srsRAN Project (for 5G gNB)

```bash
cd ~
git clone https://github.com/srsran/srsRAN_Project.git
cd srsRAN_Project
mkdir build && cd build

cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON
make -j$(nproc)
```

## Deploy Open5GS 5G Core (Docker)

```bash
cd ~/srsRAN_Project/docker
docker compose up --build 5gc -d
```

Verify containers:

```bash
docker ps
docker logs -f open5gs_5gc
```

## Configuration Files (ZMQ)

Download reference configuration files:

```bash
cd ~
wget https://docs.srsran.com/projects/project/en/latest/_downloads/a7c34dbfee2b765503a81edd2f02ec22/gnb_zmq.yaml
wget https://docs.srsran.com/projects/project/en/latest/_downloads/fbb79b4ff222d1829649143ca4cf1446/ue_zmq.conf
```

## Run srsRAN gNB

```bash
cd ~/srsRAN_Project/build/apps/gnb
sudo ./gnb -c ~/gnb_zmq.yaml
```

Ensure the gNB successfully:

- Connects to AMF
- Starts NGAP and GTP-U

## Run srsUE (with Network Namespace)

Create UE network namespace:

```bash
sudo ip netns add ue1
ip netns list
```

Run srsUE:

```bash
cd ~/srsRAN_4G/build/srsue/src

sudo ./srsue ~/ue_zmq.conf
```

Or explicitly via ZMQ arguments:

```bash
sudo ./srsue \
  --rf.device_name=zmq \
  --rf.device_args="tx_port=tcp://*:2001,rx_port=tcp://localhost:2000,id=ue,base_srate=23.04e6" \
  --gw.netns=ue1
```

## Routing Configuration

### Host Routing (Downlink)

```bash
sudo ip route add 10.45.0.0/16 via 10.53.1.2
ip route
```

### UE Namespace Routing

```bash
sudo ip netns exec ue1 ip route add default via 10.45.1.1 dev tun_srsue
sudo ip netns exec ue1 ip route
```

## Connectivity Test

### Uplink Test (UE → Core)

```bash
sudo ip netns exec ue1 ping 10.45.1.1
```

### Downlink Test (Core → UE)

```bash
ping 10.45.1.2
```

Successful ping confirms **end-to-end user plane connectivity**.

## Tutorial Video

[Open5GS srsRAN E2E Deployment Tutorial](https://youtu.be/dn2V1daWnXY?si=w_aZmGpyUHKQHxEV)
