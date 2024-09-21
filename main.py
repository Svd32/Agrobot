import logging
import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

# Токен, который ты получил от BotFather
API_TOKEN = '7327717823:AAFT2c6vm7Jnyl2k4mygRmfURhm-Sqj1GN0'

# Логирование для отладки
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Загрузка данных из таблицы (например, Excel)
def load_data():
    try:
        df = pd.read_excel('warehouse_data.xlsx', sheet_name='Sheet1')
        return df
    except Exception as e:
        logging.error(f"Ошибка загрузки данных: {e}")
        return None

# Обработка команды /start
@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Введите номер ячейки (например, Е-1), чтобы узнать информацию о ней.")

# Обработка текстовых сообщений (номера ячеек)
@dp.message()
async def cell_info(message: Message):
    df = load_data()
    
    if df is None:
        await message.answer("Не удалось загрузить данные.")
        return

    # Получаем введённый пользователем текст и приводим к нижнему регистру
    cell_number = message.text.strip().lower()

    # Приводим значения в колонке 'Ячейка' к нижнему регистру для сравнения
    df['Ячейка'] = df['Ячейка'].str.lower()

    # Поиск строки с указанным номером ячейки
    cell_data = df[df['Ячейка'] == cell_number]

    if not cell_data.empty:
        cell_name = cell_data['Наименование'].values[0]
        item_count = cell_data['Количество'].values[0]

        response = (f"Информация о ячейке:\n"
                    f"Наименование ячейки: {cell_name}\n"
                    f"Должно быть в ячейке: {item_count}")
    else:
        response = "Ячейка с таким номером не найдена."

    await message.answer(response)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
