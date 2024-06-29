from dataclasses import dataclass
from datetime import datetime
from typing import Any

import aiohttp
import descriptions
from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import (
    CallbackQuery,
    InputMediaDocument,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from aiogram.types.input_file import BufferedInputFile
from config import config
from create_bot import bot

buy_project_router = Router()
html = ParseMode.HTML
REQUEST_URL = "http://kematin.space:9999/bot/"


@dataclass
class Project:
    id: str
    name: str
    summary: str
    price: int
    category: str
    have_presentation: bool
    have_product: bool
    have_unique: bool
    is_blocked: bool
    created_at: str


async def request_json(url: str) -> Any:
    headers = {"Authorization": f"Bearer {config.SECRET_KEY}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def request_file(project_id: str, type: str) -> bytes:
    headers = {"Authorization": f"Bearer {config.SECRET_KEY}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            REQUEST_URL + f"files/{project_id}?type={type}", headers=headers
        ) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise ValueError(
                    f"Failed to retrieve file. Status code: {response.status}"
                )


async def block_project(project_id: str):
    url = f"http://kematin.space:9999/bot/project/{project_id}?is_blocked=true"
    headers = {"Authorization": f"Bearer {config.SECRET_KEY}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers):
            pass


async def handle_buy_project(message: Message, project: Project):
    types = [
        ("doc", "document.docx"),
    ]
    if project.have_presentation:
        types.append(("pptx", "presentation.pptx"))
    if project.have_unique:
        types.append(("png", "unique.png"))
    if project.have_product:
        types.append(("product", "product.zip"))
    files = []
    for type_project, filename in types:
        try:
            file_bytes = await request_file(project.id, type_project)
            file = BufferedInputFile(file_bytes, filename=filename)
            file = InputMediaDocument(media=file)
            files.append(file)
        except ValueError:
            pass
    await bot.send_message(
        message.from_user.id, descriptions.BUY_PROJECT, parse_mode=html
    )
    await bot.send_media_group(
        chat_id=message.from_user.id,
        media=files,
    )
    await bot.send_message(
        config.ADMIN_IP,
        descriptions.get_project_description_for_admin(
            project, buy_time=datetime.now(), buyer=message.from_user.username
        ),
        parse_mode=html,
    )
    await block_project(project.id)


@buy_project_router.callback_query(lambda c: c.data.startswith("buy_project_"))
async def buy_project(callback_query: CallbackQuery):
    project_id = callback_query.data.split("_")[-1]
    project_data = await request_json(REQUEST_URL + f"projects/{project_id}")
    project = Project(**project_data["project"])
    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title=f"⭐ {project.name} ⭐",
        description=project.summary,
        payload=project.id,
        provider_token=config.PROVIDER_TOKEN,
        currency="rub",
        prices=[LabeledPrice(label="Проект", amount=project.price * 100)],
        max_tip_amount=100000,
        suggested_tip_amounts=[5000, 10000, 20000, 50000],
        provider_data=None,
        request_timeout=15,
    )


@buy_project_router.pre_checkout_query(lambda q: True)
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@buy_project_router.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        pmnt = message.successful_payment
        project_id = str(pmnt.invoice_payload)
        project_data = await request_json(REQUEST_URL + f"projects/{project_id}")
        project = Project(**project_data["project"])
        await handle_buy_project(message, project)
    except Exception as e:
        await bot.send_message(
            config.ADMIN_IP,
            descriptions.get_error_message(message.from_user.username, e),
        )
