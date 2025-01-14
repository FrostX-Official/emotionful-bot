import logging

from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from aiogram.utils.i18n import gettext as _

from db import *

router = Router()

TELEGRAM_STARS = "XTR"

@router.message(Command("donate"))
async def donate_command_handler(message: Message) -> None:
    logging.warn(f"@{message.from_user.username} used /donate command.")

    await message.answer_invoice(
        title="Donation",
        description="Donate to Emotionful Bot",
        payload="donation",
        currency=TELEGRAM_STARS,
        prices=[
            LabeledPrice(label=TELEGRAM_STARS, amount=199),
        ]
    )

@router.pre_checkout_query()
async def donate_checkout_handler(event: PreCheckoutQuery) -> None:
    await event.answer(True)

@router.message(F.successful_payment.payload == "donation")
async def successful_donation(message: Message, user: User) -> None:
    logging.warn(f"@{message.from_user.username} donated {message.successful_payment.total_amount} star(s)!")

    await message.answer(_("Successfully donated {amount} star(s)!").format(amount=message.successful_payment.total_amount))