from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup 

from core.db.db import add_application
from core.keyboards.client_kb import return_kb
from config import ADMIN_IDS


router = Router()


class OrderStates(StatesGroup):
    text = State()


@router.callback_query(F.data == 'make_order')
async def make_an_order(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer_photo(FSInputFile('core/assets/order.png'), 'Для создания ордера заполните поля ниже:\n'
                              '    <i>1: Первый пункт</i>\n'
                              '    <i>2: Второй пункт</i>\n'
                              '    <i>3: Третий пункт</i>\n\n'
                              'После заполнения пунктов, отправьте сообщение в бота.')
    await state.set_state(OrderStates.text)
    await state.update_data(msg_id=msg.message_id)


@router.message(OrderStates.text)
async def make_an_order_second_step(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()

    await message.bot.delete_message(message.from_user.id, int(data["msg_id"]))
    await add_application(message.from_user.id, data["text"])

    application_text = (f'<b>Новый Ордер</b>\n\n'
                        f'<i>{data["text"]}</i>\n\n'
                        f'Пользователь: @{message.from_user.username} | <a href="tg://user?id={message.from_user.id}">Написать</a>')

    for admin_id in ADMIN_IDS:
        await message.bot.send_photo(admin_id, photo=FSInputFile("core/assets/neworder.png"), caption=application_text)
    await message.delete()
    await message.answer_photo(FSInputFile("core/assets/orderuser.png"), f'<i>{data["text"]}</i>\n\nВаш заказ ушёл исполнителю! Ожидайте, с Вами свяжутся', reply_markup=return_kb())
