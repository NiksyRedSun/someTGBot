import os
import subprocess


def run_other_script():
    # Определение текущей директории
    current_dir = os.getcwd()

    # Определение пути к скрипту, который нужно запустить
    script_to_run = os.path.join(current_dir, 'main.py')

    # Проверка существования указанного скрипта
    if not os.path.exists(script_to_run):
        print("Указанный скрипт не найден.")
        return

    # Запуск скрипта из виртуального окружения
    try:
        print("Если ниже в логе нет ошибок, значит бот в игре")
        subprocess.check_call([os.path.join(current_dir, 'venv', 'Scripts', 'python'), script_to_run])
        print("Скрипт успешно выполнен.")
    except subprocess.CalledProcessError:
        print("Не удалось выполнить скрипт.")
        return



run_other_script()
input("Нажми ENTER, чтобы выключить бота")
