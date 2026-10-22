import argparse  # Модуль для разбора аргументов командной строки
import sys  # Нужен для вывода ошибок в stderr и выхода из программы
import json  # Для сохранения отчета в формате JSON
import csv  # Для сохранения отчета в формате CSV
import datetime  # Для парсинга дат из аргументов CLI

# Импортируем наши собственные модули из папки analyzer
from .parser import parse_line
from .filter import match_filters
from .aggregator import Aggregator


def parse_date(date_str):
    if not date_str: return None
    # Мы убираем Z и преобразуем в обычный объект datetime без пояса
    return datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)


def main():
    # Создаем объект парсера аргументов.
    parser = argparse.ArgumentParser(description="CLI-анализатор логов")

    # Добавляем аргументы, которые пользователь может ввести.
    parser.add_argument("input", help="Путь к файлу лога")  # Обязательный аргумент
    parser.add_argument("--from", dest="from_date", type=parse_date, help="Начало интервала (ISO)")
    parser.add_argument("--to", dest="to_date", type=parse_date, help="Конец интервала (ISO)")
    parser.add_argument("--level", choices=["TRACE", "DEBUG", "INFO", "WARN", "ERROR"], help="Фильтр по уровню")
    parser.add_argument("--source", help="Фильтр по источнику")
    parser.add_argument("--top", type=int, default=5, help="Количество топ-ошибок")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Формат вывода")
    parser.add_argument("--output", help="Путь для сохранения отчета")

    # Считываем аргументы, введенные пользователем.
    args = parser.parse_args()

    # Создаем экземпляр нашего агрегатора статистики.
    agg = Aggregator()

    # Блок try-except для обработки ситуации, если файл не найден.
    try:
        # Открываем файл для чтения ('r') с кодировкой UTF-8.
        with open(args.input, 'r', encoding='utf-8') as f:
            # enumerate(f, 1) возвращает номер строки (начиная с 1) и саму строку.
            for line_num, line in enumerate(f, 1):
                if not line.strip(): continue  # Пропускаем пустые строки

                agg.total_lines += 1  # Считаем общее количество строк

                # Пытаемся распарсить строку.
                record = parse_line(line)

                # Если parse_line вернула None, значит строка битая.
                if record is None:
                    agg.error_lines += 1
                    # Выводим информацию о битой строке в поток ошибок (stderr).
                    # Выводим только первые 50 символов, чтобы не засорять консоль.
                    print(f"[ОШИБКА] Битая строка №{line_num}: {line.strip()[:50]}...", file=sys.stderr)
                    continue  # Переходим к следующей строке

                # Если строка валидная, проверяем, проходит ли она через фильтры.
                if match_filters(record, args.from_date, args.to_date, args.level, args.source):
                    agg.process_record(record)  # Если да — обрабатываем и собираем статистику

    except FileNotFoundError:
        # Если файл не найден, выводим ошибку и завершаем программу с кодом 1.
        print(f"Ошибка: Файл '{args.input}' не найден.", file=sys.stderr)
        sys.exit(1)

    # Получаем итоговую сводку из агрегатора.
    summary = agg.get_summary(args.top)

    # Если пользователь указал параметр --output, сохраняем результат в файл.
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as out:
            if args.format == 'json':
                # json.dump записывает словарь в файл. indent=4 делает его красивым (с отступами).
                json.dump(summary, out, indent=4, ensure_ascii=False)
            else:
                # Для CSV используем модуль csv.
                writer = csv.writer(out)
                writer.writerow(["Metric", "Value"])  # Записываем заголовки
                for k, v in summary.items():
                    writer.writerow([k, v])  # Записываем строки "ключ - значение"
        print(f"Отчет сохранен в {args.output}")
    else:
        # Если параметр --output не указан, выводим сводку прямо в консоль.
        print("=== СВОДКА ===")
        print(f"Всего строк: {summary['total_lines']}")
        print(f"Битых строк: {summary['error_lines']}")
        print(f"Событий после фильтрации: {summary['filtered_events']}")
        print(f"Уровни: {summary['levels']}")
        print(f"Источники: {summary['sources']}")
        print(f"Топ-{args.top} ошибок: {summary['top_error_codes']}")


# Стандартная проверка: если скрипт запущен напрямую, вызываем функцию main().
if __name__ == "__main__":
    main()