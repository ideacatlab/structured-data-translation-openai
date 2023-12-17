import os
import json
import shutil
import datetime
import logging
import logging.config

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        logging.info(f'Reading JSON file: {file_path}')
        return json.load(json_file)

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        logging.info(f'Saving JSON file: {file_path}')

log_file = 'storage/logs/translation.log'

def setup_logging_folders():
    if not os.path.exists('storage/logs'):
        os.makedirs('storage/logs')
    if not os.path.exists('storage/logs/archive'):
        os.makedirs('storage/logs/archive')

def archive_log_file():
    archive_folder = os.path.join('storage/logs/archive', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(archive_folder)

    logging.info(f'Log file will be archived to "{archive_folder}/translation.log".')
    shutil.move(log_file, os.path.join(archive_folder, 'translation.log'))
    
# template_file = 'translate/archive'
# part_file = 'parts/archive'
# parts_folder = 'parts'
# translate_folder = 'translate'   
       
# def archive_misc_files():
#     archive_parts = os.path.join(part_file, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
#     os.makedirs(archive_parts)
#     parts_to_archive = [file for file in os.listdir(parts_folder) if file.endswith('.json')]
#     if parts_to_archive:
#         logging.info(f'Archiving {len(parts_to_archive)} JSON files from {parts_folder} to "{part_file}"')
#         for filename in parts_to_archive:
#             source_path = os.path.join(parts_folder, filename)
#             target_path = os.path.join(part_file, filename)
#             shutil.move(source_path, target_path)
    
#     archive_translate = os.path.join(template_file, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
#     os.makedirs(archive_translate)  
#     translate_to_archive = [file for file in os.listdir(translate_folder) if file.endswith('.json')]
#     if translate_to_archive:
#         logging.info(f'Archiving {len(translate_to_archive)} JSON files from {translate_folder} to "{template_file}"')
#         for filename in translate_to_archive:
#             source_path = os.path.join(translate_folder, filename)
#             target_path = os.path.join(template_file, filename)
#             shutil.move(source_path, target_path)

#     logging.info(f'Translated files have been archived to "{archive_translate}".')

def count_translated_files(translate_folder):
    return len([filename for filename in os.listdir(translate_folder) if filename.endswith('.json')])

def translate_folder_checks():
    if not os.path.exists('storage/app/translate'):
        os.makedirs('storage/app/translate')
        logging.info('Translation folder "translate" created.')
    else:
        logging.info('Translation folder "translate" already exists.')