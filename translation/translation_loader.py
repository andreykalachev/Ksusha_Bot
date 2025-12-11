REVIEWS_TEXT = 'REVIEWS_TEXT'
LABEL_REVIEWS_LINK = 'LABEL_REVIEWS_LINK'
MINI_SHOP_TEXT = 'MINI_SHOP_TEXT'
SUPPORT_TEXT = 'SUPPORT_TEXT'
SUPPORT_NOTE = 'SUPPORT_NOTE'
LABEL_SUPPORT = 'LABEL_SUPPORT'
LABEL_SUPPORT_PAY = 'LABEL_SUPPORT_PAY'
MINI_SHOP_IMG_1 = 'MINI_SHOP_IMG_1'
MINI_SHOP_IMG_2 = 'MINI_SHOP_IMG_2'
LABEL_CERTIFICATE = 'LABEL_CERTIFICATE'
CERTIFICATE_TEXT = 'CERTIFICATE_TEXT'
LABEL_ARTIST_DAY = 'LABEL_ARTIST_DAY'
LABEL_INSPIRATION = 'LABEL_INSPIRATION'
INSPIRATION_TEXT = 'INSPIRATION_TEXT'
LABEL_INSPIRATION_LINK = 'LABEL_INSPIRATION_LINK'
from typing import Dict
from pathlib import Path
import yaml
from telegram.ext import ContextTypes
from pages import common

_cache: Dict[str, Dict[str, str]] = {}

# Exported keys
ABOUT_TEXT = 'ABOUT_TEXT'
LABEL_INFO = 'LABEL_INFO'
LABEL_STATISTICS = 'LABEL_STATISTICS'
INFO_TEXT = 'INFO_TEXT'
LABEL_MINI_SHOP = 'LABEL_MINI_SHOP'
LABEL_REVIEWS = 'LABEL_REVIEWS'
LABEL_SERVICES = 'LABEL_SERVICES'
LABEL_PAINTINGS = 'LABEL_PAINTINGS'
LABEL_ARTICLES = 'LABEL_ARTICLES'
LABEL_BACK = 'LABEL_BACK'
LABEL_QUIZ = 'LABEL_QUIZ'
LABEL_GUIDE = 'LABEL_GUIDE'
LABEL_MAIN_MENU = 'LABEL_MAIN_MENU'
SERVICES_TEXT = 'SERVICES_TEXT'
PAINTINGS_TEXT = 'PAINTINGS_TEXT'
GUIDE_GREET = 'GUIDE_GREET'
GUIDE_TEXT = 'GUIDE_TEXT'
LABEL_CONTACTS = 'LABEL_CONTACTS'
CONTACTS_TEXT = 'CONTACTS_TEXT'
CONTACTS_BTN_TELEGRAM = 'CONTACTS_BTN_TELEGRAM'
CONTACTS_BTN_CHANNEL = 'CONTACTS_BTN_CHANNEL'
CONTACTS_BTN_INSTAGRAM = 'CONTACTS_BTN_INSTAGRAM'
CONTACTS_BTN_BEHANCE = 'CONTACTS_BTN_BEHANCE'
CONTACTS_BTN_WEBSITE = 'CONTACTS_BTN_WEBSITE'
ARTICLES_MENU_GREETING = 'ARTICLES_MENU_GREETING'
LABEL_INSPIRATION_GENERATOR = 'LABEL_INSPIRATION_GENERATOR'
INSPIRATION_INTRO = 'INSPIRATION_INTRO'
INSPIRATION_OUTRO = 'INSPIRATION_OUTRO'
INSPIRATION_CARDS = 'INSPIRATION_CARDS'
LABEL_INSPIRATION_NEW = 'LABEL_INSPIRATION_NEW'


def _load_locale(locale: str) -> Dict[str, str]:
    if locale in _cache:
        return _cache[locale]
    base = Path(__file__).parent
    # prefer YAML files for human-friendly multiline support
    yaml_path = base / f"translations.{locale}.yaml"
    if yaml_path.exists():
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        _cache[locale] = data
        return data

    # final fallback: Russian YAML
    ru_yaml = base / 'translations.ru.yaml'
    if ru_yaml.exists():
        with open(ru_yaml, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        _cache[locale] = data
        return data

    _cache[locale] = {}
    return {}


def load(key: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    locale = common.get_locale(context)
    data = _load_locale(locale)
    return data.get(key, key)
