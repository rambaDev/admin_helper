from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg

btnUrlChannel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=cfg.CANNEL_URL)
channelMenu = InlineKeyboardMarkup(row_width=1)
channelMenu.insert(btnUrlChannel)
