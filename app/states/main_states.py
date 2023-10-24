from aiogram.fsm.state import StatesGroup, State

class TTS(StatesGroup):
    get_text = State()
    get_gender = State()
    get_person = State()


class STT(StatesGroup):
    get_speech = State()


class AudioTrack(StatesGroup):
    get_video = State()
