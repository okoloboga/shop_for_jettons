from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


# Checking callback from user for [id+space+bet]
class IsEnemy(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        space = callback.data.find(' ')
        return callback.data[0:space].isdigit() and callback.data[space+1:].isdigit()
