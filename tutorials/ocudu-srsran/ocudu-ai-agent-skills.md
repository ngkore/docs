# OCUDU AI Agent Skills

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** June 23, 2026

Agent skills for monitoring and operating an [Ocudu](https://gitlab.com/ocudu/ocudu) 5G RAN stack using AI coding agents such as Claude, Cursor, and Windsurf. Built on the open [Agent Skills](https://agentskills.io/) standard.

> **Note:** This documentation is a replica of the README available at the [github/ngkore/OCUDU-AI-Agent-Skills](https://github.com/ngkore/OCUDU-AI-Agent-Skills). Please refer to the original repository for the most up-to-date information.

## Repository Structure

```text
.agents/
└── skills/
    └── ocudu/
        ├── SKILL.md              # Skill instructions read by the agent
        ├── scripts/
        │   └── ws_metrics.py     # WebSocket metrics collector
        └── references/
            ├── metrics_schema.md # JSON metrics field reference
            └── config_params.md  # gNB YAML config reference
```

## Setup

### 1. Install the Skill

Clone the repository into your project or copy the `.agents/` directory:

```bash
git clone https://github.com/ngkore/OCUDU-AI-Agent-Skills.git
```

### 2. Install Dependencies

```bash
pip install websocket-client
```

### 3. Configure the gNB

Enable `remote_control` and `metrics.enable_json` in the gNB YAML configuration:

```yaml
metrics:
  enable_json: true
  layers:
    enable_sched: true
    enable_mac: true
    enable_rlc: true
    enable_ngap: true
    enable_rrc: true
    enable_executor: true
    enable_app_usage: true
    enable_du_low: true
    enable_ru: true

remote_control:
  enabled: true
  bind_addr: 127.0.0.1
  port: 8001
```

Use `bind_addr: 0.0.0.0` if connecting from a remote machine.

## Usage

Once the skill is in place, ask your AI agent natural language questions about the running gNB:

```
> How many UEs are connected and what's their signal quality?
> Are there any scheduling issues or HARQ failures?
> What's the CPU and memory usage of the gNB?
> Collect metrics during a ping test and summarize the results.
> Is the AMF connected? How many PDU sessions are active?
> What MCS and modulation scheme is the UE using?
> Check if the gNB is running.
> Run a ping test from the UE to the core network.
```

## How It Works

The agent connects to the Ocudu gNB WebSocket interface (default `127.0.0.1:8001`), subscribes to JSON metrics, and interprets the data to answer questions. Ocudu streams metrics over WebSocket — no REST API is involved.

## Requirements

- Ocudu gNB with remote control enabled
- Python 3.8+
- `websocket-client` package

## Testing the Metrics Collector

Run the metrics collector manually to verify connectivity:

```bash
pip install websocket-client
python3 .agents/skills/ocudu/scripts/ws_metrics.py --url 127.0.0.1:8001 --count 5 --pretty
```

## Tutorial Video

[OCUDU AI Agent Skills Tutorial](https://youtu.be/KVzOKfnAbRA?si=z45xA8I6crJLaAUh)
