import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = os.getenv("APP_API_TOKEN")
ADMIN_ID = int(os.getenv("APP_ADMIN_ID")

class Form(StatesGroup):
    business_type = State()
    city = State()
    name_phone = State()
    site_avito = State()
    avito_report = State()
    comment = State()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать")]],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Ответьте на 6 вопросов и получите бесплатный аудит и предложение по развитию вашего бизнеса уже сегодня\n\nНажмите кнопку ниже, чтобы начать:",
        reply_markup=kb_start
    )

@dp.message(lambda msg: msg.text == "Начать")
async def start_form(message: types.Message, state: FSMContext):
    await state.set_state(Form.business_type)
    await message.answer("1. Вид вашего бизнеса?")

@dp.message(Form.business_type)
async def get_business_type(message: types.Message, state: FSMContext):
    await state.update_data(business_type=message.text)
    await state.set_state(Form.city)
    await message.answer("2. Ваш город?")

@dp.message(Form.city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Form.name_phone)
    await message.answer("3. Ваше имя и телефон?")

@dp.message(Form.name_phone)
async def get_name_phone(message: types.Message, state: FSMContext):
    await state.update_data(name_phone=message.text)
    await state.set_state(Form.site_avito)
    await message.answer("4. Ссылка на сайт и кабинет Авито?")

@dp.message(Form.site_avito)
async def get_site_avito(message: types.Message, state: FSMContext):
    await state.update_data(site_avito=message.text)
    await state.set_state(Form.avito_report)
    await message.answer("5. XLS отчет статистики за последние 30 дней из AvitoPro (при наличии)")

@dp.message(Form.avito_report)
async def get_avito_report(message: types.Message, state: FSMContext):
    await state.update_data(avito_report=message.text)
    await state.set_state(Form.comment)
    await message.answer("6. Комментарий (по желанию)")

@dp.message(Form.comment)
async def get_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    business_type = data.get("business_type", "Не указано")
    city = data.get("city", "Не указано")
    name_phone = data.get("name_phone", "Не указано")
    site_avito = data.get("site_avito", "Не указано")
    avito_report = data.get("avito_report", "Не предоставлен")
    comment = message.text if message.text else "Не указан"

    admin_text = f"📩 Новая заявка на аудит!\n\n🏢 Вид бизнеса: {business_type}\n🌆 Город: {city}\n👤 Имя и телефон: {name_phone}\n🌐 Сайт и Авито: {site_avito}\n📊 Avito отчет: {avito_report}\n💬 Комментарий: {comment}"
    await bot.send_message(ADMIN_ID, admin_text)

    await message.answer(
        "✅ Спасибо за ответы!\n\n"
        "Мы уже получили вашу заявку и приступили к анализу. "
        "В течение дня наш специалист свяжется с вами для обсуждения деталей и подготовки персонального предложения.\n\n"
        "До скорой связи! 📞",
        reply_markup=kb_start
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
