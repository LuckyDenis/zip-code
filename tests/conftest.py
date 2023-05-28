import os

import pathlib

import psycopg
import pytest
from pytest_postgresql.janitor import DatabaseJanitor

from zip_code import config
from zip_code import database

root = pathlib.Path(__file__).parent.parent

config_file = root.joinpath("tests", "config.yaml")
os.environ["ZIP_CODE_BOT_CONFIG"] = str(config_file.resolve())

migration = root.joinpath('migration')

bot_config: config.BotConfig = config.get_bot_config()


class Message:
    class Chat:
        def __init__(self, chat_id):
            self.id = chat_id

    class FromUser:
        def __init__(self, language_code):
            self.language_code = language_code

    def __init__(self, chat_id, language_code):
        self.chat = self.Chat(chat_id)
        self.from_user = self.FromUser(language_code)


@pytest.fixture
def postgres():
    janitor = DatabaseJanitor(
        user=bot_config.ZIP_CODE_PGUSER,
        password=bot_config.ZIP_CODE_PGPASSWORD,
        port=bot_config.ZIP_CODE_PGPORT,
        host=bot_config.ZIP_CODE_PGHOST,
        dbname=bot_config.ZIP_CODE_PGDATABASE,
        version=1
    )

    try:
        janitor.init()
    except psycopg.errors.DuplicateDatabase:
        janitor.drop()
        janitor.init()

    pg = database.Postgres(bot_config)
    yield pg


@pytest.fixture
def message():
    return Message(1, 'ru')
