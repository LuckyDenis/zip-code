Как запустить бота
------------------
1. Установить зависимости проекта pip install -r ./req.txt
2. Необходимо получить токены:
   - telegram_api https://habr.com/ru/articles/543676/
   - zipcodebase https://app.zipcodebase.com

3. Указать токены в файле ./etc/zip_code/config.yaml
4. Установить плагин в PyCharm EnvFile https://plugins.jetbrains.com/plugin/7861-envfile
5. Запустить main.py
6. Указать в настройках запуска env зависимость на zip-code.env


Как запустить тесты бота
------------------------
1. Установить зависимости проекта pip install -r ./req.txt
2. Выполнить в терминале в папке проекта команду pytests