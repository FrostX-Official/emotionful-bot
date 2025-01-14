from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

router = Router()

@router.message(Command("fix"))
async def fix_command(message: Message) -> None:
    """
    Used to fix old keyboard inside bot ("Bot Commands" button)
    """

    await message.answer("Fixing...", reply_markup=ReplyKeyboardRemove())