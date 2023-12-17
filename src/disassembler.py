import json
import os
import logging
import logging.config

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def disassembler(initial_json='ro.json'):
    logging.info(f'Processing JSON file: "{initial_json}"')
    def split_json(input_data, chunk_size):
        chunks = []
        current_chunk = {}
        for key, value in input_data.items():
            current_chunk[key] = value
            if len(current_chunk) == chunk_size:
                chunks.append(current_chunk)
                current_chunk = {}
                logging.info(f'Chunk "{key}" created with "{len(current_chunk)}" items.')
        if current_chunk:
            chunks.append(current_chunk)
            logging.info(f'Final chunk created with "{len(current_chunk)}" items.')
        return chunks

    with open(initial_json, 'r') as json_file:
        data = json.load(json_file)

    chunk_size = 10
    data_chunks = split_json(data, chunk_size)

    if not os.path.exists('storage/app/parts'):
        os.makedirs('storage/app/parts')
        logging.info('JSON storage/app/parts folder "storage/app/parts/" created.')
    else:
        logging.info('JSON parts folder "storage/app/parts/" already exists.')

    for index, chunk in enumerate(data_chunks, 1):
        output_filename = f'storage/app/parts/{index}-{initial_json}'
        with open(output_filename, 'w') as output_file:
            json.dump(chunk, output_file, indent=4)
            logging.info(f'{output_filename} smaller JSON file has been extracted from "{initial_json}".')

    print(f'{len(data_chunks)} smaller JSON files have been created in the "storage/app/parts" folder.')
    logging.info(f'{len(data_chunks)} smaller JSON files have been created in the "storage/app/parts" folder.')

if __name__ == "__main__":
    disassembler()
