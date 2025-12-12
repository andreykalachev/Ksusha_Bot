from telegram import Update
from telegram.ext import ContextTypes
from . import common
from translation import translation_loader as tl
from utils import statistics
from statistics.page_visits import Page


async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    statistics.increment_page(Page.SERVICES)

    await query.edit_message_text(tl.load(tl.SERVICES_TEXT, context), reply_markup=common.get_back_keyboard(context), parse_mode='HTML')


async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    statistics.increment_page(Page.SERVICES)
    
    text = tl.load(tl.SERVICES_TEXT, context)
    await update.message.reply_text(text, reply_markup=common.get_back_keyboard(context), parse_mode='HTML')
