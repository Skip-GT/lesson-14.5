from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from crud_functions import initiate_db, init_db, get_all_products, add_user, is_included


initiate_db()
init_db()

products = get_all_products()


api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = 'Расчитать') ],
        [
            KeyboardButton(text = 'Информация') ],
        [
            KeyboardButton(text = 'Купить') ],
        [
            KeyboardButton(text='Регистрация')
        ]
    ], resize_keyboard = True
)


in_kb = InlineKeyboardMarkup()
button_calories = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
button_formulas = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
in_kb.add(button_calories, button_formulas)


product_kb = InlineKeyboardMarkup()
button_product1 = InlineKeyboardButton(text='product1', callback_data='buy_product1')
button_product2 = InlineKeyboardButton(text='product2', callback_data='buy_product2')
button_product3 = InlineKeyboardButton(text='product3', callback_data='buy_product3')
button_product4 = InlineKeyboardButton(text='product4', callback_data='buy_product4')
product_kb.add(button_product1, button_product2, button_product3, button_product4)


buy_kb = InlineKeyboardMarkup()
buy_kb.add(InlineKeyboardButton(text='Купить', callback_data='confirm_buy_product'))
buy_kb.add(InlineKeyboardButton(text='Назад', callback_data='back_to_menu'))


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup = kb)


@dp.message_handler(text = 'Расчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup = in_kb)


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer("Формула Миффлина-Сан Жеора: 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5")
    await call.answer()


@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await UserState.age.set()
    await call.message.answer("Введите свой возраст:")
    await call.answer()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await UserState.growth.set()
    await message.answer("Введите свой рост (в сантиметрах):")


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await UserState.weight.set()
    await message.answer("Введите свой вес (в килограммах):")


@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша норма калорий: {calories} ккал.")
    await state.finish()


@dp.message_handler(text = 'Информация')
async def info_mes(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.\n"
                         "Введите команду /start, чтобы начать общение.")


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    product_kb = InlineKeyboardMarkup()
    for idx, (title, description, price) in enumerate(products, start=1):
        button = InlineKeyboardButton(text=title, callback_data=f'buy_product{idx}')
        product_kb.add(button)
    await message.answer("Выберите продукт:", reply_markup=product_kb)


@dp.callback_query_handler(text = 'buy_product1')
async def get_product(call):
    with open('product1.jpg', 'rb') as img:
        await bot.send_photo(call.message.chat.id, img, caption=f"Название: Витамин А | Описание: для зрения,"
                                                                f" роста, деления клеток, "
                                                                f"репродуктивной функции и иммунитета. | Цена: 100",
                             reply_markup=buy_kb)
        await call.answer()


@dp.callback_query_handler(text = 'buy_product2')
async def get_product2(call):
    with open('product2.jpg', 'rb') as img:
        await bot.send_photo(call.message.chat.id, img, caption=f"Название: Витамин С | Описание: "
                                                                f"благоприятно воздействует на состояние десен,"
                                                                f" зубов, костной ткани, также контролирует "
                                                                f"состояние сосудов, укрепляет их. | Цена: 200",
                             reply_markup=buy_kb)
        await call.answer()


@dp.callback_query_handler(text = 'buy_product3')
async def get_product3(call):
    with open('product3.jpg', 'rb') as img:
        await bot.send_photo(call.message.chat.id, img, caption=f"Название: Витамин D3 | Описание: "
                                                                f"обмен кальция и фосфора в организме,"
                                                                f" регуляция минерализации костной ткани. | Цена: 300",
                             reply_markup=buy_kb)
        await call.answer()


@dp.callback_query_handler(text = 'buy_product4')
async def get_product4(call):
    with open('product4.jpg', 'rb') as img:
        await bot.send_photo(call.message.chat.id, img, caption=f"Название: Витамин B | Описание: "
                                                                f"для нормального обмена веществ, функционирования"
                                                                f" нервной системы, сердца и мышц, "
                                                                f"а также для производства энергии. | Цена: 400",
                             reply_markup=buy_kb)
        await call.answer()


@dp.callback_query_handler(text='back_to_menu')
async def back(call):
    await get_buying_list(call.message)
    await call.answer()


@dp.callback_query_handler(text='confirm_buy_product')
async def confirm_buy_product1(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await RegistrationState.username.set()
    await message.answer("Введите имя пользователя (только латинский алфавит):")


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if not is_included(username):
        await state.update_data(username=message.text)
        await RegistrationState.email.set()
        await message.answer("Введите свой email:")
    else:
        await message.answer("Пользователь существует, введите другое имя.")


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=message.text)
    await RegistrationState.age.set()
    await message.answer("Введите свой возраст:")


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    age = message.text
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    username = user_data['username']
    email = user_data['email']
    add_user(username, email, age)

    await message.answer("Регистрация завершена!")
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
