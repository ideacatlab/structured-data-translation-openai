import os
import logging
import argparse
import logging.config
from tqdm import tqdm
from natsort import natsorted
from src.disassembler import disassembler
from src.assembler import combine_json_files
from src.translation_logic import translate_and_save
from src.file_operations import setup_logging_folders, archive_log_file, count_translated_files, translate_folder_checks

log_dir = 'storage/logs'
log_file = os.path.join(log_dir, 'translation.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
if not os.path.isfile(log_file):
    open(log_file, 'a').close()


logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Your script description.')
    parser.add_argument('--initial_json', default='file.json', help='Specify the initial JSON file to process.')
    parser.add_argument('--lang', default=None, help='Specify the target language. Default is Romanian.')

    return parser.parse_args()

def main():
    setup_logging_folders()
    args = parse_arguments()
    disassembler(initial_json=args.initial_json)
    translate_folder_checks()

    parts_folder = 'storage/app/parts'
    translate_folder = 'storage/app/translate'
    json_files = natsorted([filename for filename in os.listdir(parts_folder) if filename.endswith('.json')])

    total_files = len(json_files)
    logging.info(f'Found {total_files} JSON files for translation.')

    translated_count = count_translated_files(translate_folder)
    logging.info(f'{translated_count} JSON files already translated.')

    with tqdm(total=total_files, desc='Translating') as pbar:
        for index, filename in enumerate(json_files, 1):
            input_file = os.path.join(parts_folder, filename)
            output_file = os.path.join(translate_folder, filename)

            if os.path.exists(output_file):
                logging.info(f'File "{output_file}" already translated. Skipping...')
                print(f'File "{output_file}" already translated. Skipping...')
                pbar.update(1)
                continue

            response_json = translate_and_save(input_file, translate_folder, args)
            logging.info(f'Translated and saved: translate/{filename} (Processed: {index}/{total_files})')
            print(f'Translated and saved: storage/app/translate/{filename} (Processed: {index}/{total_files})')
            pbar.update(1)

    print('Translation process completed.')
    logging.info('Translation process completed.')
    
    combine_json_files()
    logging.info('Combine all ofthem in a single one.')
    
    logging.info("\nTranslation complete. Archiving log file...")
    print("\nScript interrupted. Archiving log file...")
    archive_log_file()
    
try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    logging.info("\nScript interrupted. Archiving log file...")
    print("\nScript interrupted. Archiving log file...")
    # archive_misc_files()
    # logging.info("Miscelaneous file archived.")
    archive_log_file()
    print("Log file archived.")
except Exception as e:
    print(f"An error occurred: {e}")
    # archive_misc_files()
    # logging.info("Miscelaneous file archived.")
    archive_log_file()
    print("Log file archived.")

