# Keenetic VPN switcher

[![CI](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml/badge.svg)](https://github.com/hu553in/keenetic-vpn-switcher/actions/workflows/ci.yml)

A private Telegram bot that lets you toggle VPN policies for selected devices on a Keenetic router.

The bot is intended for personal use and restricts access to a predefined list of Telegram user IDs.
Each device is mapped by name and MAC address, allowing quick switching between VPN and non-VPN policies
directly from Telegram.

## Environment variables

The bot is configured entirely via environment variables.

| Variable             | Required | Description                                                        | Default            |
| -------------------- | -------- | ------------------------------------------------------------------ | ------------------ |
| `BOT_TOKEN`          | Yes      | Telegram bot token.                                                | -                  |
| `ROUTER_PASSWORD`    | Yes      | Password for the Keenetic router user.                             | -                  |
| `ALLOWED_USER_IDS`   | Yes      | Comma-separated list of Telegram user IDs allowed to use the bot.  | -                  |
| `DEVICES_JSON`       | Yes      | JSON array of `[name, mac]` pairs describing controllable devices. | -                  |
| `ROUTER_URL`         | No       | Base URL of the Keenetic router web interface.                     | http://192.168.1.1 |
| `ROUTER_USER`        | No       | Router username.                                                   | admin              |
| `VPN_POLICY_NAME`    | No       | Name of the VPN-enabled policy to apply.                           | Policy0            |
| `NO_VPN_POLICY_NAME` | No       | Name of the non-VPN policy to apply.                               | Policy1            |

## Example configuration

```
BOT_TOKEN=123456:replace-me
ROUTER_PASSWORD=super-secret-password
ALLOWED_USER_IDS=1,2
DEVICES_JSON='[["laptop","00:00:00:00:00:00"],["iphone","00:00:00:00:00:00"]]'
ROUTER_URL=http://192.168.1.1
ROUTER_USER=admin
VPN_POLICY_NAME=Policy0
NO_VPN_POLICY_NAME=Policy1
```

## Notes

- The bot assumes that VPN and non-VPN policies already exist on the router.
- Device identification is based on MAC address.
- Access control is enforced strictly via `ALLOWED_USER_IDS`.
- Designed to be simple, explicit, and safe for unattended use.
