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
                    callback_data="themes_default",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👩 Для девушек",
                    callback_data="themes_girls",
                ),
                InlineKeyboardButton(
                    text="👨 Для парней",
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
                    callback_data="theme_lux",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Clean girl",
                    callback_data="theme_clean",
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
                    text="🖤 Брат стиль",
                    callback_data="theme_brat",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💻 IT стиль",
                    callback_data="theme_it",
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
                    callback_data="theme_en",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇳 中文",
                    callback_data="theme_cn",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇫🇷 Français",
                    callback_data="theme_fr",
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
