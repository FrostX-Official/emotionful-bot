import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.i18n import gettext as _

router = Router()

@router.callback_query(F.data=="manage_packs")
async def manage_packs(query: CallbackQuery):
    logging.warn(f"@{query.from_user.username} used packs callback button.")

    await query.message.edit_text(_("📁 Packs\n" \
                                  "<i>(you have none)</i>"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=_("🔙 Back"), callback_data="start")]]
        )
    )

@router.callback_query(F.data=="new_pack")
async def new_pack(query: CallbackQuery):
    logging.warn(f"@{query.from_user.username} used new pack callback button.")

    await query.message.edit_text(_("😼 Currently in development."),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=_("🔙 Back"), callback_data="start")]]
        )
    )

@router.callback_query(F.data=="quickdelete")
async def quickdelete(query: CallbackQuery):
    logging.warn(f"@{query.from_user.username} used quickdelete callback button.")

    await query.message.edit_text(_("😼 Currently in development."),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=_("🔙 Back"), callback_data="start")]]
        )
    )