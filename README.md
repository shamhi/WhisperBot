[<img src="https://img.shields.io/badge/Telegram-%40WhisperBot-blue">](https://t.me/shuser_whisper_bot)

> 🇷🇺 README на русском доступен [здесь](README.ru.md)

# Whisper Bot

![speech_vibration](repo_images/speech_vibration.png)

#### Whisper is an indispensable tool for anyone who works with audio and video files and wants to be able to process them directly in Telegram. It provides a wide range of functions that allow you to create professional-sounding audio and video materials

## Technology
* [**aiogram**](https://github.com/aiogram/aiogram) - asyncio Telegram BotAPI framework;
* [**postgresql**](https://github.com/postgres/postgres) - working with DBMS;
* [**cachetools**](https://cachetools.readthedocs.io/en/stable) - for anti-flood throttling mechanism;
* Systemd

## Instalation
You can download [**Git Repo**](https://github.com/shamhi/whisper) by cloning on your system and installing its requirements:
```
~ >>> git clone https://github.com/shamhi/whisperbot.git
~ >>> cd whisperbot/

# Linux
~/whisperbot >>> python3 -m venv venv
~/whisperbot >>> source venv/bin/activate
~/whisperbot >>> pip3 install -r requirements.txt
~/whisperbot >>> python3 main.py

# Windows
~/whisperbot >>> python -m venv venv
~/whisperbot >>> .\venv\Scripts\activate
~/whisperbot >>> pip install -r requirements.txt
~/whisperbot >>> python main.py
```

Copy file `env_example` to `.env` (with leading dot), open and edit it.

