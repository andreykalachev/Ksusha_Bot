from __future__ import annotations

import json
from pathlib import Path
from statistics.statistics_model import StatisticsModel
from statistics.page_visits import Page


_STATS_FILE = Path(__file__).resolve().parent.parent / "statistics" / "data" / "stats.json"


def _ensure_file() -> None:
    _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not _STATS_FILE.exists() or _STATS_FILE.stat().st_size == 0:
        model = StatisticsModel()
        model.reset()
        _STATS_FILE.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")


def _load() -> StatisticsModel:
    _ensure_file()
    with _STATS_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return StatisticsModel.from_dict(raw if isinstance(raw, dict) else {})


def _save(model: StatisticsModel) -> None:
    _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _STATS_FILE.write_text(json.dumps(model.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")


from telegram import Bot
from telegram.helpers import escape_markdown

# Load model once on import and keep it in memory. Write on every update.
_MODEL: StatisticsModel = _load()


def increment_bot_start(user_id: int | None = None) -> None:
    _MODEL.bot_starts += 1
    _MODEL.page_visits.increment(Page.MAIN)
    if user_id is not None:
        if user_id not in _MODEL.unique_users:
            _MODEL.unique_users.append(user_id)
            
    _save(_MODEL)


def increment_page(page: Page) -> None:
    _MODEL.page_visits.increment(page)
    _save(_MODEL)


def reset() -> StatisticsModel:
    _MODEL.reset()
    _save(_MODEL)
    return _MODEL


def get_unique_users_count() -> int:
    return len(_MODEL.unique_users)


def format_model(model: StatisticsModel, last_users_with_indices: list[tuple[int, str]] | None = None) -> str:
    pv = model.page_visits
    last_reset = model.last_reset if model.last_reset else "never"

    # Format last users list. Escape user-provided names to avoid breaking Markdown parsing.
    if last_users_with_indices:
        last_users_str = "\n".join(
            [f"{idx}. {escape_markdown(name, version=1)}" for idx, name in last_users_with_indices]
        )
    else:
        last_users_str = "No users in this range."

    lines = [
        "📊 *Statistics*",
        "",
        "*This page is for admins only. If you are not an admin, please contact @kseniialf*",
        "",
        f"🚀 *Bot Starts*: {model.bot_starts}",
        f"👤 *Unique Users*: {len(model.unique_users)}",
        "",
        "📱 *Page Visits*:",
        f"  • Main: {pv.main}",
        f"  • Guide: {pv.guide}",
        f"  • Contacts: {pv.contacts}",
        f"  • Paintings: {pv.paintings}",
        f"  • Services: {pv.services}",
        f"  • Info: {pv.info}",
        f"  • Reviews: {pv.reviews}",
        f"  • Mini Shop: {pv.mini_shop}",
        f"  • Inspiration: {pv.inspiration}",
        "",
        f"🕒 *Last Reset*: {last_reset}",
        "",
        "👥 *Users Log*:",
        last_users_str
    ]
    return "\n".join(lines)


async def get_stats_text(bot: Bot, offset: int = 0, limit: int = 10) -> str:
    total_users = len(_MODEL.unique_users)
    end_index = total_users - offset
    start_index = max(0, end_index - limit)
    
    recent_users_ids = []
    if end_index > 0:
        recent_users_ids = _MODEL.unique_users[start_index:end_index]
    
    users_with_indices = []
    for i, user_id in enumerate(recent_users_ids):
        real_index = start_index + i + 1
        try:
            chat = await bot.get_chat(user_id)
            name = f"@{chat.username}" if chat.username else f"{chat.first_name} {chat.last_name or ''}".strip()
        except Exception:
            name = f"ID:{user_id}"
        users_with_indices.append((real_index, name))
            
    return format_model(_MODEL, users_with_indices)
