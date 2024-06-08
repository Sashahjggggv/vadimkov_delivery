from config.cfg import TOKEN, psw, table
from aiogram import Bot, Dispatcher, Router
from database.db import DataBase
# from utils.monoapi import Mono


db = DataBase(host='localhost', password=psw, database=table)
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
rt = Router()
# mono = Mono()


