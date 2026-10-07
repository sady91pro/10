from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.Keyboards.main_menu import main_menu_kb
from bot.Services.sheets import sheets_service
from bot.State.states import AddBirthday, DeleteBirthday
from bot.Utils.date_utils import format_date, parse_date

router = Router(name="birthdays")


# ---------- Список ----------
@router.message(Command("list"))
@router.message(F.text == "📋 Список")
async def list_birthdays(message: Message) -> None:
    records = sheets_service.get_all()
    if not records:
        await message.answer("Список пуст. Добавьте первую запись через ➕ Добавить.")
        return

    lines = ["<b>📋 Все дни рождения:</b>\n"]
    for i, row in enumerate(records, start=1):
        name = row.get("Имя", "—")
        date_val = row.get("Дата рождения", "—")
        extra = row.get("Дополнительно", "")
        suffix = f" — <i>{extra}</i>" if extra else ""
        lines.append(f"{i}. <b>{name}</b> — {date_val}{suffix}")

    await message.answer("\n".join(lines))


# ---------- Добавление ----------
@router.message(Command("add"))
@router.message(F.text == "➕ Добавить")
async def add_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AddBirthday.waiting_name)
    await message.answer("Введите <b>имя</b> именинника (или /cancel для отмены):")


@router.message(AddBirthday.waiting_name)
async def add_name(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Имя слишком короткое. Попробуйте ещё раз:")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(AddBirthday.waiting_date)
    await message.answer(
        "Введите <b>дату рождения</b> в формате <code>ДД.ММ.ГГГГ</code>\n"
        "или <code>ДД.ММ</code>, если год не важен:"
    )


@router.message(AddBirthday.waiting_date)
async def add_date(message: Message, state: FSMContext) -> None:
    parsed = parse_date(message.text or "")
    if not parsed:
        await message.answer("Не удалось разобрать дату. Формат: <code>15.05.1990</code>")
        return
    await state.update_data(date=format_date(message.text.strip()))
    await state.set_state(AddBirthday.waiting_extra)
    await message.answer(
        "Добавьте <b>комментарий</b> (например: друг, коллега) "
        "или отправьте «-», чтобы пропустить:"
    )


@router.message(AddBirthday.waiting_extra)
async def add_extra(message: Message, state: FSMContext) -> None:
    extra = (message.text or "").strip()
    if extra == "-":
        extra = ""

    data = await state.get_data()
    try:
        sheets_service.add(name=data["name"], date_str=data["date"], extra=extra)
    except Exception as e:
        await message.answer(f"❌ Ошибка при записи в Google Sheets: <code>{e}</code>")
        await state.clear()
        return

    await state.clear()
    await message.answer(
        f"✅ Запись добавлена: <b>{data['name']}</b> — {data['date']}",
        reply_markup=main_menu_kb(),
    )


# ---------- Удаление ----------
@router.message(Command("delete"))
@router.message(F.text == "🗑 Удалить")
async def delete_start(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteBirthday.waiting_name)
    await message.answer("Введите имя того, кого нужно удалить (или /cancel):")


@router.message(DeleteBirthday.waiting_name)
async def delete_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name:
        await message.answer("Имя не может быть пустым.")
        return

    ok = sheets_service.delete(name)
    await state.clear()

    if ok:
        await message.answer(f"🗑 Запись <b>{name}</b> удалена.", reply_markup=main_menu_kb())
    else:
        await message.answer(f"❌ Не нашёл запись с именем <b>{name}</b>.", reply_markup=main_menu_kb())


# ---------- Отмена ----------
@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.answer("Нечего отменять.")
        return
    await state.clear()
    await message.answer("Отменено.", reply_markup=main_menu_kb())
