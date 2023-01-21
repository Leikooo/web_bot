from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
import json
from flask import Flask, request

app = Flask(__name__)


BOT_TOKEN = '5934998447:AAHlmdEavqSK4ngXXQbbG-Ja_EHeS9KdvPw'
app_url = 'https://zippy-unicorn-e25167.netlify.app'
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

def webApp_form():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    webApp = WebAppInfo(url=f"{app_url}/form")
    keyboard.add(KeyboardButton(text="Форма", web_app=webApp))
    return keyboard

def webApp_shop():
   keyboard = InlineKeyboardMarkup()
   webApp = WebAppInfo(url=f"{app_url}")
   keyboard.add(InlineKeyboardButton(text="Сделать заказ", web_app=webApp))
   return keyboard


@dp.message_handler(content_types="text")
async def new_mes(message: types.Message):
   await bot.send_message(message.chat.id, 'Заполни форму', parse_mode="Markdown", reply_markup=webApp_form()) #отправляем сообщение с нужной клавиатурой
   await bot.send_message(message.chat.id, 'Купи', parse_mode="Markdown", reply_markup=webApp_shop()) #отправляем сообщение с нужной клавиатурой

@dp.message_handler(content_types="web_app_data")
async def answer(webAppMes):
   print(webAppMes)
   print(webAppMes.web_app_data.data)
   mes= json.loads(webAppMes.web_app_data.data)
   await bot.send_message(webAppMes.chat.id, f"Спасибо за обратную связь:\n\nВаша страна: {mes['country']}\nВаша удица: {mes['street']}")
# answerWebAppQuery
# SentWebAppMessage 
@app.route('/web-data', methods=['POST'])
def result():
   print(request)

if __name__ == "__main__":
    app.run()
    executor.start_polling(dp) 