# from loader import bot, db
# from handlers import dp
# from aiogram import types
# import asyncio
# import logging
# import sys


# async def main() -> None:
#     await bot.set_my_commands([
#         types.BotCommand(command="start", description="Start"),
#     ])
#     await db.create_db()
#     await db.insert_settings()
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())


# TESTING...
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN: Final = 'PASTE_TOKEN_HERE'
BOT_USERNAME: Final = '@Vadimkov_Delivery_Bot'

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Вітаю! Готовий(а) замовити щось смачненьке?')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Корисна інформація про сервіс: \n1) Доставка триває до ?хв(дуже швидка) \n2) Вартість доставки - 30 грн \n3) Вартість замовлення - від 100 грн \n4) Широкий вибір ...')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('КОНТАКТИ: \n • З питань доставки - @fortwersok \n • Розробка сервісів - <a href="https://alex.rv.ua">ALEX-Developing</a>', parse_mode='HTML')

if __name__ == '__main__':
  print('Starting bot...')
  app = Application.builder().token(TOKEN).build()

  # Commands
  app.add_handler(CommandHandler('start', start_command))
  app.add_handler(CommandHandler('info', info_command))
  app.add_handler(CommandHandler('help', help_command))

  # Polls the bot
  print('Polling...')
  app.run_polling(poll_interval=3)