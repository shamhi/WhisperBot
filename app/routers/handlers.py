from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.dice_emoji import DiceEmoji
from app.states import TTS, STT, AudioTrack
from app.keyboards import inline_kbs as kb
from aiogram.types import Message, CallbackQuery, FSInputFile
from app.routers.functions import main_functions as fn


main_router = Router()


@main_router.callback_query(F.data.in_(kb.builder_kb_data))
async def builder_callback(call: CallbackQuery):
    await call.answer(call.data)


@main_router.callback_query(F.data == kb.tts_data, StateFilter(None))
async def tts_callback(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('*Отправьте текст, который хотите преобразовать в аудио\nДля отмены введите /cancel*',
                              parse_mode='markdownv2')
    await state.set_state(TTS.get_text)


@main_router.message(F.text.regexp(r'^[A-Za-zА-Яа-я0-9?!,. -]+$'), F.text.len() < 500, TTS.get_text)
async def get_tts_text(message: Message, state: FSMContext):
    lang_code = fn.detect_language(message.text)
    await state.update_data(tts_text=message.text)
    await state.update_data(lang=lang_code)
    await message.answer('*Выберите пол для озвучки*', reply_markup=kb.genders_kb, parse_mode='markdownv2')

    await state.set_state(TTS.get_gender)


@main_router.message(TTS.get_text)
async def check_tts_text(message: Message):
    await message.answer(f'*Ваш текст должен быть менее 500 символов и не содержать специальные символы*',
                         parse_mode='markdownv2')


@main_router.callback_query(F.data.in_(kb.all_genders), TTS.get_gender)
async def get_tts_gender(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(tts_gender=call.data)
    persons = await kb.get_persons_kb(state=state)
    await call.message.answer('*Выберите персонажа*', reply_markup=persons, parse_mode='markdownv2')

    await state.set_state(TTS.get_person)


@main_router.callback_query(F.data.in_(kb.all_persons), TTS.get_person)
async def get_tts_person(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(tts_person=call.data)
    data = await state.get_data()
    text = data.get('tts_text')
    audio = await fn.create_audio(data=data)

    if audio:
        await call.message.answer_audio(audio=audio, caption=text)
    else:
        await call.message.answer(text='Что-то пошло не так')

    await state.clear()


@main_router.callback_query(F.data == kb.stt_data, StateFilter(None))
async def stt_callback(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('*Отправьте аудио или видео, чтобы получить текст\nДля отмены введите /cancel*',
                              parse_mode='markdownv2')

    await state.set_state(STT.get_speech)


@main_router.message(F.audio | F.voice | F.video, STT.get_speech)
async def get_stt_speech(message: Message, state: FSMContext, bot: Bot):
    content_type = message.content_type.lower()
    duration = await fn.get_duration(message=message, content_type=content_type)

    if duration > 300:
        await message.answer('*Отправьте файл продолжительностью менее 5 мин\nДля отмены введите /cancel*',
                             parse_mode='markdownv2')
        return

    file_id = await fn.get_file_id(message=message, content_type=content_type)
    downloaded_file = await bot.download(file=file_id)

    file_bytes = await fn.get_file_bytes(downloaded_file=downloaded_file)
    text = await fn.get_stt(file_bytes=file_bytes)

    if text:
        msg = await bot.send_message(message.chat.id, text=text, reply_markup=kb.translate_stt_kb)
    else:
        text = 'Что-то пошло не так'
        msg = await bot.send_message(message.chat.id, text=text)

    await state.clear()

    await state.update_data(stt_msg_id=msg.message_id)
    await state.update_data(stt_msg_text=msg.text)


@main_router.message(STT.get_speech)
async def check_stt_speech(message: Message):
    await message.answer('*Ваш файл не содержит аудио, попробуйте снова\nДля отмены введите /cancel*',
                         parse_mode='markdownv2')


@main_router.callback_query(F.data == kb.translate_stt_data, StateFilter(None))
async def get_stt_language(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    text = state_data.get('stt_msg_text')
    msg_id = state_data.get('stt_msg_id')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id, text=text,
                                reply_markup=kb.choose_language_stt_kb)


@main_router.callback_query(F.data.in_(kb.stt_languages_data), StateFilter(None))
async def translate_stt_text(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    call_data = call.data
    text = state_data.get('stt_msg_text')
    msg_id = state_data.get('stt_msg_id')

    translated_text = fn.translate_text(text=text, data=call_data)
    if translated_text:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id, text=translated_text,
                                    reply_markup=kb.translate_stt_kb)
    else:
        callback_text = fn.check_stt_lang(text=text)
        await call.answer(text=callback_text)


@main_router.callback_query(F.data == kb.audio_track_data, StateFilter(None))
async def audiotrack_callback(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('*Отправьте видео файл для получения аудио дорожки\nДля отмены введите /cancel*',
                              parse_mode='markdownv2')

    await state.set_state(AudioTrack.get_video)


@main_router.message(F.video, AudioTrack.get_video)
async def get_video(message: Message, bot: Bot, state: FSMContext):
    duration = message.video.duration
    file_size = message.video.file_size // 1024 // 1024
    if duration > 1800 or file_size >= 20:
        await message.answer(
            '*Отправьте видео размером не более 20МБ и продолжительностью менее 30 мин\nДля отмены введите /cancel*',
            parse_mode='markdownv2')
        return

    file_id = message.video.file_id
    downloaded_file = await bot.download(file=file_id)

    audiotrack = await fn.get_audiotrack(downloaded_file=downloaded_file)
    await message.answer_audio(audio=FSInputFile(path=audiotrack, filename='audiotrack.mp3'))

    await state.clear()


@main_router.message(AudioTrack.get_video)
async def check_get_vide(message: Message):
    await message.answer('*Вы отправили не видео, попробуйте снова\nДля отмены введите /cancel*',
                         parse_mode='markdownv2')


@main_router.message()
async def end(message: Message):
    from random import choice

    dice_list = [DiceEmoji.DICE, DiceEmoji.SLOT_MACHINE, DiceEmoji.DART, DiceEmoji.BOWLING, DiceEmoji.FOOTBALL,
                 DiceEmoji.BASKETBALL]
    await message.answer_dice(emoji=choice(dice_list))
