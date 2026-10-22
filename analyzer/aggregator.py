# Импортируем Counter из модуля collections.
# Это удобный словарь, который автоматически считает количество повторений элементов.
from collections import Counter


class Aggregator:
    # Класс-аккумулятор. Он накапливает статистику по логам во время чтения файла.

    def __init__(self):
        # Конструктор. Инициализируем счетчики нулями (и пустыми Counter).
        self.total_lines = 0  # Всего строк прочитано
        self.error_lines = 0  # Всего битых строк
        self.filtered_events = 0  # Сколько событий прошло через фильтры
        self.levels = Counter()  # Словарь: уровень -> количество
        self.sources = Counter()  # Словарь: источник -> количество
        self.error_codes = Counter()  # Словарь: код ошибки -> количество

    def process_record(self, record):
        # Метод вызывается для каждой валидной записи, которая прошла фильтры.
        self.filtered_events += 1  # Увеличиваем счетчик отфильтрованных событий

        # Распаковываем запись, нам нужны уровень, источник и код события.
        _, level, source, event_code, _ = record

        # Увеличиваем счетчики для конкретного уровня и источника.
        self.levels[level] += 1
        self.sources[source] += 1

        # Если уровень события — ERROR, то запоминаем его код в счетчике ошибок.
        if level == "ERROR":
            self.error_codes[event_code] += 1

    def get_summary(self, top_n=5):
        # Метод формирует итоговый словарь (сводку) для вывода или сохранения в файл.
        # top_n — сколько самых частых ошибок показать.
        return {
            "total_lines": self.total_lines,
            "error_lines": self.error_lines,
            "filtered_events": self.filtered_events,
            # Преобразуем Counter обратно в обычные словари (dict) для корректного вывода в JSON
            "levels": dict(self.levels),
            "sources": dict(self.sources),
            # most_common(top_n) возвращает список кортежей самых частых элементов (код, количество).
            # dict() преобразует этот список в словарь.
            "top_error_codes": dict(self.error_codes.most_common(top_n))
        }