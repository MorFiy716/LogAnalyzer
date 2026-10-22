from analyzer.parser import parse_line

def test_valid_line():
    # Проверяем, что корректная строка успешно парсится
    line = "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created"
    res = parse_line(line)
    assert res is not None
    assert res[1] == "WARN" # Проверяем, что уровень извлечен верно

def test_broken_line_missing_fields():
    # Проверяем строку, где не хватает полей (меньше 5)
    line = "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK"
    assert parse_line(line) is None

def test_broken_line_invalid_level():
    # Проверяем строку с несуществующим уровнем логирования
    line = "2026-09-01T00:08:59Z | INVALID | auth-api | AUTH_LOGIN_OK | msg"
    assert parse_line(line) is None

def test_broken_line_invalid_date():
    # Проверяем строку с невалидной датой
    line = "not-a-timestamp | ERROR | orders-api | ORDER_REJECTED | timestamp is invalid"
    assert parse_line(line) is None