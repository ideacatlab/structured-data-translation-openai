# AI Structured Translator

<p align="center"><a href="https://ideacat.ro" target="_blank"><img src=".github/assets/banner.svg" width="400" alt="AI Structured Translator Banner"></a></p>


## Description

The AI Structured Translator project is a Python3 script designed to translate structured translation files in JSON format into multiple languages. The script takes a JSON file as input, splits it into smaller files, and iterates through them, sending each to the OpenAI API to retrieve the translated data in the specified language. The translated output is then saved in separate folders for each file. The script runs automatically, providing a progress bar and other details in the command-line interface. Upon completion, the translated files are bundled back into a single JSON file, maintaining the original structure but with translated content.

## Configurations

### OpenAI API Key and Environment Variables

Before running the script, ensure that the `.env` file is set up with the required environment variables. Copy the `.env.example` file to create your `.env` file and update the OpenAI API key and other variables as follows:

```dotenv
APP_NAME="AI Structured Translator"
APP_ENV=local
APP_URL=http://127.0.0.1:8000

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_ORGANIZATION=org-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_TIMEOUT_INTERVAL=60
OPENAI_RATE_LIMIT=3
OPENAI_MODEL="gpt-3.5-turbo"
OPENAI_TEMPERATURE=0
OPENAI_MAX_TOKENS=750
OPENAI_TOP_P=1
OPENAI_FREQUENCY_PENALTY=0
OPENAI_PRESENCE_PENALTY=0
```

### Logging Configurations

The logging configurations are specified in the `log.conf` file. You can edit this file to adjust the log level (e.g., from INFO to WARNING or ERROR) based on your preferences.

```conf
[loggers]
keys=root

[handlers]
keys=fileHandler

[formatters]
keys=fileFormatter

[logger_root]
level=INFO
handlers=fileHandler

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=fileFormatter
args=('storage/logs/translation.log', 'w')

[formatter_fileFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Usage

The script supports various command-line arguments for customization:

- `--initial_json`: Specify the initial JSON file to process (default: 'file.json').
- `--lang`: Specify the target language for translation (default: Romanian).

### Examples

1. Simple usage with default values:

```bash
python3 main_script.py
```

2. Specify the target language:

```bash
python3 main_script.py --lang "Italian"
```

3. Specify both the initial JSON file and target language:

```bash
python3 main_script.py --initial_json path.json --lang "Language"
```

## Progress Messages

During script execution, progress messages are displayed in the console, showing the translation progress for each smaller JSON file. Example:

```bash
55 smaller JSON files have been created in the "storage/app/parts" folder.
Translating:   0%|                                                                                                              | 0/55 [00:00<?, ?it/s]Translated and saved: storage/app/translate/1-file.json (Processed: 1/55)
Translating:   2%|██▌                                                                                                           | 1/55 [00:11<10:07, 11.25s/it]Translated and saved: storage/app/translate/2-file.json (Processed: 2/55)
Translating:   4%|█████                                                                                                         | 2/55 [00:21<09:37, 10.89s/it]Translated and saved: storage/app/translate/3-file.json (Processed: 3/55)
Translating:   5%|███████▌                                                                                                      | 3/55 [00:31<09:03, 10.45s/it]Translated and saved: storage/app/translate/4-file.json (Processed: 4/55)
Translating:   7%|██████████                                                                                                    | 4/55 [01:04<16:14, 19.10s/it]Translated and saved: storage/app/translate/5-file.json (Processed: 5/55)
Translating:   9%|████████████▋                                                                                                 | 5/55 [01:14<13:15, 15.91s/it]Translated and saved: storage/app/translate/6-file.json (Processed: 6/55)
Translating:  11%|███████████████▏                                                                                              | 6/55 [01:20<10:21, 12.69s/it]

[...]

Translating:  98%|██████████████████████████████████████████████████████████████████████████████████████████████████████████▍  | 54/55 [17:41<00:21, 21.76s/it]Translated and saved: storage/app/translate/55-file.json (Processed: 55/55)
Translating: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████ | 55/55 [18:20<00:00, 20.01s/it]
Translation process completed.
Combined translations have been saved to output/translated.json

Script interrupted. Archiving log file...
```

Feel free to explore and adapt the AI Structured Translator project based on your translation needs. If you encounter any issues or have suggestions for improvement, please open an issue on the [GitHub repository](https://github.com/ideacatlab/structured-data-translation-openai).