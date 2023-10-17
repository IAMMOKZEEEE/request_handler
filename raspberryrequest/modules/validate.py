import requests
import logging
from raspberryrequest.config import VALID, NONRETRYABLE, RETRYABLE, FATAL
from raspberryrequest.exceptions import NonRetryableStatusCodeError, FatalStatusCodeError

logging.basicConfig(
    level=logging.WARNING,
    format=' %(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('proxypull.log')]
)


def valid_status(response: requests.Response) -> bool:
    if not response.text:
        logging.warning('No response.')
        return False
    response_dict = response.json()

    try:
        code = response_dict['code']
    except (AttributeError, KeyError):
        code = response.status_code
    logging.debug('CODE: ', type(code))
    if response.status_code in VALID or code in VALID:
        logging.debug('Valid response code.')
        return True
    elif response.status_code in RETRYABLE or code in RETRYABLE:
        logging.debug('Retryable response code.')
        return False
    elif response.status_code in NONRETRYABLE or code in NONRETRYABLE:
        logging.debug('Non-retryable response code.')
        raise NonRetryableStatusCodeError(
            f'Cannot retry. Non-retryable status: {response.status_code}')
    elif response.status_code in FATAL or code in FATAL:
        logging.debug('Fatal response code.')
        raise FatalStatusCodeError(
            f'Fatal status code: {response.status_code}. Raspberry request will stop.')
    return False