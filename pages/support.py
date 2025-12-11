from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from translation import translation_loader as tl
from pages import common
from enum import Enum




async def _build_support_payload(context: ContextTypes.DEFAULT_TYPE):
    text = tl.load(tl.SUPPORT_TEXT, context)
    buttons = [
        [InlineKeyboardButton("Revolut", url="https://revolut.me/kseniialf")],
        [InlineKeyboardButton("Tinkoff", url="https://tbank.ru/cf/6jqmOPGfhZ8")],
        [InlineKeyboardButton(tl.load(tl.LABEL_BACK, context), callback_data=common.MainMenuCallback.BACK.value)],
    ]
    return text, InlineKeyboardMarkup(buttons)


async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    text, keyboard = await _build_support_payload(context)
    try:
        await query.edit_message_text(text, reply_markup=keyboard)
    except Exception:
        await query.message.delete()
        await context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=keyboard)


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, keyboard = await _build_support_payload(context)
    await update.message.reply_text(text, reply_markup=keyboard)
