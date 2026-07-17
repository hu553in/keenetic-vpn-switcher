# Keenetic VPN switcher

[![CI](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml/badge.svg)](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml)

Private Telegram bot for switching selected Keenetic devices between VPN and non-VPN policies.

## What it does

- Shows configured devices in Telegram
- Applies the VPN or non-VPN Keenetic policy to the selected MAC address
- Saves the router configuration after every successful change
- Restricts access to configured Telegram user IDs

## Requirements

- Python 3.14+
- `uv`
- Bun for repository tooling
- Telegram bot token
- Keenetic router credentials
- Existing Keenetic policies for VPN and non-VPN routing
- Optional: Docker for deployment

## Setup

Local checkout:

```bash
make install-deps
make ensure-env
```

Docker image:

```bash
docker build -t keenetic-vpn-switcher .
```

CI publishes `ghcr.io/hu553in/keenetic-vpn-switcher`; `latest` follows `main`, while `sha-*` tags
are immutable.

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

Local:

```bash
uv run --env-file .env python3 main.py
```

Docker:

```bash
docker run --rm --env-file .env keenetic-vpn-switcher
```

Open `/start` in Telegram, choose a device, then choose the VPN action.

## Runtime behavior

- The bot calls the Keenetic web API at `ROUTER_URL`
- Devices are matched by MAC address
- Access control is enforced before callbacks and messages are handled
- The router configuration is saved after policy changes

## Development

```bash
make install-deps
uv run prek install
make check
make check-fix
```

Focused checks:

```bash
make lint
make lint-fix
make check-types
make check-deps
make check-vulns
make check-unused
make check-security
```
