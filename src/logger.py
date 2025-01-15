import logging
import os

# Получаем путь к корню проекта
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Указываем папку для логов в корне проекта
LOGS_DIR = os.path.join(ROOT_DIR, "..", "logs")
LOGS_DIR = os.path.abspath(LOGS_DIR)  # Преобразуем в абсолютный путь


def setup_logger(name_module: str) -> logging.Logger:
    # Определяем путь к файлу логов относительно текущего файла
    log_file_path = os.path.join(LOGS_DIR, f"{name_module}.log")
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger(name_module)
    logger.setLevel(logging.DEBUG)

    # Проверяем, есть ли уже обработчики у логгера
    if not logger.handlers:
        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Форматирование логов
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
