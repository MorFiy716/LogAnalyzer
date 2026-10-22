import datetime  # Импортируем модуль для работы с датой и временем

# Множество (set) допустимых уровней логирования.
# Используем set, так как поиск в нем происходит за O(1), быстрее чем в списке.
VALID_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR"}


def parse_line(line):
    # Функция принимает строку (line) и пытается разобрать её на составные части.
    # Возвращает кортеж из 5 элементов или None, если строка битая.

    # Разделяем строку по разделителю " | ". strip() убирает пробелы и переносы строк по краям.
    parts = line.strip().split(" | ")

    # Проверяем, что получилось ровно 5 частей. Если больше или меньше — строка битая.
    if len(parts) != 5:
        return None

    # Распаковываем список parts в переменные.
    ts_str, level, source, event_code, message = parts

    # Проверка: входит ли уровень в список разрешенных (VALID_LEVELS).
    if level not in VALID_LEVELS:
        return None

    # Блок проверки даты (ISO 8601). Используем try-except, так как fromisoformat выбросит ошибку, если дата невалидна.
    try:
        # В Python стандартная библиотека (до 3.11) не понимает букву 'Z' в конце (UTC).
        # Поэтому мы заменяем её на '+00:00', чтобы функция смогла распарсить дату.
        if ts_str.endswith('Z'):
            ts_str = ts_str[:-1] + '+00:00'

        # Пытаемся преобразовать строку в объект datetime. Если не получится — сработает except.
        ts = datetime.datetime.fromisoformat(ts_str)
    except ValueError:
        return None  # Если дата битая, возвращаем None

    # Если все проверки пройдены, возвращаем кортеж с данными.
    return ts, level, source, event_code, message