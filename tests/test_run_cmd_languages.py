import pathlib

from zip_code import main

root = pathlib.Path(__file__).parent.parent
migration = root.joinpath('migration')


async def fake_send_message(*args, **kwargs):
    text = kwargs.get('text')
    assert text == "Russian: /ru\nEnglish: /en"


async def test_run_cmd_start(postgres, message, monkeypatch):
    monkeypatch.setattr(main, 'send_message', fake_send_message)

    await postgres.on_startup()

    async with postgres.db_pool.acquire() as conn:
        for sql_file in sorted(migration.iterdir()):
            with open(sql_file) as file:
                await conn.execute(file.read())

    await main.run_cmd_languages(message, postgres)

    await postgres.on_shutdown()
