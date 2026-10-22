from analyzer.aggregator import Aggregator
import datetime


def test_aggregator_logic():
    # Создаем объект агрегатора
    agg = Aggregator()

    # Создаем тестовую запись с уровнем ERROR
    record = (datetime.datetime.now(), "ERROR", "auth-api", "AUTH_ERR", "msg")

    # Передаем ее в агрегатор
    agg.process_record(record)

    # Проверяем, что счетчики увеличились правильно
    assert agg.filtered_events == 1
    assert agg.levels["ERROR"] == 1
    assert agg.sources["auth-api"] == 1
    assert agg.error_codes["AUTH_ERR"] == 1


def test_get_summary():
    # Проверяем, что метод get_summary возвращает словарь с нужными ключами
    agg = Aggregator()
    summary = agg.get_summary(top_n=3)
    assert "total_lines" in summary
    assert "top_error_codes" in summary