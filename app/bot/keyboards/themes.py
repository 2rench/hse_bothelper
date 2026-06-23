from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_themes_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨ Стандарт",
                    callback_data="theme_default",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💃 Для girls",
                    callback_data="themes_girls",
                ),
                InlineKeyboardButton(
                    text="🕺 Для менов",
                    callback_data="themes_boys",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Языки",
                    callback_data="themes_languages",
                )
            ],
        ]
    )
def get_girls_themes_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Люкс girl",
                    callback_data="theme_luxury",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💅 Нишевая girl",
                    callback_data="theme_clean_girl",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="themes",
                )
            ]
        ]
    )
def get_boys_themes_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🖤 Брат(макан) стиль",
                    callback_data="theme_brother",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💻 Для айтишников",
                    callback_data="theme_it_style",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="themes",
                )
            ]
        ]
    )
def get_languages_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇬🇧 English",
                    callback_data="theme_english",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇳 中文",
                    callback_data="theme_chinese",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇫🇷 Français",
                    callback_data="theme_french",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="themes",
                )
            ]
        ]
    )
