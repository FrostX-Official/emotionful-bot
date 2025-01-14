import logging

from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from aiogram.utils.i18n import gettext as _

from ..utils.random_heart import random_heart, random_heart_with_exclusion

from db import *

router = Router()

async def get_start_menu_content(event: Message | CallbackQuery):
    heart1 = await random_heart()
    heart2 = await random_heart_with_exclusion([heart1])
    heart3 = await random_heart_with_exclusion([heart1, heart2])

    name = html.bold(event.from_user.full_name.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace('\'','&apos;'))

    return (
        _(
            "{heart1} Hi, <b>{name}</b> !\n" \
            "{heart2} To start managing your stickers and emojis please use inline reply keyboard below.\n" \
            "{heart3} Use the /help command to understand how to upload your images and videos into UGC packs.\n" \
            "💸 Use the /donate command to support the bot.\n" \
            "⚠ Report any issues to @frostxoff !"
        ).format(
            heart1=heart1,
            heart2=heart2,
            heart3=heart3,
            name=name
        ), InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=_("📁 Manage your packs"), callback_data="manage_packs")],
            [InlineKeyboardButton(text=_("🌠 New Pack"), callback_data="new_pack")],
            [InlineKeyboardButton(text=_("❌ Quickly Delete Asset"), callback_data="quickdelete")]
        ])
    )
    
@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    logging.warn(f"@{message.from_user.username} used /start command.")

    text, reply_markup = await get_start_menu_content(message)
    await message.answer(text, reply_markup=reply_markup)

@router.callback_query(F.data=="start")
async def start_callback_handler(query: CallbackQuery):
    logging.warn(f"@{query.from_user.username} used /start query.")

    text, reply_markup = await get_start_menu_content(query)
    await query.message.edit_text(text, reply_markup=reply_markup)