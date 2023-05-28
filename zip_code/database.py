import typing

import asyncpg

# Чтобы не было повторения имен, модули можно переименовывать
# через конструкцию as <новое имя>. Хорошей практикой разработки
# давать новые имена <имя родительского модуля>_<имя импортированного модуля>
from zip_code import config


class Postgres:
    # Про приведения типов https://habr.com/ru/companies/lamoda/articles/432656/
    bot_config: config.BotConfig
    db_pool: typing.Optional[asyncpg.Pool]

    def __init__(self, bot_config: config.BotConfig):
        self.bot_config = bot_config
        self.db_pool: typing.Optional[asyncpg.Pool] = None

    async def on_startup(self):
        # Хорошей практикой именования асинхронных методов-настройки:
        # `on_startup`, `async_init` или `ainit`
        if not self.db_pool:
            # Документация по библиотеке asyncpg
            # https://magicstack.github.io/asyncpg/current/api/index.html
            # На русском примеры работы https://www.blast.hk/threads/117184/
            self.db_pool = await asyncpg.create_pool(
                user=self.bot_config.ZIP_CODE_PGUSER,
                password=self.bot_config.ZIP_CODE_PGPASSWORD,
                database=self.bot_config.ZIP_CODE_PGDATABASE,
                host=self.bot_config.ZIP_CODE_PGHOST,
                port=self.bot_config.ZIP_CODE_PGPORT,
            )

    async def on_shutdown(self):
        if self.db_pool:
            # Документация по библиотеке asyncpg
            # https://magicstack.github.io/asyncpg/current/api/index.html
            # На русском примеры работы https://www.blast.hk/threads/117184/
            await self.db_pool.close()

    async def insert_new_user(self, query_args: dict):
        async with self.db_pool.acquire() as connection:
            # Так можно сказать какой тип у переменной в ручную
            connection: asyncpg.Connection
            # документация по postgres
            # https://postgrespro.ru/docs/postgresql/14/sql-insert
            await connection.execute(
                """
                INSERT INTO 
                    public.user (chat_id, language)
                VALUES 
                   ($1, $2)
                ON CONFLICT
                   (chat_id)
                DO NOTHING;
                """,
                query_args['chat_id'],
                query_args['language']
            )

    async def select_user_language(self, query_args: dict) -> dict:
        async with self.db_pool.acquire() as connection:
            # Так можно сказать какой тип у переменной в ручную
            connection: asyncpg.Connection
            # документация по postgres
            # https://postgrespro.ru/docs/postgresql/15/sql-select
            result = await connection.fetchrow(
                """
                SELECT 
                    language
                FROM
                    public.user
                WHERE
                    chat_id = $1;
                """,
                query_args['chat_id'],
            )

            return result

    async def update_user_language(self, query_args: dict):
        async with self.db_pool.acquire() as connection:
            # Так можно сказать какой тип у переменной в ручную
            connection: asyncpg.Connection
            # документация по postgres
            # https://postgrespro.ru/docs/postgresql/15/sql-update
            await connection.execute(
                """
                UPDATE 
                    public.user
                SET
                    language = $2
                WHERE
                    chat_id = $1;
                """,
                query_args['chat_id'],
                query_args['language']
            )
