import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8771966211:AAHRyxKV4CliVxFp9EZ-_AgcRYrZk0zxLSw"

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()

AUDIT_DATA = [
    {"question": "1. Как часто вы употребляете алкоголь?", "options": [("Никогда",0), ("Раз в месяц или реже",1), ("2–4 раза в месяц",2), ("2–3 раза в неделю",3), ("4 раза в неделю или чаще",4)]},
    {"question": "2. Сколько порций алкоголя вы обычно выпиваете за день, когда пьёте?", "options": [("1–2",0), ("3–4",1), ("5–6",2), ("7–9",3), ("10 и более",4)]},
    {"question": "3. Как часто вы выпиваете 6 и более порций за один раз?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти каждый день",4)]},
    {"question": "4. Как часто за последний год вы не могли остановиться после начала употребления?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти ежедневно",4)]},
    {"question": "5. Как часто из-за алкоголя вы не выполняли свои обязанности?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти ежедневно",4)]},
    {"question": "6. Как часто вам нужно было выпить утром, чтобы прийти в себя?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти ежедневно",4)]},
    {"question": "7. Как часто вы чувствовали вину или раскаяние после употребления?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти ежедневно",4)]},
    {"question": "8. Как часто вы не могли вспомнить события из-за алкоголя?", "options": [("Никогда",0), ("Реже раза в месяц",1), ("Раз в месяц",2), ("Раз в неделю",3), ("Почти ежедневно",4)]},
    {"question": "9. Были ли травмы у вас или других людей из-за вашего употребления?", "options": [("Нет",0), ("Да, но не за последний год",2), ("Да, за последний год",4)]},
    {"question": "10. Говорили ли вам близкие или врачи сократить употребление?", "options": [("Нет",0), ("Да, но не за последний год",2), ("Да, за последний год",4)]}
]

class TestStates(StatesGroup):
    answering = State()

WELCOME_TEXT = """
<b>Тест AUDIT — честная проверка употребления алкоголя</b>

Иногда сложно понять:
это просто привычка или уже проблема.

Этот тест разработан Всемирной организацией здравоохранения (ВОЗ)
и используется по всему миру.

Он помогает увидеть ситуацию без иллюзий:
— есть ли риск  
— насколько всё серьёзно  
— нужно ли что-то менять  

<b>Что считается одной порцией алкоголя:</b>
— 330 мл пива (≈ 5%)  
— 150 мл вина (≈ 12%)  
— 40 мл крепкого алкоголя (водка, виски и т.д.)

Всего 10 вопросов. Займёт около 2 минут.

Отвечайте честно — это только для вас.

В конце вы получите результат и объяснение.

Нажмите кнопку ниже, чтобы начать.
"""

def get_interpretation(score: int) -> str:
    if score <= 7:
        return (
            "🟢 <b>Низкий риск</b>\n\n"
            "Скорее всего, ваше употребление алкоголя находится в пределах нормы.\n\n"
            "Важно сохранять контроль и не увеличивать дозы со временем."
        )
    
    elif 8 <= score <= 15:
        return (
            "🟡 <b>Рискованное употребление</b>\n\n"
            "Уже есть признаки, что алкоголь начинает влиять на вашу жизнь.\n\n"
            "Это тот этап, когда ещё можно всё изменить без серьёзных последствий.\n\n"
            "Стоит задуматься и обратить внимание на свои привычки."
        )
    
    elif 16 <= score <= 19:
        return (
            "🟠 <b>Вредное употребление</b>\n\n"
            "Алкоголь уже оказывает заметное влияние на здоровье или жизнь.\n\n"
            "Игнорировать это уже не получится — ситуация требует внимания.\n\n"
            "Рекомендуется обратиться за консультацией и разобраться в причинах."
        )
    
    else:
        return (
            "🔴 <b>Высокая вероятность зависимости</b>\n\n"
            "С высокой вероятностью алкоголь уже стал серьёзной проблемой.\n\n"
            "Самостоятельно справиться может быть сложно.\n\n"
            "Лучшее решение сейчас — не откладывать и обратиться за помощью."
        )

async def ask_question(message: types.Message | types.CallbackQuery, q_index: int):
    q_data = AUDIT_DATA[q_index]
    builder = InlineKeyboardBuilder()
    for text, score in q_data["options"]:
        builder.row(InlineKeyboardButton(text=text, callback_data=f"ans_{score}"))
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(q_data["question"], reply_markup=builder.as_markup())
    else:
        await message.answer(q_data["question"], reply_markup=builder.as_markup())

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    # Кнопка внизу (НЕ пропадает)
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать тест")]],
        resize_keyboard=True
    )

    await message.answer(
        WELCOME_TEXT,
        reply_markup=reply_kb,
        parse_mode="HTML"
    )



@dp.callback_query(F.data == "start_test")
async def start_test(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    await ask_question(callback, 0)
    await callback.answer()

@dp.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data.get("current_q", 0)
    total_score = data.get("total_score", 0)

    score = int(callback.data.split("_")[1])
    total_score += score
    current_q += 1

    if current_q < len(AUDIT_DATA):
        await state.update_data(current_q=current_q, total_score=total_score)
        await ask_question(callback, current_q)
    else:
        result_text = get_interpretation(total_score)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Пройти заново", callback_data="start_test"))
        builder.add(InlineKeyboardButton(text="Записаться на консультацию", url="https://t.me/voshodkrsk"))
        await callback.message.edit_text(
            f"<b>Тест завершен!</b>\n\nВаш результат: <b>{total_score} баллов</b>.\n\n{result_text}",
            reply_markup=builder.as_markup()
        )

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
