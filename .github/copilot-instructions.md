# Ksusha Bot - AI Coding Instructions

## Project Overview
This is a Telegram bot built with `python-telegram-bot` (v20+ async) for an art-related service (Ksusha). It features a main menu, articles, a quiz (via Telegram Web App), and contact info.

## Architecture
- **Entry Point**: `bot.py` initializes the `Application`, `ConversationHandler`, and global handlers.
- **Modular Design**: Feature logic is split into `pages/` (e.g., `main_menu.py`, `articles/`, `contacts.py`).
- **State Management**: Uses `telegram.ext.ConversationHandler`. States are defined in `pages/states.py` (e.g., `MENU`, `ARTICLES_MENU`, `QUIZ`).
- **Translations**: Custom translation system in `translation/`. All user-facing text MUST use `translation_loader.load(key, context)`.
- **Data**: Quiz data stored in JSON. Statistics in `statistics/`.

## Coding Conventions

### Telegram Handlers
- **Async/Await**: All handlers must be `async`.
- **Context**: Use `context: ContextTypes.DEFAULT_TYPE` for type hinting.
- **Callback Queries**:
  - Always call `await query.answer()` at the start of callback handlers.
  - Use `Enum` classes for callback data (e.g., `ArticleCallback`, `MainMenuCallback`).
  - When a handler covers multiple buttons (e.g., a menu state), dispatch logic based on `query.data` explicitly.
  - Return the next state (e.g., `return MENU`) to transition or maintain state.

### Translations
- **Never hardcode text**. Add keys to `translation/translations.{lang}.yaml` and constants to `translation/translation_loader.py`.
- **Structure**: Keep translation files organized in the following order:
  1. **Business Entities** (Long texts, descriptions, messages)
  2. **Feature Labels** (Button labels, short titles)
  3. **Navigation & System** (Back buttons, common commands, language names)
- Usage: `text = tl.load(tl.SOME_KEY, context)`
- Locale is stored in `context.user_data[LOCALE]`.

### UI/UX
- **Inline Keyboards**: Use `InlineKeyboardMarkup` for menus.
- **Message Editing**: Prefer `query.edit_message_text` over sending new messages for menu navigation to reduce clutter.
- **Web Apps**: Use `WebAppInfo` for complex interactions like the Quiz.

## Key Workflows

### Local Development
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Ensure .env has TELEGRAM_TOKEN
python bot.py
```

### Deployment (VPS)
Refer to `readme.txt` for `rsync` and `screen` commands.
```bash
# Update code
rsync -avz --delete --exclude 'venv' --exclude '.env' --exclude 'git' ./ root@<host>:~/ksusha_bot
# Restart bot
screen -S ksusha -X quit || true
screen -S ksusha -dm bash -lc "source ksusha_env.sh && venv/bin/python bot.py"
```

## Common Pitfalls
- **"Message is not modified"**: If a handler rebuilds the same menu without checking `query.data`, `edit_message_text` will raise `BadRequest`. Ensure logic handles specific actions (like navigation) before falling back to "refreshing" the view.
- **Circular Imports**: `pages/` modules often reference each other. Use local imports inside functions if necessary to avoid cycles.

## Additional AI Coding Rules

- **Minimize comments**: Add comments only for critical logic or non-obvious code. Avoid excessive or obvious comments.
- **Avoid try/except**: Do not use try/except unless error handling is absolutely necessary for user experience or data integrity.
- **File updates**: Never use terminal commands (like `sed`, `awk`, `perl`, etc.) to update file contents. Always use file editing tools directly.
