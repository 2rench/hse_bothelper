from pathlib import Path

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

from config import ADMINS

from app.admin.admin_states import (
    BroadcastState,
)

from app.admin.admin_keyboards import (
    admin_keyboard,
    confirm_keyboard,
)

from app.admin.broadcast_service import (
    send_broadcast,
)

router = Router()


@router.message(F.text == "/admin")
async def admin_panel(
    message: Message,
):

    if message.from_user.id not in ADMINS:
        return

    await message.answer(
        "⚙️ Панель администратора",
        reply_markup=admin_keyboard()
    )


@router.callback_query(
    F.data == "create_broadcast"
)
async def create_broadcast(
    callback: CallbackQuery,
    state: FSMContext,
):

    await callback.message.answer(
        "📢 Отправьте текст или фото с подписью"
    )

    await state.set_state(
        BroadcastState.waiting_content
    )


@router.message(
    BroadcastState.waiting_content
)
async def get_content(
    message: Message,
    state: FSMContext,
):

    image_path = None

    text = (
        message.caption
        or message.text
        or ""
    )

    if message.photo:

        Path(
            "files/broadcasts"
        ).mkdir(
            exist_ok=True,
            parents=True
        )

        photo = message.photo[-1]

        file = await message.bot.get_file(
            photo.file_id
        )

        image_path = (
            f"files/broadcasts/"
            f"{photo.file_id}.jpg"
        )

        await message.bot.download_file(
            file.file_path,
            destination=image_path
        )

    await state.update_data(
        text=text,
        image_path=image_path,
    )

    await message.answer(
        "Отправить всем?",
        reply_markup=confirm_keyboard()
    )

    await state.set_state(
        BroadcastState.waiting_confirm
    )


@router.callback_query(
    BroadcastState.waiting_confirm,
    F.data == "broadcast_yes"
)
async def confirm_send(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()

    await callback.message.answer(
        "🚀 Начинаю рассылку..."
    )

    success, failed = await send_broadcast(
        bot=callback.bot,
        text=data.get("text"),
        image_path=data.get("image_path"),
    )

    await callback.message.answer(
        f"✅ Рассылка завершена\n\n"
        f"Успешно: {success}\n"
        f"Ошибок: {failed}"
    )

    await state.clear()


@router.callback_query(
    BroadcastState.waiting_confirm,
    F.data == "broadcast_no"
)
async def cancel_send(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()

    image_path = data.get(
        "image_path"
    )

    if image_path:

        Path(
            image_path
        ).unlink(
            missing_ok=True
        )

    await state.clear()

    await callback.message.answer(
        "❌ Рассылка отменена"
    )
