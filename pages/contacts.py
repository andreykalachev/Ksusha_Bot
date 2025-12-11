from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from translation.languages import Locale
from utils import statistics
from statistics.page_visits import Page

TG_URL = os.getenv("TG_URL")
TG_CHANNEL_URL = os.getenv("TG_CHANNEL_URL")
INSTAGRAM_RU = os.getenv("INSTAGRAM_RU")
INSTAGRAM_EN = os.getenv("INSTAGRAM_EN")
BEHANCE_URL = os.getenv("BEHANCE_URL")


def _build_contacts_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.CONTACTS)

    locale = common.get_locale(context)
    instagram = INSTAGRAM_RU if locale == Locale.RU.value else INSTAGRAM_EN

    keyboard = [
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_TELEGRAM, context), url=TG_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_CHANNEL, context), url=TG_CHANNEL_URL)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_INSTAGRAM, context), url=instagram)],
        [InlineKeyboardButton(tl.load(tl.CONTACTS_BTN_BEHANCE, context), url=BEHANCE_URL)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.CONTACTS_TEXT, context)
    return text, reply_markup


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text, reply_markup = _build_contacts_payload(context)
    await query.edit_message_text(text, reply_markup=reply_markup)


async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, reply_markup = _build_contacts_payload(context)
    await update.message.reply_text(text, reply_markup=reply_markup)
