from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


# Unknown messages
@router.message()
async def send_answer(message: Message, state: FSMContext):
    await message.answer(text='Не понял, что ты сказал...')
    await state.clear()

