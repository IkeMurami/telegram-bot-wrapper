# Telegram bot wrapper

Использую пакет [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) ([docs](https://python-telegram-bot.org/))

В своей надстройке стараюсь:

- инкапсулировать настройку бота
- оставить только добавление хендлеров
- преобразовать настройку бота в плоский список параметров конструктора

PS: возможно, это не будет лучше, чем исходный пакет, но для меня будет понятнее как использовать его :)

## Build and run

Install

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "."
```

Put a telegram bot token to `examples/.env`

```
cd examples
python -B main.py
```
