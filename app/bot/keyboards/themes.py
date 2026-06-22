from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_themes_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="😎 Стандарт",
                    callback_data="theme_default"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎀 Нишевая girl",
                    callback_data="theme_girl"
                ),
                InlineKeyboardButton(
                    text="💎 Люкс girl",
                    callback_data="theme_lux"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✨ Clean girl",
                    callback_data="theme_clean"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🖤 Брат стиль",
                    callback_data="theme_brat"
                ),
                InlineKeyboardButton(
                    text="💻 IT стиль",
                    callback_data="theme_it"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🇬🇧 English",
                    callback_data="theme_en"
                ),
                InlineKeyboardButton(
                    text="🇨🇳 中文",
                    callback_data="theme_cn"
                ),
                InlineKeyboardButton(
                    text="🇫🇷 Français",
                    callback_data="theme_fr"
                )
            ]

        ]
    )
