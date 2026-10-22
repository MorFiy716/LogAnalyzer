import sys
from unittest.mock import patch
from analyzer.cli import main


def test_cli_main_success(tmp_path):
    # tmp_path — это временная папка, которую создает pytest для тестов
    log_file = tmp_path / "test.log"
    log_file.write_text("2026-09-01T00:08:59Z | WARN | auth-api | CODE | msg\n", encoding="utf-8")

    # Имитируем ввод пользователя в командную строку
    test_args = ["prog", str(log_file), "--top", "1"]

    # Перехватываем аргументы и вывод, чтобы тест не ломал консоль
    with patch.object(sys, 'argv', test_args):
        main()  # Если ошибок нет, тест пройден


def test_cli_file_not_found():
    test_args = ["prog", "non_existent_file.log"]
    with patch.object(sys, 'argv', test_args):
        try:
            main()
        except SystemExit as e:
            assert e.code == 1  # Проверяем, что программа завершилась с ошибкой