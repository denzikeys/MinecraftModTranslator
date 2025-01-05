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

1. Place your `.jar` files in the `in` directory.
2. Run the main script to translate mods:
   ```sh
   python src/translate_mods.py
   ```
3. Run the filter script to sort mods based on file presence:
   ```sh
   python src/filter_mods.py
   ```
4. Run the completion script to finalize the translation process:
   ```sh
   python src/complete_translation.py
   ```
5. Follow the on-screen instructions.

## Directory Structure

```
MinecraftModTranslator/
├── src/
│   ├── translate_mods.py
│   ├── filter_mods.py
│   ├── complete_translation.py
│   └── complete_translation_backup.py
├── README.md
└── requirements.txt
```

## File Descriptions

### `translate_mods.py`

**Description**: Main script for translating mods. Includes functions for unpacking and packing JAR files, translating text, creating directories, reading and writing JSON files.

**Usage**:
```sh
python src/translate_mods.py
```

### `filter_mods.py`

**Description**: Script for filtering mods based on the presence of specific files in JAR archives. Moves mods to appropriate directories based on the presence of `en_us.json` and `ru_ru.json` files.

**Usage**:
```sh
python src/filter_mods.py
```

### `complete_translation.py`

**Description**: Script for completing the translation process. Includes functions for unpacking and packing JAR files, translating text, creating directories, reading and writing JSON files, and processing JAR files based on the presence of specific files.

**Usage**:
```sh
python src/complete_translation.py
```

### `complete_translation_backup.py`

**Description**: Backup copy of the completion script. Includes the same functions as `complete_translation.py` and can be used for testing or as a backup.

**Usage**:
```sh
python src/complete_translation_backup.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
