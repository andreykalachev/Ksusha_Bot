from telegram import Update
from telegram.ext import ContextTypes
from pages.common import get_main_keyboard

from utils.logging_config import configure_logging
from translation import translation_loader as tl
from pages.contacts import contacts_command, show_contacts
from pages.articles.menu import articles_command, show_articles_menu
from pages.paintings import paintings_command, show_paintings
from pages.services import services_command, show_services
from pages.mini_shop import mini_shop_command, show_mini_shop
from pages.info import info_command, show_info
from pages.reviews import reviews_command, show_reviews
from pages.support import support_command, show_support
from utils import statistics

logger = configure_logging()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(
        "Received /start from user id=%s, username=%s",
        user.id if user else None,
        getattr(user, 'username', None),
    )

    statistics.increment_bot_start(user.id if user else None)

    keyboard = get_main_keyboard(context)
    await update.message.reply_text(tl.load(tl.ABOUT_TEXT, context), reply_markup=keyboard)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(
        "Received unknown command from user: %s",
        update.effective_user.id if update.effective_user else None,
    )
    await update.message.reply_text(tl.load(tl.UNKNOWN_COMMAND, context))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(tl.load(tl.HELP_TEXT, context))


async def contacts_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_contacts(update, context)
    else:
        await contacts_command(update, context)


async def support_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_support(update, context)
    else:
        await support_command(update, context)


async def articles_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_articles_menu(update, context)
    else:
        await articles_command(update, context)


async def paintings_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_paintings(update, context)
    else:
        await paintings_command(update, context)


async def services_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_services(update, context)
    else:
        await services_command(update, context)


async def mini_shop_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_mini_shop(update, context)
    else:
        await mini_shop_command(update, context)


async def info_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_info(update, context)
    else:
        await info_command(update, context)


async def reviews_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await show_reviews(update, context)
    else:
        await reviews_command(update, context)
