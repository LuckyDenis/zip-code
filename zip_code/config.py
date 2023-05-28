import dataclasses
import os
import yaml
import pathlib


# Про датаклассы https://pylot.me/article/2-dataclass-i-v-python/#
@dataclasses.dataclass(frozen=True)
class BotConfig:
    ZIP_CODE_TELEGRAM_TOKEN: str
    ZIP_CODE_PGUSER: str
    ZIP_CODE_PGPASSWORD: str
    ZIP_CODE_PGHOST: str
    ZIP_CODE_PGPORT: int
    ZIP_CODE_PGDATABASE: str
    ZIP_CODE_API_TOKEN: str


# Про приведения типов https://habr.com/ru/companies/lamoda/articles/432656/
def get_bot_config() -> BotConfig:
    # Про переменные окружения `os.environ` можно почитать тут
    # https://lumpics.ru/linux-environment-variables/?ysclid=li73zmwpw8987338773
    # в pycharm для удобства можно указать файл в котором
    # можно указать такие переменны. Как это сделать можно посмотреть тут
    # https://overcoder.net/q/23212/как-установить-переменные-окружения-в-pycharm
    # В этом проекте это сделано через файл zip-code.env
    bot_config_path_from_env = os.environ.get('ZIP_CODE_BOT_CONFIG')
    bot_config_path = pathlib.Path(bot_config_path_from_env)

    with open(bot_config_path.resolve()) as bot_config_stream:
        bot_config_file = yaml.safe_load(stream=bot_config_stream)

    return BotConfig(**bot_config_file)
