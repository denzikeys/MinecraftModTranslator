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

# URL для Google Translate API
google_translate_url = "https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl={}&tl={}&q={}"

# Функция для распаковки JAR файлов
def unjar(jar_path, extract_path):
    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"Extracted {jar_path} to {extract_path}")

# Функция для упаковки JAR файлов
def jar(jar_path, source_dir):
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
        if not os.path.exists(mod_path):
            os.makedirs(mod_path)
            print(f"Created folder {mod_path}")

# Функция для поиска файла en_us.json в подпапках
def find_en_us_json(mod_path):
    for root, dirs, files in os.walk(mod_path):
        if "en_us.json" in files:
            return os.path.join(root, "en_us.json")
    return None

# Функция для чтения JSON файлов
def read_en_json(jar_names):
    new_json_data = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_all_json = os.path.join(path_json_all, f"{current_date}.json")

    # Создаем директорию, если она не существует
    if not os.path.exists(path_json_all):
        os.makedirs(path_json_all)
        print(f"Created directory {path_json_all}")

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
def translate_json():
    json_files = [f for f in os.listdir(path_json_all) if f.endswith(".json")]
    current_date = datetime.now().strftime("%Y-%m-%d")
    for json_file in json_files:
        if json_file.split(".")[0] == current_date:
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
def create_ru_json_files():
    json_files = [f for f in os.listdir(path_json_all) if f.startswith("ru_")]
    current_date = datetime.now().strftime("%Y-%m-%d")
    for json_file in json_files:
        if json_file.split(".")[0].endswith(current_date):
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
    if os.path.exists(path_ru):
        shutil.rmtree(path_ru)
        print(f"Cleared folder {path_ru}")
    if os.path.exists(path_json_all):
        shutil.rmtree(path_json_all)
        print(f"Cleared folder {path_json_all}")

# Функция для запроса нажатия клавиши
def wait_for_keypress():
    input("Press any key to continue...")

# Основная функция
def main():
    while True:
        wait_for_keypress()
        clear_data_folder()
        jar_files = [f for f in os.listdir(path_jar_en) if f.endswith(".jar")]
        create_folders(jar_files)
        for jar_file in jar_files:
            mod_name = jar_file.split("-")[0]
            extract_path = os.path.join(path_ru, mod_name)
            unjar(os.path.join(path_jar_en, jar_file), extract_path)
        read_en_json(jar_files)
        translate_json()
        create_ru_json_files()
        for jar_file in jar_files:
            mod_name = jar_file.split("-")[0]
            jar(os.path.join(path_jar_ru, jar_file), os.path.join(path_ru, mod_name))
            delete_original_jar(jar_file)

if __name__ == "__main__":
    main()
