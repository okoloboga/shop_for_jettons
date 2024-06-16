from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router_unknown = Router()


# Unknown messages
@router_unknown.message()
async def send_answer(message: Message, state: FSMContext):
    await message.answer(text='Не понял, что ты сказал...')
    await state.clear()

