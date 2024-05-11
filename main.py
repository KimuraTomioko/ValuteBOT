"""

Привет, если ты - следующий программист взявщий заказ, то ты - настоящий Iron man! Проект полностью сделан, подключена Юкасса, но
почему-то моему заказчику отказали в её регистрации, я свою часть выполнил, то есть сделал бота и настроил оплату, а вот моему
заказчику-мудачку очень нужны 1000 рублей, он говорит, что я должен вернуть ему 1000 рублей(из 5000, правда. Но не суть), короче,
этому примату отказали в Юкассе, и он требует подключить anypay. Но проблема в том, что у AnyPay отвратительная документация и API
поэтому, я даже мучаться не стал, сказал что не буду подключать и ничего платить. Короче, заказчик просто идиота кусок, ему ничего не
подходит. Я буду очень рад, если ИМЕННО ТЫ выполнишь заказ. Если же ты его выполнишь, то, можешь пожалуйста прислать мне как же ты это
сделал, вот мой телеграм: https://t.me/AntonioMargarettiNt, туда же пиши по всем возникающим вопросам. 
Удачи тебе, а с тобой был 15-ти летний школьник. Да прибудет с тобой код.

P.S:

Вот это я наговнокодил

"""



import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType

# Устанавливаем уровень логгирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token="6348850809:AAGaFkStZtcWslgXGupDv27jNgG8oVAJeK4")
PAYMENT_TOKEN = '1744374395:TEST:0fe170fd35e79da177dc'
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу с тремя колонками: chat_id (целые числа), sum_to_buy (целые числа), paid (строки)
cursor.execute('''CREATE TABLE IF NOT EXISTS purchases
                  (chat_id INTEGER, sum_to_buy INTEGER, user_id_game INT, paid TEXT)''')
conn.commit()

# Определяем обработчик команды "/start"
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Проверяем, существует ли уже запись с данным chat_id
    cursor.execute("SELECT * FROM purchases WHERE chat_id=?", (message.chat.id,))
    existing_entry = cursor.fetchone()
    if existing_entry:
        # Если запись уже существует, отправляем приветственное сообщение с клавиатурой
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button_about_us = KeyboardButton("ℹ️О нас")
        button_buy_currency = KeyboardButton("💵Покупка валюты")
        button_reviews = KeyboardButton("🔥Отзывы")
        keyboard.add(button_about_us, button_buy_currency, button_reviews)
        
        await message.answer("Приветствую, добро пожаловать в магазин для покупки валюты", reply_markup=keyboard)
    else:
        # Если запись не существует, добавляем новую запись в базу данных и отправляем приветственное сообщение
        cursor.execute("INSERT INTO purchases (chat_id) VALUES (?)", (message.chat.id,))
        conn.commit()
        
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button_about_us = KeyboardButton("О нас")
        button_buy_currency = KeyboardButton("💵Покупка валюты")
        button_reviews = KeyboardButton("🔥Отзывы")
        keyboard.add(button_about_us, button_buy_currency, button_reviews)
        
        await message.answer("Приветствую, добро пожаловать в магазин для покупки валюты", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Покупка валюты"
@dp.message_handler(text="💵Покупка валюты")
async def buy_currency(message: types.Message):
    # Создаем клавиатуру с выбором суммы валюты
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("2400 💰"))
    keyboard.add(KeyboardButton("5400 💰"))
    keyboard.add(KeyboardButton("10800 💰"))
    keyboard.add(KeyboardButton("21200 💰"))
    keyboard.add(KeyboardButton("42400 💰"))
    keyboard.add(KeyboardButton("Go Back"))

    # Отправляем сообщение с клавиатурой выбора суммы валюты и картинку
    await message.answer_photo(photo="https://i0.wp.com/news.seagm.com/wp-content/uploads/2023/04/CODM-CPCodeGlobal-featuredimage-1200x675-1.jpg?fit=1200%2C675&ssl=1",
                               caption="📋Price лист:\n 🪙2400 CP - 1350 Рублей.\n 🪙5400 CP - 1350 Рублей.\n 🪙10800 CP - 5000 Рублей.\n 🪙21200 CP - 9500 Рублей.\n 🪙42400 CP - 18700 Рублей.",
                               reply_markup=keyboard)
    await message.answer("Выберите сумму валюты:", reply_markup=keyboard)

# Обработчик нажатия на кнопки суммы валюты
@dp.message_handler(text=["2400 💰", "5400 💰", "10800 💰", "21200 💰", "42400 💰"])
async def select_currency_amount(message: types.Message):
    # Маппинг соответствия CP к G
    cp_to_g = {
        "2400 💰": 1350,
        "5400 💰": 2800,
        "10800 💰": 5000,
        "21200 💰": 9500,
        "42400 💰": 18700
    }
    
    # Получаем выбранное количество валюты из текста кнопки
    currency_amount = cp_to_g[message.text]
    
    # Обновляем значение sum_to_buy в базе данных
    cursor.execute("UPDATE purchases SET sum_to_buy=? WHERE chat_id=?", (currency_amount, message.chat.id))
    conn.commit()
    
    # Отправляем пользователю сообщение о том, что его выбор учтен
    await message.answer(f"Вы выбрали {message.text}. Общая сумма покупки: {currency_amount} рублей.")
    
    # Запрашиваем у пользователя его игровой ID
    await message.answer("🆔Укажите свой id из игры:")
    # Устанавливаем следующий обработчик для получения игрового ID пользователя
    dp.register_message_handler(get_user_id_game, state="*")


# Обработчик для получения игрового ID пользователя
async def get_user_id_game(message: types.Message):
    # Получаем игровой ID пользователя
    user_id_game = message.text
    
    # Обновляем значение user_id_game в базе данных
    cursor.execute("UPDATE purchases SET user_id_game=? WHERE chat_id=?", (user_id_game, message.chat.id))
    conn.commit()
    
    # Сбрасываем состояние обработчика
    await dp.current_state().reset_state()

    # Сообщаем пользователю, что его игровой ID сохранен
    await message.answer("Ваш игровой ID сохранен. Теперь вы можете продолжить. Введите команду /buy для осуществления платежа.")


@dp.message_handler(text='import this')
async def show_python_philosophy(message: types.Message):
    await message.answer_photo(photo='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Zen_Of_Python.png/300px-Zen_Of_Python.png', caption='Красивое лучше, чем уродливое. Явное лучше, чем неявное.\nПростое лучше, чем сложное.\nСложное лучше, чем запутанное.\nПлоское лучше, чем вложенное.\nРазреженное лучше, чем плотное.\nЧитаемость имеет значение.\nОсобые случаи не настолько особые, чтобы нарушать правила.\nПри этом практичность важнее безупречности.\nОшибки никогда не должны замалчиваться.\nЕсли они не замалчиваются явно.\nВстретив двусмысленность, отбрось искушение угадать.\nДолжен существовать один и, желательно, только один очевидный способ сделать это.\nХотя он поначалу может быть и не очевиден, если вы не голландец.\nСейчас лучше, чем никогда.\nХотя никогда зачастую лучше, чем прямо сейчас.\nЕсли реализацию сложно объяснить — идея плоха.\nЕсли реализацию легко объяснить — идея, возможно, хороша.\nПространства имён — отличная штука!\nБудем делать их больше!')

from aiogram import types

from aiogram.types import LabeledPrice

# Обработчик команды /buy
@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    # Получаем сумму для оплаты из базы данных
    cursor.execute("SELECT sum_to_buy FROM purchases WHERE chat_id=?", (message.chat.id,))
    sum_to_buy = cursor.fetchone()[0]
    
    await bot.send_message(message.chat.id, "Тестовый платёж!!!")

    # Создаем объект LabeledPrice для указания цены товара
    labeled_price = LabeledPrice(label="Покупка игровой валюты", amount=sum_to_buy * 100)

    await bot.send_invoice(message.chat.id, 
                           title="Покупку игровой валюты",
                           description="Покупка игровой валюты Call Of Duty",
                           provider_token= PAYMENT_TOKEN, 
                           currency='rub', 
                           photo_url='https://blz-contentstack-images.akamaized.net/v3/assets/bltf408a0557f4e4998/bltd31831eda9199937/62abc0df5cbe472513c0ce59/Cortez_Base_Game-Bnet_Game-Card_Feature-960x540.jpg',
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False, 
                           prices=[labeled_price],  # Передаем объект LabeledPrice вместо простого числа
                           start_parameter='gold-call-of',
                           payload='test-invoice-payload')

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successeful_payment(message: types.Message):
    print("SUCCESSEFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} == {value}")
    
    # Получаем информацию о покупке из базы данных
    cursor.execute("SELECT user_id_game, paid, sum_to_buy FROM purchases WHERE chat_id=?", (message.chat.id,))
    user_id_game, paid, sum_to_buy = cursor.fetchone()

    # Обновляем статус оплаты в базе данных
    cursor.execute("UPDATE purchases SET paid=? WHERE chat_id=?", ("yes", message.chat.id))
    conn.commit()

    # Отправляем личное сообщение с информацией о платеже
    await bot.send_message(
        "1921428012",  # Ваш Telegram ID
        f"Прошла оплата:\n"
        f"id игрока: {user_id_game}\n"
        f"оплачено: yes\n"
        f"chat_id: {message.chat.id}\n"
        f"количество купленной валюты: {sum_to_buy}"
    )
    await bot.send_message(message.chat.id, "🟢Отлично, платёж прошёл! ⌛️Ожидайте 10 минут до пополнения вашего аккаунта!")



'''# Обработчик успешной оплаты
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    # Обновляем статус оплаты в базе данных
    cursor.execute("UPDATE purchases SET paid=? WHERE chat_id=?", ("yes", message.chat.id))
    conn.commit()
    
    # Сообщаем пользователю, что оплата прошла успешно
    await message.answer("Оплата прошла успешно. Спасибо за покупку!")'''

# Обработчик нажатия на кнопку "Go Back"
@dp.message_handler(text="Go Back")
async def go_back(message: types.Message):
    # Создаем клавиатуру с кнопками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_about_us = KeyboardButton("ℹ️О нас")
    button_buy_currency = KeyboardButton("💵Покупка валюты")
    button_reviews = KeyboardButton("🔥Отзывы")
    keyboard.add(button_about_us, button_buy_currency, button_reviews)
    
    # Отправляем приветственное сообщение с клавиатурой
    await message.answer(text='Вернулись обратно', reply_markup=keyboard)

# Обработчик нажатия на кнопку "О нас"
@dp.message_handler(text="ℹ️О нас")
async def send_about_us_info(message: types.Message):
    # Отправляем информацию о нас
    await message.answer("Доброго времени суток\nВ нашем магазине ты можешь купить валюту Call of Dute CP.\nМагазина Аккаунтов  https://t.me/AccountBes\nВладелец  @garant_eremenko\nГарантии https://vk.com/wall-207631280_1\nГоворите за нас друзьям, будем рады, так же не забывайте оставлять отзывы во вкладке - отзывы 😅\nИ остерегайтесь Фейков Будьте бдительны.\nСпасибо за внимание, хорошего настроения, и позитива 😇")

# Обработчик нажатия на кнопку "Отзывы"
@dp.message_handler(text="🔥Отзывы")
async def send_reviews(message: types.Message):
    # Отправляем отзывы
    await message.answer("🫡Тут отзывы о нас 👉 https://t.me/cp_donat_otzivi/2 👈")

# Запускаем бота
if __name__ == '__main__':
    import asyncio
    from aiogram import executor
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)





