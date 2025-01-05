import os
import zipfile
import shutil
import time

def check_assets_in_jar(jar_path):
    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.startswith('assets/'):
                return True
    return False

def find_file_in_jar(zip_ref, file_pattern):
    for file_info in zip_ref.infolist():
        if file_info.filename.endswith(file_pattern) and 'assets/' in file_info.filename and 'lang/' in file_info.filename:
            return True
    return False

def process_jar_files(input_dir, noass_dir, full_ru_dir, no_ru_ru_dir):
    # Создаем выходные директории, если они не существуют
    for dir_path in [noass_dir, full_ru_dir, no_ru_ru_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Получаем список файлов в input_dir
    jar_files = [f for f in os.listdir(input_dir) if f.endswith('.jar')]

    for jar_file in jar_files:
        input_path = os.path.join(input_dir, jar_file)

        if not check_assets_in_jar(input_path):
            shutil.move(input_path, os.path.join(noass_dir, jar_file))
            print(f'Moved to noass: {jar_file}')
            continue

        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            has_en_us = find_file_in_jar(zip_ref, 'en_us.json')
            has_ru_ru = find_file_in_jar(zip_ref, 'ru_ru.json')

        if has_ru_ru:
            destination_dir = full_ru_dir
        elif has_en_us:
            destination_dir = no_ru_ru_dir
        else:
            destination_dir = noass_dir

        try:
            shutil.move(input_path, os.path.join(destination_dir, jar_file))
            print(f'Moved to {destination_dir}: {jar_file}')
        except PermissionError as e:
            print(f'PermissionError: {e}')
            print(f'Failed to move: {jar_file}')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'in')
    noass_dir = os.path.join(script_dir, 'full')
    full_ru_dir = os.path.join(script_dir, 'full_ru')
    no_ru_ru_dir = os.path.join(script_dir, 'step_3_ru_en')

    process_jar_files(input_dir, noass_dir, full_ru_dir, no_ru_ru_dir)
