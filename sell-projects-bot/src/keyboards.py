from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def buy_project_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌍 Все 🌍", callback_data="all_project"),
            ],
            [
                InlineKeyboardButton(text="📗 Full 11", callback_data="full11_project"),
                InlineKeyboardButton(text="Full 9", callback_data="full9_project"),
                InlineKeyboardButton(text="Min 📗", callback_data="min_project"),
            ],
            [
                InlineKeyboardButton(
                    text="⭐ Exclusive ⭐", callback_data="exclusive_project"
                ),
            ],
            [
                InlineKeyboardButton(text="⬅ Вернуться", callback_data="start"),
            ],
        ]
    )

    return keyboard


def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="💵 Товары 💵", callback_data="get_all_projects"),
        ],
        [
            InlineKeyboardButton(text="🌠 О нас", callback_data="about"),
            InlineKeyboardButton(text="Отзывы 🧑‍💻", callback_data="feedback"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def interactive_keyboard(
    index: int, project_id: int, project_size: int, category: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="💸 Купить 💸", callback_data=f"buy_project_{project_id}"
        ),
        width=1,
    )
    second_row_buttons = list()
    if index > 0:
        second_row_buttons.append(
            InlineKeyboardButton(text="️⬅⬅⬅", callback_data=f"prev_project_{category}")
        )

    if index < project_size - 1:
        second_row_buttons.append(
            InlineKeyboardButton(text="️➡➡➡", callback_data=f"next_project_{category}")
        )

    keyboard.row(*second_row_buttons, width=2)
    keyboard.row(
        InlineKeyboardButton(text="⬅ Вернуться", callback_data="get_all_projects"),
        width=1,
    )
    return keyboard.as_markup()


def return_to_start() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="⬅ Вернуться в начало", callback_data="start"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
