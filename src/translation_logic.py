import json
import openai
import time
from .openai_api import call_openai_api
import os
import logging
import logging.config
from dotenv import load_dotenv

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
load_dotenv(override=True)

def translate_and_save(input_file, output_folder, parsed_args=None):
    max_retries = 3
    retry_delay = 20
    custom_retry_delay = 90

    for retry_count in range(max_retries):
        with open(input_file, 'r') as json_file:
            data = json.load(json_file)
            
        lang_argument = parsed_args.lang
        target_language = lang_argument if lang_argument else os.getenv("DEFAULT_OUTPUT_LANGUAGE")
        
        prompt = f'Translate these lines from JSON object from a translation file used in Laravel, from English to {target_language} just on the right side of the key-value pairs. Return me as a response just the JSON object back, translated as I explained, and no more other data.\n{json.dumps(data)}'

        success = False

        try:
            response = call_openai_api(prompt)
            success = True
            logging.info('API request successful')
        # except openai.error.RateLimitError as rate_limit_error:
        #     sleep_time = int(rate_limit_error.meta['wait_seconds'])
        #     logging.warning('Rate limit exceeded. Waiting...')
        #     time.sleep(sleep_time)
        #     logging.warning('Rate limit wait completed')
        except openai.error.Timeout as timeout_error:
            logging.warning('API request timeout. Retrying...')
            time.sleep(retry_delay)
            logging.warning('Retrying API request after timeout')
        except openai.error.ServiceUnavailableError:
            logging.warning('Server overloaded or not ready yet. Waiting...')
            for i in range(custom_retry_delay, 0, -1):
                logging.warning(f'Waiting for {i} seconds...')
                time.sleep(1)
            logging.warning('Wait completed')

        if success:
            response_content = response.choices[0].message['content']
            logging.info('API response received')
            try:
                response_json = json.loads(response_content)
            except json.JSONDecodeError as e:
                logging.error(f'JSON decoding error for {input_file}: {str(e)}')
                if retry_count < max_retries - 1:
                    logging.warning('Retrying JSON decoding...')
                    time.sleep(retry_delay)
                    logging.warning('Retrying JSON decoding completed')
                else:
                    logging.error('Max retries reached. Skipping to the next JSON.')
            else:
                logging.info('JSON decoding successful')
                output_file = os.path.join(output_folder, os.path.basename(input_file))
                logging.info(f'Saving translated JSON to {output_file}')
                with open(output_file, 'w', encoding='utf-8') as translated_file:
                    json.dump(response_json, translated_file, indent=4, ensure_ascii=False)
                    logging.info('Translation saved')
                return response_json

    return None
