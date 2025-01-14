import logging

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from aiogram.utils.i18n import gettext as _

from db import *

router = Router()

TELEGRAM_STARS = "XTR"

async def get_donate_data(user: User) -> tuple[str, InlineKeyboardMarkup]:
    """Generates donation selection `text` and `reply_markup` based on `user` data.

    Args:
        user (User): User in Database

    Returns:
        tuple[str, InlineKeyboardMarkup]: `text` and `reply_markup` to use in `message.answer` or `query.message.answer`
    """

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ 1", callback_data="donation_1")],
        [InlineKeyboardButton(text="⭐ 49", callback_data="donation_49")],
        [InlineKeyboardButton(text="⭐ 249", callback_data="donation_149")],
        [InlineKeyboardButton(text="⭐ 499", callback_data="donation_499")],
    ])

    total_stars_donated = user.stars
    if total_stars_donated == 0:
        return _("<b>💘 Donation</b>\n") + _("💔 You haven't donated stars yet."), keyboard
    return _("<b>💘 Donation</b>\n") + _("💗 You've donated {amount} star so far! &lt;3", "💗 You've donated {amount} stars so far! &lt;3", total_stars_donated).format(amount=total_stars_donated), keyboard

@router.message(Command("donate"))
async def donate_command_handler(message: Message, user: User) -> None:
    logging.warn(f"@{message.from_user.username} used /donate command.")

    text, reply_markup = await get_donate_data(user)
    await message.answer(
        text=text,
        reply_markup=reply_markup
    )

@router.callback_query(F.data == "donate")
async def donate_query_handler(query: CallbackQuery, user: User) -> None:
    logging.warn(f"@{query.from_user.username} used donate query.")

    text, reply_markup = await get_donate_data(user)
    await query.message.answer(
        text=text,
        reply_markup=reply_markup
    )

@router.callback_query(F.data.startswith("donation"))
async def donation_callback(query: CallbackQuery) -> None:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("💳 Pay"), pay=True)],
        [InlineKeyboardButton(text=_("🔙 Back"), callback_data="donate")]
    ])

    amount = query.data.split("_")[1]
    await query.message.answer_invoice(
        title=_("💘 Donation") + f" (⭐ {amount})",
        description=_("Donate to Emotionful Bot!"),
        payload="donation_"+str(amount),
        currency=TELEGRAM_STARS,
        prices=[
            LabeledPrice(label=TELEGRAM_STARS, amount=amount),
        ],
        reply_markup=keyboard
    )

@router.pre_checkout_query()
async def donate_checkout_handler(event: PreCheckoutQuery) -> None:
    await event.answer(ok = True)

@router.message(F.successful_payment)
async def successful_donation(message: Message, user: User, bot: Bot) -> None:
    await bot.refund_star_payment(
        user_id = message.from_user.id,
        telegram_payment_charge_id = message.successful_payment.telegram_payment_charge_id,
    )

    amount = message.successful_payment.total_amount
    logging.warn(f"@{message.from_user.username} donated {amount} star(s)!")

    total_stars_donated = user.stars+amount
    await User.update_or_create(
        id = message.from_user.id,
        username = message.from_user.username,
        stars = user.stars,
        defaults = {
            "username": message.from_user.username,
            "stars": total_stars_donated
        }
    )
    await message.answer(
        _("💘 Successfully donated {amount} star!", "💘 Successfully donated {amount} stars!", amount).format(amount=amount) + "\n" +
        _("💗 You've donated {amount} star so far! &lt;3", "💗 You've donated {amount} stars so far! &lt;3", total_stars_donated).format(amount=total_stars_donated)
    )