from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import FSInputFile

import descriptions
import keyboards
from create_bot import bot

main_router = Router()
html = ParseMode.HTML


@main_router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        descriptions.START, reply_markup=keyboards.start_keyboard(), parse_mode=html
    )


@main_router.callback_query(lambda c: c.data == "start")
async def start_callback(callback_query: CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        descriptions.START,
        reply_markup=keyboards.start_keyboard(),
        parse_mode=html,
    )


@main_router.message(Command("about"))
async def about_command(message: Message) -> None:
    img_url = "./static/price_list.jpeg"
    input_photo = FSInputFile(img_url)
    await bot.send_photo(
        message.from_user.id,
        photo=input_photo,
        caption=descriptions.ABOUT,
        reply_markup=keyboards.return_to_start(),
        parse_mode=html,
    )


@main_router.callback_query(lambda c: c.data == "about")
async def about_callback(callback_query: CallbackQuery):
    img_url = "./static/price_list.jpeg"
    input_photo = FSInputFile(img_url)
    await bot.send_photo(
        callback_query.from_user.id,
        photo=input_photo,
        caption=descriptions.ABOUT,
        reply_markup=keyboards.return_to_start(),
        parse_mode=html,
    )


@main_router.message(Command("feedback"))
async def feedback_command(message: Message) -> None:
    await message.answer(
        descriptions.FEEDBACK, reply_markup=keyboards.return_to_start(), parse_mode=html
    )


@main_router.callback_query(lambda c: c.data == "feedback")
async def feedback_callback(callback_query: CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        descriptions.FEEDBACK,
        reply_markup=keyboards.return_to_start(),
        parse_mode=html,
    )
