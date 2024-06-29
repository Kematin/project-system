from dataclasses import dataclass

from config import config


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


ABOUT = (
    "Предоставляем полностью готовые индивидуальные проекты 9-11 класс"
    + "\n\n✅ Все регионы"
    + "\n✅ Индивидуальность 90+"
    + "\n✅ Безопасное оформление "
    + "\n\n<b>НАЛИЧИЕ:</b>"
    + "\n\n<i>FULL 11 PROJECT  - <b>1999 ₽</b></i>"
    + "\n————————————————"
    + "\n<i>FULL 9 PROJECT  - <b>999 ₽</b></i>"
    + "\n————————————————"
    + "\n<i>MINIMUM  - <b>299 ₽</b></i>"
    + "\n————————————————"
    + "\n<i>EXCLUSIVE - <b>2999 ₽</b></i>"
    + "\n————————————————"
    + "\n\n*<b><i>По всем вопросам: @LamberJacks</i></b>"
    + '\n*<b><i>Разработкой занимался: <a href="https://github.com/Kematin">Kematin</a></i></b>'
)
START = (
    "🌜 Функционал бота 🌛"
    + "\n\nПокупка готового проекта\n<b>| Товары |</b>"
    + "\n\nПодробная информация о нас\n<b>| О нас |</b>"
    + "\n\nПосмотреть отзывы покупателей\n<b>| Отзывы |</b>"
)
FEEDBACK = (
    "Если хотите ознакомиться с отзывами других покупателей, переходите в:\n<b><u>https://t.me/sell_project_shop_feedback</u></b>"
    + "\n\nВы так-же можете оставить свой отзыв после покупки товара."
    + "\n\n*<i>Отзывы добавляются в канал после проверки модерации</i>"
)

BUY_PROJECTS = (
    "<b>Список предлагаемых товаров</b>"
    + "\n\n<i><u>FULL 11 PROJECT:</u></i>"
    + "\n✓ <i>Проект document.docx</i>"
    + "\n✓ <i>Презентация presentation.pptx</i>"
    + "\n✓ <i>Продукт product.png (флаер, буклет) </i>"
    + "\n✓ <i>Уникальность</i>"
    + "\n\n<i><u>FULL 9 PROJECT:</u></i>"
    + "\n✓ <i>Проект document.docx</i>"
    + "\n✓ <i>Презентация presentation.pptx</i>"
    + "\n✓ <i>Уникальность</i>"
    + "\n\n<i><u>MINIMUM:</u></i>"
    + "\n✓ <i>Проект document.docx</i>"
    + "\n× <i>Презентация presentation.pptx</i>"
    + "\n× <i>Продукт product.png (флаер, буклет) </i>"
    + "\n× <i>Уникальность</i>"
    + "\n\n<i><u>EXCLUSIVE:</u></i>"
    + "\n✓ <i>Проект document.docx</i>"
    + "\n✓ <i>Презентация presentation.pptx</i>"
    + "\n✓ <i>Продукт product.png (флаер, буклет) </i>"
    + "\n✓ <i>Уникальность</i>"
    + "\n✓ <i>Университетский уровень</i>"
    + "\n\n*<i>Цены могут меняться в зависимости от сложности проекта</i>"
)
BUY_PROJECT = (
    "Спасибо за покупку нашего товара!"
    + "\n\nЕсли захотите оставить отзыв о купленном проекте, напишите нашему менеджеру: <b><i>@LamberJacks</i></b>"
    + "\n\nУдачного дня 😊"
)


def get_project_description(project: Project) -> str:
    have = {1: "✔️", 0: "✖️"}

    desc = (
        "<b>Информация о товаре</b>"
        + f"\n\n<u>Название:</u>\n{project.name}"
        + f"\n\n<u>Краткое содержание:</u>\n{project.summary}"
        + f"\n\n<u>Цена: <b>{project.price} ₽</b></u>"
        + f"\n<u>Категория:</u> {config.CATEGORIES[project.category]}"
        + f"\n\n<u>Презентация:</u> {have[project.have_presentation]}"
        + f"\n<u>Продукт:</u> {have[project.have_product]}"
        + f"\n<u>Уникальность:</u> {have[project.have_unique]}"
    )
    return desc


def get_project_description_for_admin(
    project: Project, buy_time: str, buyer: str
) -> str:
    project_desc = get_project_description(project)
    return (
        f"Был куплен проект с ID:\n{project.id}"
        + f"\n\n{project_desc}"
        + f"\n\nБыл куплен:\n{buy_time}"
        + f"\n\nПокупатель:\n{buyer}"
    )


def get_error_message(buyer: str, e: Exception) -> str:
    desc = "ОШИБКА ПРИ ПОКУПКЕ ТОВАРА" + f"\n\nBUYER USER: {buyer}" + f"ERROR: {e}"
    return desc
