import configparser
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

config = configparser.ConfigParser()
config.read("./settings/config.ini")

token = os.getenv('token')
# token = config['Token']['token']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class TalkingBot:

    def __init__(self):
        self.message_hystory = []
        self.user_chat_to = None
        self.user_first_name = None
        self.user_last_name = None
        self.admin_id = 758905227

        self.client = None

    # 1763672666 (Настя)
    # 758905227 (Александр)
    def main_self(self):

        @dp.message_handler(commands=['start'])
        async def send_welcome(message: types.Message):

            if message.from_user.id != self.admin_id:
                self.message_hystory.append(await bot.send_message(self.admin_id, f'<i>Стартовал пользователь с id {message.from_user.id}\n{message.from_user.username}</i>', parse_mode='html'))

                talking_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                talking_start = KeyboardButton('Начать диалог')
                talking_keyboard.add(talking_start)
                self.message_hystory.append(await bot.send_message(message.chat.id, 'Для того, чтобы начать диалог, нажмите на кнопку', reply_markup=talking_keyboard))
            else:
                self.message_hystory.append(await bot.send_message(self.admin_id, 'Бот активен'))

        @dp.message_handler(content_types=['text'])
        async def messages(message):
            if message.text == 'Начать диалог':
                self.user_chat_to = message.chat.id
                self.message_hystory.append(await bot.send_message(self.user_chat_to, f'Запрос отправлен, скоро с вами свяжется опреатор'))
                markup = InlineKeyboardMarkup()
                button = InlineKeyboardButton('Начать диалог', callback_data='start_dialog')
                markup.add(button)
                self.user_first_name = message.from_user.first_name
                self.user_last_name = message.from_user.last_name
                self.client = f'{self.user_first_name} {self.user_last_name}'

                self.message_hystory.append(await bot.send_message(self.admin_id, f'Поступил запрос от пользователя\n'
                                                                                  f'id - {message.from_user.id}\n'
                                                                                  f'first name - {message.from_user.first_name}\n'
                                                                                  f'last name - {message.from_user.last_name}',
                                                                   reply_markup=markup)
                                            )
            else:
                if message.from_user.id == self.user_chat_to:
                    await bot.send_message(self.admin_id, f'{self.client}:\n{message.text}')
                else:
                    await bot.send_message(self.user_chat_to, f'оператор:\n{message.text}')

        @dp.callback_query_handler()
        async def catch_callback(callback: types.CallbackQuery):
            if callback.data == 'start_dialog':
                self.user_id_to = callback.message.from_user.id
                await clear_screen()
                self.message_hystory.append(await bot.send_message(callback.message.chat.id, f"Вы пишете {self.client}"))



        async def clear_screen():
            for msg in reversed(self.message_hystory):
                await msg.delete()
                self.message_hystory.pop()
                pass

        executor.start_polling(dp, skip_updates=True)

TalkingBot().main_self()
