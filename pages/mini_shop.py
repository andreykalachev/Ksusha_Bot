from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
import os
from pages import common
from translation import translation_loader as tl
from translation.languages import Locale
from utils import statistics
from statistics.page_visits import Page

# RU images
MINI_SHOP_IMG_RU_1 = os.getenv("MINI_SHOP_IMG_RU_1")
MINI_SHOP_IMG_RU_2 = os.getenv("MINI_SHOP_IMG_RU_2")
# EN images
MINI_SHOP_IMG_EN_1 = os.getenv("MINI_SHOP_IMG_EN_1")
MINI_SHOP_IMG_EN_2 = os.getenv("MINI_SHOP_IMG_EN_2")


def _build_mini_shop_payload(context: ContextTypes.DEFAULT_TYPE):
    statistics.increment_page(Page.MINI_SHOP)
    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_CERTIFICATE, context), callback_data=common.MainMenuCallback.CERTIFICATE.value)],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = tl.load(tl.MINI_SHOP_TEXT, context)
    return text, reply_markup


async def show_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    try:
        await query.message.delete()
    except Exception:
        pass
    
    locale = common.get_locale(context)
    if locale == Locale.RU.value:
        images = [MINI_SHOP_IMG_RU_1, MINI_SHOP_IMG_RU_2]
    else:
        images = [MINI_SHOP_IMG_EN_1, MINI_SHOP_IMG_EN_2]
        
    media = [InputMediaPhoto(media=img_id) for img_id in images]
    media_messages = await context.bot.send_media_group(chat_id=chat_id, media=media)
    message_ids = [m.message_id for m in media_messages]
    common.store_media_message_ids(context, message_ids)
    
    # Send follow-up message with Back button
    keyboard = [
        [InlineKeyboardButton(tl.load(tl.LABEL_MAIN_MENU, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=tl.load(tl.CERTIFICATE_TEXT, context), reply_markup=reply_markup)


async def show_mini_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text, reply_markup = _build_mini_shop_payload(context)
    
    # If the previous message was a text message (e.g. main menu), edit it.
    # If it was something else (e.g. we are coming back from somewhere else), 
    # we might need to delete and send new, but edit_message_text is usually safe for menus.
    try:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    except Exception:
        # Fallback: delete and send new if edit fails (e.g. if previous was a photo)
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text,
            reply_markup=reply_markup
        )


async def mini_shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = _build_mini_shop_payload(context)
    await update.message.reply_text(text=text, reply_markup=reply_markup)
