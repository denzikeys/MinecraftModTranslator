import os
import shutil
import zipfile
import json
import requests
from datetime import datetime

# Пути к папкам
path_jar_en = "./in/"
path_jar_ru = "./jar_ru/"
path_json_all = "./data/json/"
path_ru = "./data/ru/"
path_full = "./full/"

# URL для Google Translate API
google_translate_url = "https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl={}&tl={}&q={}"

# Функция для распаковки JAR файлов
def unjar(jar_path, extract_path):
    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"Extracted {jar_path} to {extract_path}")

# Функция для упаковки JAR файлов
def jar(jar_path, source_dir):
    os.makedirs(os.path.dirname(jar_path), exist_ok=True)
    with zipfile.ZipFile(jar_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, source_dir)
                zip_ref.write(file_path, arcname)
        print(f"Packed {source_dir} into {jar_path}")

# Функция для перевода текста
def translate(text, from_lang, to_lang):
    response = requests.get(google_translate_url.format(from_lang, to_lang, text))
    return response.json()[0][0][0]

# Функция для создания папок
def create_folders(jar_names):
    for jar_name in jar_names:
        mod_name = jar_name.split("-")[0]
        mod_path = os.path.join(path_ru, mod_name)
        os.makedirs(mod_path, exist_ok=True)
        print(f"Created folder {mod_path}")

# Функция для поиска файла en_us.json в подпапках
def find_en_us_json(mod_path):
    for root, dirs, files in os.walk(mod_path):
        if "en_us.json" in files:
            return os.path.join(root, "en_us.json")
    return None

# Функция для поиска файла ru_ru.json в подпапках
def find_ru_ru_json(mod_path):
    for root, dirs, files in os.walk(mod_path):
        if "ru_ru.json" in files:
            return os.path.join(root, "ru_ru.json")
    return None

# Функция для чтения JSON файлов
def read_en_json(jar_names):
    new_json_data = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_all_json = os.path.join(path_json_all, f"{current_date}.json")

    os.makedirs(path_json_all, exist_ok=True)

    for jar_name in jar_names:
        mod_name = jar_name.split("-")[0]
        mod_path = os.path.join(path_ru, mod_name, "assets")
        folder_ru_en_json = find_en_us_json(mod_path)
        if folder_ru_en_json:
            with open(folder_ru_en_json, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                new_json_data.append({mod_name: json_data})
                print(f"Read JSON data from {folder_ru_en_json}")
        else:
            print(f"File not found: {folder_ru_en_json}")

    with open(file_all_json, 'w', encoding='utf-8') as file:
        json.dump(new_json_data, file, indent=2, ensure_ascii=False)
        print(f"Saved combined JSON data to {file_all_json}")

# Функция для перевода JSON файлов
def translate_json(json_file):
    with open(os.path.join(path_json_all, json_file), 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        translated_data = []
        for item in json_data:
            mod_name = list(item.keys())[0]
            translated_namespace = {}
            for key, value in item[mod_name].items():
                translated_text = translate(value, "en", "ru")
                translated_namespace[key] = translated_text
            translated_data.append({mod_name: translated_namespace})

    with open(os.path.join(path_json_all, f"ru_{json_file}"), 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, indent=2, ensure_ascii=False)
        print(f"Translated JSON data saved to {os.path.join(path_json_all, f'ru_{json_file}')}")

# Функция для создания русских JSON файлов
def create_ru_json_files(json_file):
    with open(os.path.join(path_json_all, json_file), 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for item in json_data:
            mod_name = list(item.keys())[0]
            original_en_us_path = find_en_us_json(os.path.join(path_ru, mod_name, "assets"))
            if original_en_us_path:
                path_ru_json_file = os.path.join(os.path.dirname(original_en_us_path), "ru_ru.json")
                with open(path_ru_json_file, 'w', encoding='utf-8') as ru_file:
                    json.dump(item[mod_name], ru_file, indent=2, ensure_ascii=False)
                    print(f"Created Russian JSON file at {path_ru_json_file}")
            else:
                print(f"Original en_us.json file not found for {mod_name}")

# Функция для удаления исходного JAR файла
def delete_original_jar(jar_file):
    os.remove(os.path.join(path_jar_en, jar_file))
    print(f"Deleted original JAR file: {jar_file}")

# Функция для очистки папки data
def clear_data_folder():
    for folder in [path_ru, path_json_all]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Cleared folder {folder}")

# Функция для запроса нажатия клавиши
def wait_for_keypress():
    input("Press any key to continue...")

# Функция для проверки наличия папки assets в JAR файле
def check_assets_in_jar(jar_path):
    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
        return any(file_info.filename.startswith('assets/') for file_info in zip_ref.infolist())

# Функция для поиска файла в JAR файле
def find_file_in_jar(zip_ref, file_pattern):
    return any(file_info.filename.endswith(file_pattern) and 'assets/' in file_info.filename and 'lang/' in file_info.filename for file_info in zip_ref.infolist())

# Функция для обработки JAR файлов
def process_jar_files(input_dir, full_dir, jar_ru_dir):
    for dir_path in [full_dir, jar_ru_dir]:
        os.makedirs(dir_path, exist_ok=True)

    jar_files = [f for f in os.listdir(input_dir) if f.endswith('.jar')]

    for jar_file in jar_files:
        clear_data_folder()
        input_path = os.path.join(input_dir, jar_file)

        if not check_assets_in_jar(input_path):
            shutil.move(input_path, os.path.join(full_dir, jar_file))
            print(f'Moved to full: {jar_file}')
            continue

        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            has_en_us = find_file_in_jar(zip_ref, 'en_us.json')
            has_ru_ru = find_file_in_jar(zip_ref, 'ru_ru.json')

        if has_en_us and has_ru_ru:
            shutil.move(input_path, os.path.join(full_dir, jar_file))
            print(f'Moved to full: {jar_file}')
        elif has_en_us:
            mod_name = jar_file.split("-")[0]
            extract_path = os.path.join(path_ru, mod_name)
            unjar(input_path, extract_path)
            read_en_json([jar_file])
            current_date = datetime.now().strftime("%Y-%m-%d")
            translate_json(f"{current_date}.json")
            create_ru_json_files(f"ru_{current_date}.json")
            jar(os.path.join(jar_ru_dir, jar_file), extract_path)
            delete_original_jar(jar_file)
        else:
            shutil.move(input_path, os.path.join(full_dir, jar_file))
            print(f'Moved to full: {jar_file}')

# Основная функция
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'in')
    full_dir = os.path.join(script_dir, 'full')
    jar_ru_dir = os.path.join(script_dir, 'jar_ru')

    for dir_path in [input_dir, full_dir, jar_ru_dir, path_json_all, path_ru]:
        os.makedirs(dir_path, exist_ok=True)

    while True:
        wait_for_keypress()
        clear_data_folder()
        process_jar_files(input_dir, full_dir, jar_ru_dir)

if __name__ == "__main__":
    main()
