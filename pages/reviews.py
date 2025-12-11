from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from translation.languages import LOCALE, Locale
from utils import statistics
from statistics.page_visits import Page

REVIEWS_URL = os.getenv("REVIEWS_URL")

RU_REVIEW_PHOTOS = [
    "AgACAgIAAxkBAAID5Wk7HpikSBYEJRIDJZ7fcoQHB25UAAIYDWsbeNvZSVXsfw1JHjvDAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAID5mk7HpiTsnZI3vZkECB2HkEtlZvcAAIZDWsbeNvZScvWiP5zh6EAAQEAAwIAA3kAAzYE",
    "AgACAgIAAxkBAAID52k7HphSoEmTkBiraavZyTc46jS4AAIaDWsbeNvZSfGyC5AX8Vi-AQADAgADeQADNgQ",
    "AgACAgIAAxkBAAID6Gk7HpjQw0zMXCXzHHSTdD7t04O7AAIbDWsbeNvZSTE-5Whd-ajJAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAID6Wk7HphC64FC_pKPiy0E6oV3sB-DAAIcDWsbeNvZSTM-atiNQS_8AQADAgADeQADNgQ",
    "AgACAgIAAxkBAAID6mk7HpjQ-Xa9SZhKxvvkpDHQWPQHAAIdDWsbeNvZSYaGo3kuked4AQADAgADeQADNgQ"
]

EN_REVIEW_PHOTOS = [
    "AgACAgIAAxkBAAID8Wk7HqVbszaZ0fPzIZYK-Hg94Kq4AALKC2sbdXDgSVej3H7bA6WoAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAID8mk7HqVVDB8zozTSUuIu2ZnwXnAzAALLC2sbdXDgSe3ttwez_R7nAQADAgADeQADNgQ"
]

def _build_reviews_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.REVIEWS)
    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_REVIEWS_LINK, context), url=REVIEWS_URL)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.REVIEWS_TEXT, context)
    return text, reply_markup

def _get_photos(context: ContextTypes.DEFAULT_TYPE):
    user_locale = context.user_data.get(LOCALE)
    if user_locale == Locale.EN.value:
        return EN_REVIEW_PHOTOS
    return RU_REVIEW_PHOTOS

async def show_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        await query.message.delete()
    except Exception:
        pass

    photos = _get_photos(context)
    media_group = [InputMediaPhoto(media=photo) for photo in photos]
    
    if media_group:
        media_messages = await context.bot.send_media_group(chat_id=query.message.chat_id, media=media_group)
        try:
            message_ids = [m.message_id for m in media_messages]
            common.store_media_message_ids(context, message_ids)
        except Exception:
            pass

    text, reply_markup = _build_reviews_payload(context)
    await context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=reply_markup)


async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = _get_photos(context)
    media_group = [InputMediaPhoto(media=photo) for photo in photos]
    
    if media_group:
        media_messages = await update.message.reply_media_group(media=media_group)
        try:
            message_ids = [m.message_id for m in media_messages]
            common.store_media_message_ids(context, message_ids)
        except Exception:
            pass

    text, reply_markup = _build_reviews_payload(context)
    await update.message.reply_text(text=text, reply_markup=reply_markup)
