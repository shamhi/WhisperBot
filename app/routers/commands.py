from aiogram import Router, html
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.fsm.context import FSMContext
from app.keyboards import inline_kbs as kb
from app.routers.functions import cmd_functions as fn
from app.db.postgres.storage import PostgresConnection
import structlog
import asyncpg


cmd_router = Router()


@cmd_router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, db_pool: asyncpg.Pool, db_logger: structlog.typing.FilteringBoundLogger):
    db = PostgresConnection(connection_poll=db_pool, logger=db_logger)

    user_id = message.from_user.id
    user_name = message.from_user.username

    await db.register_user(user_id=user_id, name=user_name)

    if message.from_user is None:
        return

    text = f'<b>Добро пожаловать,</b> <a href="tg://user?id={user_id}">{html.quote(message.from_user.full_name)}</a>\n\n' \
           f'🔊Я чат-бот, который работает с аудио и видео! 🎵\n\n' \
           f'Нажми, чтобы выбрать действие'
    await message.answer(text, reply_markup=kb.start_kb, parse_mode='HTML')
    print(message.contact)

@cmd_router.message(Command('help'), StateFilter(None))
async def cmd_help(message: Message):
    text = f'<b>Если у вас возникли какие-то вопросы или вы нашли баг в боте, напишите <a href="tg://user?id=1282629807">ему</a>.</b>\n\n' \
           f'<b>Вот что я могу</>'

    await message.answer(text, reply_markup=kb.start_kb, parse_mode='HTML')


@cmd_router.message(Command('stat'), StateFilter(None))
async def cmd_stat(message: Message):
    stat = fn.get_stat()
    await message.answer(stat, parse_mode='HTML')


@cmd_router.message(Command('game'), StateFilter(None))
async def cmd_game(message: Message):
    # from random import choice
    #
    # dice_list = [DiceEmoji.DICE, DiceEmoji.SLOT_MACHINE, DiceEmoji.DART, DiceEmoji.BOWLING, DiceEmoji.FOOTBALL,
    #              DiceEmoji.BASKETBALL]
    # await message.answer_dice(emoji=choice(dice_list))

    await message.answer('Выберите игру', reply_markup=kb.choosing_game_kb)


@cmd_router.message(Command('cancel'))
async def cancel_states(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('*Все состояния отменены*', parse_mode='markdown')
    text = f'<b>Добро пожаловать,</b> <a href="tg://user?id={message.from_user.id}">{html.quote(message.from_user.full_name)}</a>\n\n' \
           f'🔊Я чат-бот, который работает с аудио и видео! 🎵\n\n' \
           f'Нажми, чтобы выбрать действие'
    await message.answer(text, reply_markup=kb.start_kb, parse_mode='HTML')


@cmd_router.message(Command('shamhi'))
async def get_users_data(message: Message, db_pool: asyncpg.Pool, db_logger: structlog.typing.FilteringBoundLogger):
    db = PostgresConnection(connection_poll=db_pool, logger=db_logger)

    data_list = await db.get_users_columns()
    text = '\n\n'.join(['\n'.join([f'`{k}` *\\=\\=\\=* `{v}`' for k, v in data.items()]) for data in data_list])
    await message.answer(text=text, parse_mode='markdownv2')
