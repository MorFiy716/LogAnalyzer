#!/bin/bash
# Активируем виртуальное окружение, чтобы использовать установленные там pytest и pytest-cov
source venv/bin/activate

# Запускаем тесты.
# --cov=analyzer собирает статистику покрытия для папки analyzer.
# --cov-report=html создает красивый HTML-отчет в папке htmlcov.
# tests/ указывает, где лежат файлы с тестами.
pytest --cov=analyzer --cov-report=html tests/

# Выводим сообщение для пользователя о том, куда сохранился отчет.
echo "Отчет создан! Открой файл D:\\WSL_Projects\\LogAnalyzer\\htmlcov\\index.html в браузере."