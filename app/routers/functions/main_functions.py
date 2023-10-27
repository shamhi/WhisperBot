from googletrans import Translator
from app.config import EDEN_API
from moviepy.editor import VideoFileClip
import aiohttp
import requests
import json

translator = Translator()

api = EDEN_API


def detect_language(text):
    try:
        detected = translator.detect(text)
        lang_code = detected.lang

        return lang_code
    except:
        return


def translate_text(text, data):
    lang_data = {
        'stt_ru': 'ru',
        'stt_en': 'en',
        'stt_es': 'es',
        'stt_fr': 'fr',
        'stt_de': 'de',
        'stt_cn': 'zh-CN'
    }
    lang_code = detect_language(text=text)
    if lang_code not in lang_data.values():
        return
    lang_dest = lang_data.get(data)
    if lang_dest != lang_code:
        translated_text = translator.translate(text=text, dest=lang_dest).text
        return translated_text
    else:
        return


def check_stt_lang(text):
    lang_data = {
        "ru": "Ваш текст уже Ru",
        "en": "Your text is already En",
        "es": "Su texto ya está Es",
        "fr": "Votre texte est déjà Fr",
        "de": "Ihr Text ist bereits De",
        "zh-CN": "您的文本已经 Cn"
    }
    lang_code = detect_language(text=text)

    return lang_data.get(lang_code)


async def create_audio(data):
    voices = {
        'ru': {'MALE': {'Sasha': ['google', 'ru-RU-Standard-B'], 'Maxim': ['amazon', 'ru-RU_Maxim_Standard']},
               'FEMALE': {'Elena': ['google', 'ru-RU-Standard-C'], 'Tatyana': ['amazon', 'ru-RU_Tatyana_Standard']}},
        'en': {'MALE': {'Kevin': ['google', 'en-US-Standard-B'], 'Justin': ['amazon', 'en-US_Justin_Standard']},
               'FEMALE': {'Emma': ['google', 'en-US-Standard-C'], 'Joanna': ['amazon', 'en-US_Joanna_Neural']}}
    }

    try:
        lang = data.get('lang')
        gender = str(data.get('tts_gender')).upper()
        person = data.get('tts_person')
        text = data.get('tts_text')

        provider = voices[lang][gender][person]

        headers = {"Authorization": f"Bearer {api}"}
        url = "https://api.edenai.run/v2/audio/text_to_speech"

        payload = {
            'providers': provider[0],
            'language': lang,
            'option': gender,
            provider[0]: provider[1],
            'text': text
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, json=payload, headers=headers)
            content = await response.text()
            result = json.loads(content)

        audio_url = result.get(provider[0]).get('audio_resource_url')

        return audio_url
    except Exception:
        return


async def get_stt(file_bytes):
    try:
        url = "https://api.edenai.run/v2/audio/speech_to_text_async"
        headers = {"Authorization": f"Bearer {api}"}
        data = {"providers": "openai", "language": "ru-RU"}
        files = {'file': file_bytes}

        response = requests.post(url, data=data, files=files, headers=headers)
        result = json.loads(response.text)
        public_id = result['public_id']
        result = json.loads(requests.get(f'https://api.edenai.run/v2/audio/speech_to_text_async/{public_id}',
                                         headers=headers).content.decode())
        text = result['results']['openai']['text']

        return text
    except Exception:
        return


async def get_duration(message, content_type):
    duration = 0

    match content_type:
        case 'audio':
            duration = message.audio.duration
        case 'voice':
            duration = message.voice.duration
        case 'video':
            duration = message.video.duration

    return duration


async def get_file_id(message, content_type):
    file_id = ''

    match content_type:
        case 'audio':
            file_id = message.audio.file_id
        case 'voice':
            file_id = message.voice.file_id
        case 'video':
            file_id = message.video.file_id

    return file_id


async def get_file_bytes(downloaded_file):
    file_bytes = downloaded_file.read()

    with open('app/audio_temp/audio.mp3', 'wb') as file:
        file.write(file_bytes)

    file_bytes = open('app/audio_temp/audio.mp3', 'rb')

    return file_bytes


async def get_audiotrack(downloaded_file):
    video_bytes = downloaded_file.read()

    with open('app/video_temp/video.mp4', 'wb') as file:
        file.write(video_bytes)

    video = VideoFileClip('app/video_temp/video.mp4')
    audio = video.audio
    audio.write_audiofile(filename='app/video_temp/audio.mp3')

    return 'app/video_temp/audio.mp3'
