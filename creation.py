import os
import sys
import subprocess




def create_venv():
    # Определение текущей директории
    current_dir = os.getcwd()

    # Создание виртуального окружения
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'], cwd=current_dir)
        print("Виртуальное окружение создано успешно в папке:", os.path.join(current_dir, 'venv'))
    except subprocess.CalledProcessError:
        print("Не удалось создать виртуальное окружение.")



def install_requirements():
    # Определение текущей директории
    current_dir = os.getcwd()

    # Путь к файлу requirements.txt
    requirements_file = os.path.join(current_dir, 'requirements.txt')

    # Проверка наличия файла requirements.txt
    if not os.path.exists(requirements_file):
        print("Файл requirements.txt не найден в текущей директории.")

    # Установка зависимостей из файла requirements.txt
    try:
        subprocess.check_call(['venv/Scripts/pip', 'install', '-r', requirements_file])
        print("Зависимости установлены успешно.")
    except subprocess.CalledProcessError:
        print("Не удалось установить зависимости из файла requirements.txt.")



def run_alembic_upgrade():
    # Определение текущей директории
    current_dir = os.getcwd()

    # Проверка наличия файла alembic.ini
    alembic_ini_path = os.path.join(current_dir, 'alembic.ini')
    if not os.path.exists(alembic_ini_path):
        print("Файл alembic.ini не найден в текущей директории.")

    # Запуск миграции базы данных
    try:
        subprocess.check_call(['venv/Scripts/alembic', 'upgrade', 'head'], cwd=current_dir)
        print("Миграция базы данных выполнена успешно.")
    except subprocess.CalledProcessError:
        print("Не удалось выполнить миграцию базы данных.")



create_venv()
install_requirements()
run_alembic_upgrade()

input("Нажмите Enter для продолжения")
