import pymongo
from aiogram import Bot, Dispatcher

from config import config


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def getInstance(self):
        if self.connection is None:
            connection_string = "mongodb+srv://{username}:{password}@{address}/?retryWrites=true&w=majority"
            self.connection = pymongo.MongoClient(
                connection_string.format(username=config('db_user'), password=config('db_password'), address=config('db_address')))
        return self.connection


class MyBot(metaclass=MetaSingleton):
    instance = None

    def getInstance(self):
        if self.instance is None:
            self.instance = Bot(token=config('token'), parse_mode="HTML")
        return self.instance


class MyDispatcher(metaclass=MetaSingleton):
    instance = None

    def getInstance(self):
        if self.instance is None:
            self.instance = Dispatcher()
        return self.instance


def bootstrap():
    Database()
    MyBot()
    MyDispatcher()
