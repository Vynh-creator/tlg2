from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import app.keyboads as kb
import logging
from aiogram.fsm.state import StatesGroup,State
logging.basicConfig(level=logging.INFO)
from  dateutil import parser
from app.database.requests import registration
class Reg(StatesGroup):
    phone=State()
    first_name_p=State()
    last_name_p = State()
    first_name_ch=State()
    last_name_ch = State()
    day_name=State()
    time=State()
    tg_id=State()
    pai=State()
    chat_user_id=State()
router = Router()
# router.message.middleware(TestMiddleWare())




# class Reg(StatesGroup):
#   name = State()
#  number = State()

async def send_start_message(message: Message):
    await message.answer(
        "Добро пожаловать к нам в телеграмм бот!\n Мы компания Робот и я если вы хотите вы можете записаться к нам на занятия",
        reply_markup=kb.main)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await send_start_message(message)


@router.callback_query(F.data == 'to_main')
async def to_main(callback: CallbackQuery):
    await callback.answer()
    await send_start_message(callback.message)


@router.message(F.text == "Информация о нас")
async def inf_about_club(message: Message):
    await message.answer("Здесь вы можете посмотреть все о нашем клубе")


@router.message(F.text == "Наши награды")
async def rewards(message: Message):
    await message.answer("У нас есть много серьезных наград")

@router.message(F.text == "Запись")
async def write_on(message: Message,state:FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(chat_user_id=message.chat.id)
    await state.set_state(Reg.day_name)
    await message.answer("Выберите день записи",reply_markup=await kb.days())

@router.callback_query(Reg.day_name)
async def choose_time(callback: types.CallbackQuery,state:FSMContext):
    logging.info(f"Выбран день: {callback.data}")
    await state.update_data(day_name=callback.data)
    await state.set_state(Reg.time)
    await callback.message.answer("Выберите время", reply_markup=await kb.time(callback.data))

@router.callback_query(Reg.time)
async def paiment(callback: types.CallbackQuery,state:FSMContext):
    logging.info(f"Выбрано время: {callback.data.split("_")[0]}")
    await state.update_data(time=callback.data)
    await state.set_state(Reg.pai)
    await callback.message.answer("оплатите",reply_markup=kb.pay)

@router.callback_query(Reg.pai)
async def choose_last_name_p(callback: types.CallbackQuery,state:FSMContext):
    logging.info(f"оплачено")
    await state.set_state(Reg.phone)
    await callback.message.answer("Введите номер телефона")

@router.message(Reg.phone)
async def choose_phone(message:Message,state:FSMContext):
    logging.info(f"введен номер телефона {message.text}")
    await state.update_data(phone=message.text)
    await state.set_state(Reg.first_name_p)
    await message.answer("Напишите ваше имя")

@router.message(Reg.first_name_p)
async def choose_last_name_p(message:Message,state:FSMContext):
    logging.info(f"Имя родителя: {message.text}")
    await state.update_data(first_name_p=message.text)
    await state.set_state(Reg.last_name_p)
    await message.answer("Напишите вашу фамилию")

@router.message(Reg.last_name_p)
async def choose_first_name_ch(message:Message,state:FSMContext):
    logging.info(f"Фамилия родителя{message.text}")
    await state.update_data(last_name_p=message.text)
    await state.set_state(Reg.first_name_ch)
    await message.answer("Напишите имя ребенка не волнуйтесь если у вас несколько детей то их можно будет добавить позже")

@router.message(Reg.first_name_ch)
async def choose_last_name_ch(message:Message,state:FSMContext):
    logging.info(f"Имя ребенка{message.text}")
    await state.update_data(first_name_ch=message.text)
    await state.set_state(Reg.last_name_ch)
    await message.answer("Введите фамилию ребенка")

@router.message(Reg.last_name_ch)
async def end_reg(message:Message,state:FSMContext):
    logging.info(f"Фамилия ребенка {message.text}")
    await state.update_data(last_name_ch=message.text)
    data = await state.get_data()
    await registration(data['tg_id'],data['first_name_p'],data['last_name_p'],data['phone'],data['chat_user_id'],data['first_name_ch'],data['last_name_ch'],data['day_name'],data['time'])



# @router.message(Command("reg"))
# async def reg1(message: Message, state: FSMContext):
#   await state.set_state(Reg.name)
#  await message.answer("Введите ваше имя")

# @router.message(Reg.name)
# async def reg_two(message: Message, state: FSMContext):
#   await state.update_data(name=message.text)
#  await state.set_state(Reg.number)
#  await message.reply("Введите номер", reply_markup=kb.req_numb)

# @router.message(Reg.number, F.contact)
# async def reg3(message: types.Message, state: FSMContext):
#   await state.update_data(number=message.contact.phone_number)
#  data = await state.get_data()
# await message.answer(f"Спасибо, регистрация завершена Имя: {data['name']}, Номер: {data['number']}")
# await state.clear()
# await message.answer("Регистрация завершена.", reply_markup=types.ReplyKeyboardRemove())

# @router.message(F.text == 'Каталог')
# async def catalog(message: Message):
#   await message.answer("Выберите категорию товара", reply_markup=await kb.categories())


# @router.callback_query(F.data.startswith("category_"))
# async def category(callback: CallbackQuery):
#   await callback.answer("Вы выбрали категорию")
#  await callback.message.answer("Выберите товар по категории",
#            reply_markup=await kb.items(callback.data.split("_")[1]))


# @router.callback_query(F.data.startswith("item_"))
# sync def category(callback: CallbackQuery):
#   item_data = await rq.get_item_inf(callback.data.split("_")[1])
#  await callback.answer("Вы выбрали товар")
# await callback.message.answer(
#    f"Название: {item_data.name},\n Описание: {item_data.description},\n цена: {item_data.price}$",
#   reply_markup=await kb.items(callback.data.split("_")[1]))
