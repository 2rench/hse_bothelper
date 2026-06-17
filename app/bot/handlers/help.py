from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(
    lambda c: c.data == "help"
)
async def change_group(
    callback: CallbackQuery,
):

    await callback.message.edit_text(
        "💬 Пишите, если что",
    )
