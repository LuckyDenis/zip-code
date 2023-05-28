import aiogram
from aiogram import types

from zip_code import config
from zip_code import middleware
from zip_code import database
from zip_code import zip

bot_config: config.BotConfig = config.get_bot_config()

bot = aiogram.Bot(token=bot_config.ZIP_CODE_TELEGRAM_TOKEN)
dp = aiogram.Dispatcher(bot)

# Устанавливаем middleware
# Если в приложении используется middleware,
# то поступивший запрос сначала попадает в неё,
# и только потом передается в обработчик
# (например это функция `run_cmd_start`).
# Обработчик формирует и отдает ответ.
# Этот ответ снова сначала попадает в
# middleware и уже она отдает его наружу.
dp.middleware.setup(
    middleware.PostgresMiddleware(
        postgres=database.Postgres(
            bot_config=bot_config,
        )
    )
)


@dp.message_handler(commands=['start', 'help'])
async def run_cmd_start(message: types.Message, postgres: database.Postgres):
    await postgres.insert_new_user(
        query_args={
            "chat_id": message.chat.id,
            "language": message.from_user.language_code
        }
    )

    answer_text = {
        'ru': 'Привет!\nЭтот бот поможет тебе узнать '
              'чуть больше про твой почтовый индекс. Отправь его мне',
        'en': 'Hello!\nThis bot will help you find out '
              'a little more about your zip code. Send it to me'
    }

    text = answer_text.get(message.from_user.language_code, 'en')
    await send_message(
        chat_id=message.chat.id,
        text=text,
    )


@dp.message_handler(commands=['languages'])
async def run_cmd_languages(message: types.Message, postgres: database.Postgres):
    await send_message(
        chat_id=message.chat.id,
        text="Russian: /ru\nEnglish: /en",
    )


@dp.message_handler(commands=['ru'])
async def run_cmd_ru_language(message: types.Message, postgres: database.Postgres):
    await postgres.update_user_language(
        query_args={
            "chat_id": message.chat.id,
            "language": 'ru'
        }
    )
    await send_message(
        chat_id=message.chat.id,
        text="Язык изменен",
    )


@dp.message_handler(commands=['en'])
async def run_cmd_en_language(message: types.Message, postgres: database.Postgres):
    await postgres.update_user_language(
        query_args={
            "chat_id": message.chat.id,
            "language": 'en'
        }
    )
    await send_message(
        chat_id=message.chat.id,
        text="Change language",
    )


@dp.message_handler(regexp=r'^\d{5}(?:[-\s]\d{4})?$')
async def run_cmd_post_index(message: types.Message, postgres: database.Postgres):
    code = message.text
    codes_info = await zip.CodeApi(bot_config).get_codes_info(code)

    user_language = await postgres.select_user_language(
        query_args={
            "chat_id": message.chat.id
        }
    )
    if user_language['language'] == 'ru':
        for code_info in codes_info:
            await send_message(
                chat_id=message.chat.id,
                text=f"Код страны: {code_info.country_code}\n"
                     f"Штат: {code_info.state} / {code_info.state_en}\n"
                     f"Город: {code_info.city} / {code_info.city_en}\n"
                     f"Широта: {code_info.latitude}\n"
                     f"Долгота: {code_info.longitude}\n\n",
            )
    elif user_language['language'] == 'en':
        for code_info in codes_info:
            await send_message(
                chat_id=message.chat.id,
                text=f"Country code: {code_info.country_code}\n"
                     f"State: {code_info.state} / {code_info.state_en}\n"
                     f"City: {code_info.city} / {code_info.city_en}\n"
                     f"Latitude: {code_info.latitude}\n"
                     f"Longitude: {code_info.longitude}\n\n",
            )


async def send_message(chat_id: str, text: str):
    await bot.send_message(chat_id=chat_id, text=text)


async def _on_startup(dispatcher):
    middlewares = dispatcher.middleware
    for midd in middlewares.applications:
        if isinstance(midd, middleware.PostgresMiddleware):
            await midd.postgres.on_startup()


async def _on_shutdown(dispatcher):
    middlewares = dispatcher.middleware
    for midd in middlewares.applications:
        if isinstance(midd, middleware.PostgresMiddleware):
            await midd.postgres.on_shutdown()


if __name__ == '__main__':
    # Документация по библиотеке по работе с апи телеграмм
    # (api telegram) https://docs.aiogram.dev/en/latest/quick_start.html
    aiogram.executor.start_polling(
        dispatcher=dp,
        on_startup=_on_startup,
        on_shutdown=_on_shutdown
    )
