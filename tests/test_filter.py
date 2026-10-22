import datetime
from analyzer.filter import match_filters

# Создаем тестовую запись (дата, уровень, источник, код, сообщение)
record = (
    datetime.datetime(2026, 9, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
    "ERROR", "auth-api", "CODE", "msg"
)


def test_filter_no_limits():
    # Если фильтры не заданы, запись должна проходить
    assert match_filters(record, None, None, None, None) is True


def test_filter_by_level():
    # Проверка фильтра по уровню
    assert match_filters(record, None, None, "ERROR", None) is True
    assert match_filters(record, None, None, "INFO", None) is False


def test_filter_by_source():
    # Проверка фильтра по источнику
    assert match_filters(record, None, None, None, "auth-api") is True
    assert match_filters(record, None, None, None, "payment-worker") is False


def test_filter_by_date():
    # Проверка фильтра по дате
    dt_before = datetime.datetime(2026, 9, 1, 11, 0, 0, tzinfo=datetime.timezone.utc)
    dt_after = datetime.datetime(2026, 9, 1, 13, 0, 0, tzinfo=datetime.timezone.utc)

    # Время записи (12:00) больше 11:00, значит проходит
    assert match_filters(record, dt_before, None, None, None) is True
    # Время записи (12:00) меньше 13:00, значит проходит
    assert match_filters(record, None, dt_after, None, None) is True
    # Время записи (12:00) меньше 11:00 — не проходит (False)
    assert match_filters(record, dt_after, None, None, None) is False