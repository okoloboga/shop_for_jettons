from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from fluentogram import TranslatorRunner

router_unknown = Router()


# Unknown messages
@router_unknown.message()
async def send_answer(message: Message, 
                      state: FSMContext,
                      i18n: TranslatorRunner):
    await message.answer(text=i18n.unknown.message())
    await state.clear()

