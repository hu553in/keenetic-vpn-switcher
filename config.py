import json
import os
from typing import Any


def _get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def _require(value: str | None, env_name: str) -> str:
    if value is None:
        raise RuntimeError(f"Environment variable {env_name} is required but missing.")
    return value


def _parse_allowed_users(raw: str | None) -> list[int]:
    if not raw:
        raise RuntimeError(
            "ALLOWED_USER_IDS must be set to a comma-separated list of Telegram user IDs."
        )

    ids: list[int] = []
    for token in raw.split(","):
        stripped = token.strip()
        if not stripped:
            continue
        try:
            ids.append(int(stripped))
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid Telegram user id '{stripped}' in ALLOWED_USER_IDS."
            ) from exc

    if not ids:
        raise RuntimeError(
            "ALLOWED_USER_IDS must contain at least one valid Telegram user id."
        )

    return ids


def _parse_devices(raw: str | None) -> list[list[str]]:
    if raw is None:
        raise RuntimeError(
            "DEVICES_JSON must be set to a valid JSON array of [name, mac] pairs."
        )

    try:
        decoded: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("DEVICES_JSON must be valid JSON.") from exc

    if not isinstance(decoded, list):
        raise RuntimeError("DEVICES_JSON must decode to a list of [name, mac] pairs.")

    validated: list[list[str]] = []
    for entry in decoded:
        if not isinstance(entry, (list, tuple)) or len(entry) != 2:
            raise RuntimeError(
                "Each device entry must be a two-item list of [name, mac] in DEVICES_JSON."
            )
        name, mac = entry
        if not isinstance(name, str) or not isinstance(mac, str):
            raise RuntimeError(
                "Device name and mac must both be strings in DEVICES_JSON."
            )
        validated.append([name, mac])

    if not validated:
        raise RuntimeError("DEVICES_JSON must contain at least one device entry.")

    return validated


ROUTER = _get_env("ROUTER_URL", "http://192.168.1.1")
USER = _get_env("ROUTER_USER", "admin")
PASSWORD = _require(_get_env("ROUTER_PASSWORD"), "ROUTER_PASSWORD")

BOT_TOKEN = _require(_get_env("BOT_TOKEN"), "BOT_TOKEN")
ALLOWED_USER_IDS = _parse_allowed_users(_get_env("ALLOWED_USER_IDS"))

DEVICES = _parse_devices(_get_env("DEVICES_JSON"))

VPN_POLICY = _get_env("VPN_POLICY_NAME", "Policy0")
NO_VPN_POLICY = _get_env("NO_VPN_POLICY_NAME", "Policy1")
