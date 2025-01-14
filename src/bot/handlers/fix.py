from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

router = Router()

@router.message(Command("fix"))
async def fix_command(message: Message) -> None:
    """
    Fixes old keyboard inside bot ("Bot Commands" button)
    """

    await message.answer("<i>internal keyboard fix</i>", reply_markup=ReplyKeyboardRemove())