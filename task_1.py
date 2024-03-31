from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor
import sys


def copy_file(file, dest_path):
    # Визначаємо директорію куди будемо копіювати на основі розширення файлу
    extension_dir = dest_path / file.suffix.replace(".", "")
    extension_dir.mkdir(parents=True, exist_ok=True)
    # Формуємо повний шлях до файлу призначення
    dest_file = extension_dir / file.name
    # Копіюємо файл
    shutil.copy(file, dest_file)


def process_directory(source_path, dest_path):
    # Створення пулу потоків з максимальною кількістю водночас виконуваних потоків, рівною 10
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Рекурсивна ітерація по всіх файлах у заданій директорії (directory) та її піддиректоріях
        # Метод rglob("*.*") шукає всі файли, які мають розширення (ігнорує папки)
        for file in source_path.rglob("*.*"):
            if file.is_file():
                # Відправлення завдання на копіювання файлу в пул потоків для асинхронного виконання
                # Функція copy_file буде виконана в одному з потоків пулу
                executor.submit(copy_file, file, dest_path)


def copy_files_by_extension(source_dir, dest_dir):
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    # Створюємо директорію куди будемо копіювати, або ігноруємо якщо така директорія існує
    dest_path.mkdir(parents=True, exist_ok=True)
    # Обробляємо кожен файл в директорії source_dir паралельно
    process_directory(source_path, dest_path)


def main():
    if len(sys.argv) < 2:
        print(
            "Wrong command, expecting command: python task_1.py source_dir [destination_dir]"
        )
        sys.exit(1)
    source_dir = sys.argv[1]
    dest_dir = "./dist" if len(sys.argv) == 2 else sys.argv[2]
    copy_files_by_extension(source_dir, dest_dir)


if __name__ == "__main__":
    main()
