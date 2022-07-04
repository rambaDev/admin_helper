import logging
#import telebot
import time
from time import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
import asyncio
from contextlib import suppress

from aiogram.utils.exceptions import (
    MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound)

import config as cfg
import markups as nav
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.tg_bot_token)
dp = Dispatcher(bot)
db = Database('database.db')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


def check_sub_channel(chat_member):
    return chat_member['status'] != "left"


@dp.message_handler(commands=['mute'], commands_prefix="/")
async def mute(message: types.Message):
    if str(message.from_user.id) == cfg.ADMIN_ID:
        if not message.reply_to_message:
            await message.reply("mute выдается в ответ на сообщение!")
            return

        mute_sec = int(message.text[6:])
        db.add_mute(message.reply_to_message.from_user.id, mute_sec)
        await message.bot.delete_message(cfg.CHAT_ID, message.message_id)
        await message.reply_to_message.reply(f"Занят горловым миньетом на {mute_sec} минут!")


@dp.message_handler(commands=['мут'])
def mute(message: types.Message):
    print(message.reply_to_message.from_user.id)
    bot.restrict_chat_member(
        message.chat.id, message.reply_to_message.from_user.id, until_date=time.time() + 120)
    bot.send_message(message.chat.id, 'Администратор кинул вас в мут на 2м',
                     reply_to_message_id=message.message_id)


@dp.message_handler(content_types=["new_chat_members"])
async def user_joined(message: types.Message):
    new_mem = await message.answer("Привет!\nтолько для подписчиков канала @OmArtVall", reply_markup=nav.channelMenu)
    asyncio.create_task(delete_message(new_mem, 5))
    await message.delete()


@dp.message_handler()
async def mess_handler(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)

    if check_sub_channel(await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)):
        text = message.text.lower()
        for word in cfg.WORLDS:
            if word in text:
                await message.delete()
    else:
        msg = await message.answer("ТОЛЬКО ДЛЯ ПОДПИСЧИКОВ КАНАЛА!!!\n\nЕсть 3 секунды сделать это\n\n @OmArtVall", reply_markup=nav.channelMenu)
        asyncio.create_task(delete_message(msg, 3))
        await message.delete()


@dp.message_handler(content_types=["left_chat_member"])
async def start_commandr(message: types.Message):
    await message.answer("Ливнул, сучара...\n🤷‍♀️Чё приходил этот говноед...🤷🏻‍♂️")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# , on_startup=on_startup
# async def on_startup(_):
#     print(' @zrknbot=>TOKEN:5154856916:AAHhqjpbsoufPpYLq3_vXCGfhwjJN368jiE\nБот готов к работе...')

# @dp.message_handler(commands=['id'], commands_prefix="/")
# async def get_id(message: types.Message):
#     await bot.send_message(message.from_id, f"ID: {message.from_user.id}")
