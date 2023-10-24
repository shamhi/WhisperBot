[<img src="https://img.shields.io/badge/Telegram-%40WhisperBot-blue">](https://t.me/shuser_whisper_bot)

# Whisper Bot

![speech_vibration](repo_images/speech_vibration.png)

#### Whisper - это незаменимый инструмент для всех, кто работает с аудио и видео файлами и хочет иметь возможность обрабатывать их прямо в Telegram. Он предоставляет широкий спектр функций, которые позволяют создавать профессионально звучащие аудио и видео материалы

## Технологии
* [**aiogram**](https://github.com/aiogram/aiogram) - работа с BotAPI;
* [**postgresql**](https://github.com/postgres/postgres) - работа с базой данных;
* [**cachetools**](https://cachetools.readthedocs.io/en/stable) - реализация троттлинга для борьбы с флудом;
* Systemd

## Установка
Вы можете клонировать [**репозиторий**](https://github.com/shamhi/whisper) на вашу систему и установить его необходимые требования следующим образом:
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
Скопируйте файл `env_example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое.
