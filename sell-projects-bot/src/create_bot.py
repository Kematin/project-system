from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiohttp import web
from config import config

bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

webhook_path = "/webhook"
app = web.Application()
