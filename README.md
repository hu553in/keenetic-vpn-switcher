# Keenetic VPN switcher

Toggle the VPN policy applied to devices on a Keenetic router through a private Telegram bot.

## Environment variables

| Variable             | Required | Note                                                                            | Default              | Example                                                           |
| -------------------- | -------- | ------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------------------------- |
| `BOT_TOKEN`          | Yes      | -                                                                               | -                    | `123456:replace-me`                                               |
| `ROUTER_PASSWORD`    | Yes      | -                                                                               | -                    | `super-secret-password`                                           |
| `ALLOWED_USER_IDS`   | Yes      | The comma-separated list of Telegram user IDs allowed to interact with the bot. | -                    | `1,2`                                                             |
| `DEVICES_JSON`       | Yes      | The JSON array of `[name, mac]` pairs describing selectable devices.            | -                    | `[["laptop","00:00:00:00:00:00"],["iphone","00:00:00:00:00:00"]]` |
| `ROUTER_URL`         | No       | -                                                                               | `http://192.168.1.1` | -                                                                 |
| `ROUTER_USER`        | No       | -                                                                               | `admin`              | -                                                                 |
| `VPN_POLICY_NAME`    | No       | -                                                                               | `Policy0`            | -                                                                 |
| `NO_VPN_POLICY_NAME` | No       | -                                                                               | `Policy1`            | -                                                                 |
