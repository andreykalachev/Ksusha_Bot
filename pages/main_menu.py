from telegram import Update
from telegram.ext import ContextTypes
from pages.commands import articles_wrapper, contacts_wrapper, paintings_wrapper, services_wrapper, support_wrapper
from pages.info import show_info
from pages import common
from translation import translation_loader as tl

from translation.languages import Locale, LOCALE
from utils import statistics
from statistics.page_visits import Page

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == common.MainMenuCallback.INFO.value:
        await show_info(update, context)
    elif data == common.MainMenuCallback.PAINTINGS.value:
        await paintings_wrapper(update, context)
    elif data == common.MainMenuCallback.SERVICES.value:
        await services_wrapper(update, context)
    elif data == common.MainMenuCallback.ARTICLES.value:
        await articles_wrapper(update, context)
    elif data == common.MainMenuCallback.CONTACTS.value:
        await contacts_wrapper(update, context)
    elif data == common.MainMenuCallback.REVIEWS.value:
        from pages.reviews import show_reviews
        await show_reviews(update, context)
    elif data == common.MainMenuCallback.MINI_SHOP.value:
        from pages.mini_shop import show_mini_shop
        await show_mini_shop(update, context)
    elif data == common.MainMenuCallback.INSPIRATION.value:
        from pages.inspiration import show_inspiration
        await show_inspiration(update, context)
    elif data == common.MainMenuCallback.SUPPORT.value:
        await support_wrapper(update, context)
    elif data == common.MainMenuCallback.BACK.value:
        statistics.increment_page(Page.MAIN)
        greeting = tl.load(tl.ABOUT_TEXT, context)
        keyboard = common.get_main_keyboard(context, user_id=update.effective_user.id)
        await common.delete_stored_media_messages(context, context.bot, query.message.chat_id)
        try:
            await query.edit_message_text(greeting, reply_markup=keyboard)
        except Exception:
            await query.message.delete()
            await context.bot.send_message(chat_id=query.message.chat_id, text=greeting, reply_markup=keyboard)
    elif data == common.MainMenuCallback.SET_LANG_EN.value:
        statistics.increment_page(Page.MAIN)
        context.user_data[LOCALE] = Locale.EN.value
        keyboard = common.get_main_keyboard(context, user_id=update.effective_user.id)
        await query.edit_message_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)
    elif data == common.MainMenuCallback.SET_LANG_RU.value:
        statistics.increment_page(Page.MAIN)
        context.user_data[LOCALE] = Locale.RU.value
        keyboard = common.get_main_keyboard(context, user_id=update.effective_user.id)
        await query.edit_message_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)
    elif data == common.MainMenuCallback.STATISTICS.value:
        from pages.statistics import show_statistics
        await show_statistics(update, context)
