from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_days,get_time
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Запись')],
    [KeyboardButton(text='Информация о нас'),
     KeyboardButton(text='Наши награды')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...')
req_numb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Отправить номер телефона',
                request_contact=True
            )],

    ], resize_keyboard=True
)
async def days():
    keyboard=InlineKeyboardBuilder()
    days_name=await get_days()
    for day in days_name:
        keyboard.add(InlineKeyboardButton(text=f"{day}",callback_data=f"{day}"))
    keyboard.add(InlineKeyboardButton(text="На главную",callback_data="to_main"))
    return keyboard.as_markup()


from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime

async def time(day):
    keyboard = InlineKeyboardBuilder()
    all_time = await get_time(day)

    for clock in all_time:

        keyboard.add(InlineKeyboardButton(text=clock.split("_")[0], callback_data=f"{clock}"))

    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main"))
    return keyboard.as_markup()

pay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить',callback_data="paid")]])
