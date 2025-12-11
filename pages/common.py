import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from translation import translation_loader as tl
from translation.languages import Language, Locale, LOCALE
from telegram.ext import ContextTypes
from typing import Optional
import asyncio
from enum import Enum
from utils import statistics
from statistics.page_visits import Page


class MainMenuCallback(str, Enum):
    INFO = 'info'
    PAINTINGS = 'paintings'
    SERVICES = 'services'
    ARTICLES = 'articles'
    CONTACTS = 'contacts'
    REVIEWS = 'reviews'
    MINI_SHOP = 'mini_shop'
    INSPIRATION = 'inspiration'
    SUPPORT = 'support'
    CERTIFICATE = 'show_certificate'
    BACK = 'back'
    STATISTICS = 'statistics'
    SET_LANG_EN = 'set_lang_en'
    SET_LANG_RU = 'set_lang_ru'


def is_admin(user_id: int) -> bool:
    admin_user_ids = os.getenv("ADMIN_USER_IDS", "")
    return str(user_id) in admin_user_ids


def get_locale(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get(LOCALE, Locale.RU.value)


def get_main_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id: int = None) -> InlineKeyboardMarkup:
    locale = get_locale(context)
    if locale == Locale.RU.value:
        lang_row = [InlineKeyboardButton(Language.ENGLISH.value, callback_data=MainMenuCallback.SET_LANG_EN.value)]
    else:
        lang_row = [InlineKeyboardButton(Language.RUSSIAN.value, callback_data=MainMenuCallback.SET_LANG_RU.value)]

    buttons = [
        [InlineKeyboardButton(tl.load(tl.LABEL_INFO, context), callback_data=MainMenuCallback.INFO.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_PAINTINGS, context), callback_data=MainMenuCallback.PAINTINGS.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_SERVICES, context), callback_data=MainMenuCallback.SERVICES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_ARTICLES, context), callback_data=MainMenuCallback.ARTICLES.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_MINI_SHOP, context), callback_data=MainMenuCallback.MINI_SHOP.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_INSPIRATION_GENERATOR, context), callback_data=MainMenuCallback.INSPIRATION.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_REVIEWS, context), callback_data=MainMenuCallback.REVIEWS.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_CONTACTS, context), callback_data=MainMenuCallback.CONTACTS.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_SUPPORT, context), callback_data=MainMenuCallback.SUPPORT.value)],
    ]

    if user_id and is_admin(user_id):
        buttons.append([InlineKeyboardButton(tl.load(tl.LABEL_STATISTICS, context), callback_data=MainMenuCallback.STATISTICS.value)])

    buttons.append(lang_row)

    return InlineKeyboardMarkup(buttons)


def get_back_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=MainMenuCallback.BACK.value)],
    ])


# Key in user_data to store last sent media group message ids
SENT_MEDIA_MESSAGE_IDS = "sent_media_message_ids"


def store_media_message_ids(context: ContextTypes.DEFAULT_TYPE, message_ids: list[int]):
    context.user_data[SENT_MEDIA_MESSAGE_IDS] = message_ids


def pop_media_message_ids(context: ContextTypes.DEFAULT_TYPE) -> Optional[list[int]]:
    return context.user_data.pop(SENT_MEDIA_MESSAGE_IDS, None)


async def delete_stored_media_messages(context: ContextTypes.DEFAULT_TYPE, bot, chat_id: int) -> None:
    ids = context.user_data.pop(SENT_MEDIA_MESSAGE_IDS, None)
    if not ids:
        return
    try:
        await asyncio.gather(*(bot.delete_message(chat_id=chat_id, message_id=m_id) for m_id in ids))
    except Exception:
        pass


async def main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    statistics.increment_page(Page.MAIN)
    keyboard = get_main_keyboard(context, user_id=update.effective_user.id)
    await update.message.reply_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)

async def admin_file_handler(update, context):
    if is_admin(update.effective_user.id):
        if update.message.document:
            await update.message.reply_text(f"`{update.message.document.file_id}`", parse_mode='Markdown')
        elif update.message.photo:
            await update.message.reply_text(f"`{update.message.photo[-1].file_id}`", parse_mode='Markdown')