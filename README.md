# Keenetic VPN switcher

[![CI](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml/badge.svg)](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml)

Private Telegram bot for switching selected Keenetic devices between VPN and non-VPN policies.

## What it does

- Shows configured devices in Telegram
- Applies the VPN or non-VPN Keenetic policy to the selected MAC address
- Saves the router configuration after every successful change
- Restricts access to configured Telegram user IDs

## Requirements

- Python
- `uv`
- Make and Bun for repository tooling
- Telegram bot token
- Keenetic router credentials
- Existing Keenetic policies for VPN and non-VPN routing
- Optional: Docker for deployment

## Setup

Local setup:

```bash
make install-deps
make ensure-env
```

Published image:

```bash
docker pull ghcr.io/hu553in/keenetic-vpn-switcher:latest
```

`latest` follows `main`; `sha-*` tags identify commits. Pin
`ghcr.io/hu553in/keenetic-vpn-switcher@sha256:<digest>` for an immutable deployment.

Local image:

```bash
docker build -t keenetic-vpn-switcher .
```

## Configuration

| Name                 | Required | Default              | Description                         |
| -------------------- | -------- | -------------------- | ----------------------------------- |
| `BOT_TOKEN`          | Yes      | -                    | Telegram bot token                  |
| `ROUTER_PASSWORD`    | Yes      | -                    | Keenetic router password            |
| `ALLOWED_USER_IDS`   | Yes      | -                    | Comma-separated Telegram user IDs   |
| `DEVICES_JSON`       | Yes      | -                    | JSON array of `[name, mac]` pairs   |
| `ROUTER_URL`         | No       | `http://192.168.1.1` | Keenetic web API base URL           |
| `ROUTER_USER`        | No       | `admin`              | Keenetic username                   |
| `VPN_POLICY_NAME`    | No       | `Policy0`            | Policy applied when VPN is enabled  |
| `NO_VPN_POLICY_NAME` | No       | `Policy1`            | Policy applied when VPN is disabled |

Edit the generated `.env`; `.env.example` contains every supported variable and its default.

## Usage

Run from a checkout:

```bash
uv run --locked --env-file .env python3 main.py
```

Docker:

In `.env`, remove the outer single quotes from `DEVICES_JSON`, keeping the JSON double quotes.
`docker run --env-file` passes values literally; the local `uv` command needs the outer quotes.

```bash
docker run --rm --env-file .env ghcr.io/hu553in/keenetic-vpn-switcher:latest
```

Replace the published image name with `keenetic-vpn-switcher` to run the local image.

Open `/start` in Telegram, choose a device, then choose the VPN action.

## Development

```bash
make install-deps
uv run --locked prek install
make check
make check-fix
```

Focused checks:

```bash
make lint
make lint-fix
make check-hooks
make check-types
make check-deps
make check-vulns
make check-unused
make check-security
make check-config
make check-renovate
make check-workflows
```
