import os
import json
import logging
import logging.config
from natsort import natsorted

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def combine_json_files():
    folder_path = 'storage/app/translate'
    json_files = natsorted([file for file in os.listdir(folder_path) if file.endswith('.json')])
    logging.info(f'Sorting JSON from "{folder_path}"')

    combined_translations = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            combined_translations.update(data)
            logging.info(f'Data from "{file_path}" is extracted')

    output_file_path = 'output/translated.json'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(combined_translations, output_file, ensure_ascii=False, indent=4)

    print(f'Combined translations have been saved to {output_file_path}')
    logging.info(f'Combined translations have been saved to {output_file_path}')
    
if __name__ == "__main__":
    combine_json_files()
