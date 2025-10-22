import asyncio
import hashlib
import logging

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    ALLOWED_USER_IDS,
    BOT_TOKEN,
    DEVICES,
    NO_VPN_POLICY,
    PASSWORD,
    ROUTER,
    USER,
    VPN_POLICY,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def is_allowed(user_id: int | None) -> bool:
    return user_id is not None and user_id in ALLOWED_USER_IDS


def get_policy(vpn_enabled: bool) -> str:
    return VPN_POLICY if vpn_enabled else NO_VPN_POLICY


def do_post(session: requests.Session, url: str, json: dict | None = None) -> None:
    payload = json or {}
    response = session.post(url, json=payload, timeout=5)

    response.raise_for_status()
    if "error" in response.text.lower():
        raise RuntimeError(response.text)


def authenticate(session: requests.Session) -> None:
    response = session.get(f"{ROUTER}/auth", timeout=5)

    if response.status_code == 401:
        realm = response.headers["X-NDM-Realm"]
        chall = response.headers["X-NDM-Challenge"]

        md5 = hashlib.md5(f"{USER}:{realm}:{PASSWORD}".encode()).hexdigest()
        sha = hashlib.sha256((chall + md5).encode()).hexdigest()

        do_post(session, f"{ROUTER}/auth", {"login": USER, "password": sha})


def set_policy(session: requests.Session, mac: str, policy: str) -> None:
    payload = {
        "mac": mac,
        "permit": True,
        "policy": policy,
    }

    do_post(session, f"{ROUTER}/rci/ip/hotspot/host", payload)
    do_post(session, f"{ROUTER}/rci/system/configuration/save")


def apply_policy_sync(device_index: int, enable_vpn: bool) -> str:
    name, mac = DEVICES[device_index]
    policy = get_policy(enable_vpn)

    with requests.Session() as session:
        authenticate(session)
        set_policy(session, mac, policy)

    return f"✅ Turned {'on' if enable_vpn else 'off'} VPN for {name}."


def build_device_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=name, callback_data=f"device:{idx}")]
        for idx, (name, _mac) in enumerate(DEVICES)
    ]
    return InlineKeyboardMarkup(rows)


def build_action_keyboard(device_index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🟢 On", callback_data=f"action:{device_index}:on"
                ),
                InlineKeyboardButton(
                    "🔴 Off", callback_data=f"action:{device_index}:off"
                ),
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
        ]
    )


async def show_device_menu(message, prompt: str = "🔄 Select a device:") -> None:
    await message.reply_text(f"{prompt}", reply_markup=build_device_keyboard())


async def handle_start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_allowed(user.id if user else None):
        LOGGER.warning(
            "Rejected /start from unauthorized user %s", user.id if user else "unknown"
        )
        return

    if update.message:
        user_id = user.id if user else "unknown"
        LOGGER.info("Serving device menu to user %s via /start", user_id)
        await show_device_menu(update.message)


async def handle_text(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_allowed(user.id if user else None):
        LOGGER.warning(
            "Rejected text message from unauthorized user %s",
            user.id if user else "unknown",
        )
        return

    if update.message:
        user_id = user.id if user else "unknown"
        LOGGER.info("Serving device menu to user %s via text", user_id)
        await show_device_menu(update.message)


async def handle_unauthorized(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    LOGGER.warning(
        "Blocked update from unauthorized user %s", user.id if user else "unknown"
    )


async def handle_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    user = query.from_user
    if not is_allowed(user.id if user else None):
        LOGGER.warning(
            "Rejected callback from unauthorized user %s",
            user.id if user else "unknown",
        )
        await query.answer()
        return

    data = query.data or ""

    if data == "back":
        user_id = user.id if user else "unknown"
        LOGGER.info("User %s navigated back to device menu", user_id)
        await query.answer()
        await query.edit_message_text(
            "🔄 Select a device:", reply_markup=build_device_keyboard()
        )
        return

    if data.startswith("device:"):
        await query.answer()
        try:
            device_index = int(data.split(":", maxsplit=1)[1])
            name, _mac = DEVICES[device_index]
        except (ValueError, IndexError):
            user_id = user.id if user else "unknown"
            LOGGER.warning("User %s selected unknown device payload %s", user_id, data)
            await query.edit_message_text("❌ Unknown device.")
            return

        user_id = user.id if user else "unknown"
        LOGGER.info("User %s selected device %s", user_id, name)
        await query.edit_message_text(
            f"🔄 Choose VPN action for {name}:",
            reply_markup=build_action_keyboard(device_index),
        )
        return

    if data.startswith("action:"):
        parts = data.split(":")
        if len(parts) != 3:
            await query.answer()
            return

        _, index_str, action = parts
        try:
            device_index = int(index_str)
            name, _mac = DEVICES[device_index]
        except (ValueError, IndexError):
            await query.answer()
            LOGGER.warning(
                "User %s triggered action with unknown device payload %s",
                user.id if user else "unknown",
                data,
            )
            await query.edit_message_text("❌ Unknown device.")
            return

        enable_vpn = action == "on"
        await query.answer("⏳ Applying…", show_alert=False)
        await query.edit_message_text(
            f"⏳ Turning {'on' if enable_vpn else 'off'} VPN for {name}…"
        )

        try:
            result = await asyncio.to_thread(
                apply_policy_sync, device_index, enable_vpn
            )
        except Exception as exc:
            LOGGER.exception(
                "Failed to apply policy for %s (user=%s, action=%s)",
                name,
                user.id if user else "unknown",
                action,
            )
            await query.edit_message_text(
                f"❌ Failed to turn {'on' if enable_vpn else 'off'} VPN for {name}: {exc}"
            )
        else:
            LOGGER.info(
                "Applied policy for %s (user=%s, action=%s)",
                name,
                user.id if user else "unknown",
                action,
            )
            await query.edit_message_text(result)
            if query.message:
                await query.message.reply_text(
                    "🔄 Select another device:", reply_markup=build_device_keyboard()
                )


def build_application(include_handlers: bool = True) -> Application:
    application = Application.builder().token(BOT_TOKEN).build()

    if include_handlers:
        allowed_filter = filters.User(ALLOWED_USER_IDS)
        application.add_handler(
            CommandHandler("start", handle_start, filters=allowed_filter)
        )
        application.add_handler(
            MessageHandler(
                allowed_filter & filters.TEXT & ~filters.COMMAND, handle_text
            )
        )
        application.add_handler(
            MessageHandler(~allowed_filter & filters.TEXT, handle_unauthorized)
        )
        application.add_handler(CallbackQueryHandler(handle_callback))

    return application


def run_bot() -> None:
    application = build_application()
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    run_bot()
