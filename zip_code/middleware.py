from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from zip_code import database


class PostgresMiddleware(BaseMiddleware):
    def __init__(self, postgres: database.Postgres):
        self.postgres = postgres
        super(PostgresMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data["postgres"] = self.postgres
