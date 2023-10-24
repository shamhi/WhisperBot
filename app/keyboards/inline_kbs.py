from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


builder_kb = InlineKeyboardBuilder()
for i in range(1, 17):
    builder_kb.add(InlineKeyboardButton(text=str(i), callback_data=f'build{str(i)}'))
builder_kb.adjust(4)

builder_kb_data = [f'build{str(i)}' for i in range(1, 17)]

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Текст в Аудио", callback_data='tts'),
        InlineKeyboardButton(text="Аудио в Текст", callback_data='stt')
    ],
    [
        InlineKeyboardButton(text="Аудиодорожка из видео", callback_data='audio_track')
    ]
])


choosing_game_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сапёр', callback_data='game_sapper')],
    [InlineKeyboardButton(text='Казино', callback_data='game_casino')]
])

choosing_sapper_data = 'game_sapper'
choosing_casino_data = 'game_casino'


translate_stt_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перевести', callback_data='translate_stt')]
])

choose_language_stt_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Ru🇷🇺', callback_data='stt_ru'),
        InlineKeyboardButton(text='En🇬🇧', callback_data='stt_en')
    ],
    [
        InlineKeyboardButton(text='Es🇪🇸', callback_data='stt_es'),
        InlineKeyboardButton(text='Fr🇫🇷', callback_data='stt_fr')
    ],
    [
        InlineKeyboardButton(text='De🇩🇪', callback_data='stt_de'),
        InlineKeyboardButton(text='Cn🇨🇳', callback_data='stt_cn')
    ]
])


genders_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='MALE', callback_data='male'),
        InlineKeyboardButton(text='FEMALE', callback_data='female')
    ]
])

en_male_persons_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Kevin', callback_data='Kevin'),
        InlineKeyboardButton(text='Justin', callback_data='Justin')
    ]
])

ru_male_persons_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Sasha', callback_data='Sasha'),
        InlineKeyboardButton(text='Maxim', callback_data='Maxim')
    ]
])

en_female_persons_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Emma', callback_data='Emma'),
        InlineKeyboardButton(text='Joanna', callback_data='Joanna')
    ]
])

ru_female_persons_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Elena', callback_data='Elena'),
        InlineKeyboardButton(text='Tatyana', callback_data='Tatyana')
    ]
])


async def get_persons_kb(state):
    data = await state.get_data()
    lang = data.get('lang')
    gender = data.get('tts_gender')
    try:
        persons_kb = {
            ('en', 'male'): en_male_persons_kb,
            ('en', 'female'): en_female_persons_kb,
            ('ru', 'male'): ru_male_persons_kb,
            ('ru', 'female'): ru_female_persons_kb
        }

        return persons_kb[(lang, gender)]
    except KeyError:
        persons_kb = {
            'male': ru_male_persons_kb,
            'female': ru_female_persons_kb
        }

        await state.update_data(lang='ru')

        return persons_kb[gender]


all_genders = ['male', 'female']
all_persons = ['Kevin', 'Justin', 'Sasha', 'Maxim', 'Emma', 'Joanna', 'Elena', 'Tatyana']

tts_data = 'tts'
stt_data = 'stt'
audio_track_data = 'audio_track'
translate_stt_data = 'translate_stt'
stt_languages_data = ['stt_ru', 'stt_en', 'stt_es', 'stt_fr', 'stt_de', 'stt_cn']
