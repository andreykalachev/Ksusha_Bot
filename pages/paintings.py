from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from utils import statistics
from statistics.page_visits import Page
from typing import Tuple


BEHANCE_URL = os.getenv("BEHANCE_URL")
WEBSITE_URL = os.getenv("WEBSITE_URL")


def _build_paintings_payload(context: ContextTypes.DEFAULT_TYPE) -> Tuple[str, InlineKeyboardMarkup]:
    statistics.increment_page(Page.PAINTINGS)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_WEBSITE, context), url=WEBSITE_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_BEHANCE, context), url=BEHANCE_URL)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ])

    text = tl.load(tl.PAINTINGS_TEXT, context)
    return text, keyboard


async def show_paintings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, reply_markup = _build_paintings_payload(context)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def paintings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, reply_markup = _build_paintings_payload(context)
    await update.message.reply_text(text, reply_markup=reply_markup)


__all__ = ['show_paintings', 'paintings_command']
