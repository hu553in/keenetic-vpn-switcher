# Keenetic VPN switcher

Toggle the VPN policy applied to devices on a Keenetic router
through a private Telegram bot.

## Environment variables

All sensitive configuration is supplied through environment variables
(or a `.env` file when running locally).

| Variable             | Required | Description                                                         |
| -------------------- | -------- | ------------------------------------------------------------------- |
| `BOT_TOKEN`          | Yes      | Telegram bot token issued by `@BotFather`.                          |
| `ROUTER_PASSWORD`    | Yes      | Password for the Keenetic router admin account.                     |
| `ALLOWED_USER_IDS`   | Yes      | Comma-separated Telegram user IDs allowed to interact with the bot. |
| `DEVICES_JSON`       | Yes      | JSON array of `[name, mac]` pairs describing selectable devices.    |
| `ROUTER_URL`         | No       | Router base URL (defaults to `http://192.168.1.1`).                 |
| `ROUTER_USER`        | No       | Router username (defaults to `admin`).                              |
| `VPN_POLICY_NAME`    | No       | Policy applied when VPN is enabled (defaults to `Policy0`).         |
| `NO_VPN_POLICY_NAME` | No       | Policy applied when VPN is disabled (defaults to `Policy1`).        |

Copy `.env.example` to `.env` and fill in your real values for local development.

```bash
cp .env.example .env
# edit .env with your secrets
```

## Local development

1. Install [uv](https://docs.astral.sh/uv/) (or use another Python packaging tool).
2. Install dependencies: `uv sync`.
3. Run the bot with your environment: `uv run --env-file .env python main.py`.

## Docker

Build and run the container locally:

```bash
docker build -t keenetic-vpn-switcher .
docker run --env-file .env keenetic-vpn-switcher
```

You can also supply variables inline, e.g. `docker run -e BOT_TOKEN=... -e ROUTER_PASSWORD=...`.

## GitHub Actions

The workflow in `.github/workflows/docker.yml` builds and pushes the Docker image
to GitHub Container Registry (`ghcr.io/<owner>/<repo>`) on every push to `main`.
Configure environment secrets (`BOT_TOKEN`, `ROUTER_PASSWORD`, etc.)
in your deployment environment or orchestrator when running the image.
