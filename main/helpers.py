import json
import random
import environ
import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG)

logger = logging.getLogger(__name__)

# logging.config.fileConfig('/path/to/logging.conf')
env = environ.Env()
environ.Env.read_env()


CIPHERS = (
    'AES256-SHA'
)


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)


def send_otp_to_phone(phone_number, message):
    # otp = random.randint(100000, 999999)
    url = 'https://api.smsfly.uz/'
    credentials = {
        "key": env("token"),
        "phone": str(phone_number),
        "message": message
    }
    session = requests.session()
    adapter = TlsAdapter(ssl.OP_NO_SSLv2)
    session.mount("https://", adapter)
    try:
        response = session.request(method='POST', url=url, json=credentials)
        # print(response.text)
        data = json.loads(response.text)
        logger.info(data)
        if data['success']:
            return True, None
        else:
            error = data['reason'] if 'reason' in data else 'Unknown error'
            error += f" {phone_number}"
            logger.error(error)
            return False, error
    except Exception as exception:
        logger.error(exception)
        return False, str(exception)


