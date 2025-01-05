# MinecraftModTranslator

A tool to translate Minecraft mods into Russian using Google Translate API.

## Features

- Extracts `.jar` files and processes `en_us.json` files.
- Translates text from English to Russian.
- Creates new `ru_ru.json` files with translated text.
- Repacks `.jar` files with the translated JSON files.
- Filters mods based on the presence of specific files.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ВашеИмяПользователя/MinecraftModTranslator.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd MinecraftModTranslator
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the script to create the necessary directories:
   ```sh
   python translator.py
   ```
2. Place your `.jar` files in the `in` directory.
3. With the script running, press any key to start the processing.
4. The script will process the `.jar` files:
   - Files that already have Russian localization or do not need localization will be moved to the `full` directory.
   - Translated files will be moved to the `jar_ru` directory.

## Directory Structure

```
MinecraftModTranslator/
├── translator.py
├── in/
├── jar_ru/
├── data/
├── full/
├── README.md
└── requirements.txt
```

## File Descriptions

### `translator.py`

**Description**: Main script for translating mods. Includes functions for unpacking and packing JAR files, translating text, creating directories, reading and writing JSON files, and processing JAR files based on the presence of specific files.

**Usage**:
```sh
python translator.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# MinecraftModTranslator

Инструмент для перевода модов Minecraft на русский язык с использованием Google Translate API.

## Функции

- Извлекает `.jar` файлы и обрабатывает `en_us.json` файлы.
- Переводит текст с английского на русский.
- Создает новые `ru_ru.json` файлы с переведенным текстом.
- Упаковывает `.jar` файлы с переведенными JSON файлами.
- Фильтрует моды на основе наличия определенных файлов.

## Требования

- Python 3.x
- Библиотека Requests (`pip install requests`)

## Установка

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/ВашеИмяПользователя/MinecraftModTranslator.git
   ```
2. Перейдите в директорию репозитория:
   ```sh
   cd MinecraftModTranslator
   ```
3. Установите необходимые зависимости:
   ```sh
   pip install -r requirements.txt
   ```

## Использование

1. Запустите скрипт для создания необходимых директорий:
   ```sh
   python translator.py
   ```
2. Поместите ваши `.jar` файлы в директорию `in`.
3. С запущенным скриптом нажмите любую клавишу для начала обработки.
4. Скрипт обработает `.jar` файлы:
   - Файлы, которые уже имеют русскую локализацию или не нуждаются в локализации, будут перемещены в директорию `full`.
   - Переведенные файлы будут перемещены в директорию `jar_ru`.

## Структура директорий

```
MinecraftModTranslator/
├── translator.py
├── in/
├── jar_ru/
├── data/
├── full/
├── README.md
└── requirements.txt
```

## Описание файлов

### `translator.py`

**Описание**: Основной скрипт для перевода модов. Включает функции для распаковки и упаковки JAR файлов, перевода текста, создания директорий, чтения и записи JSON файлов, а также обработки JAR файлов на основе наличия определенных файлов.

**Использование**:
```sh
python translator.py
```

## Вклад

Вклад приветствуется! Пожалуйста, откройте issue или отправьте pull request.

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).
