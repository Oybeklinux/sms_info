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

env = environ.Env()
environ.Env.read_env()


CIPHERS = (
    'AES256-SHA'
)

message_available = """
Здравствуйте, payer_name! 

Администрация IT-ACADEMY уведомляет вас о том, что студент student_name пропустил урок study_date числа. 

В случае, если студент заболел или имеет другую уважительную причину, просим вас уведомить Администратора

С уважением,
Администрация IT Academy

——

Assalomu alaykum payer_name!

Sizni IT-ACADEMY maʼmuriyati student_name talaba study_date sanasida dars qoldirganligi haqida xabar beradi.

Agar talaba kasal bo'lib qolgan bo’lsa yoki boshqa uzrli sababga ega bo'lsa, administratorga xabar berishingizni so’raymiz

Hurmat bilan,
IT Academy ma'muriyati
"""

message_homework = """
Здравствуйте, payer_name! 

Администрация IT-ACADEMY уведомляет вас о том, что студент student_name не выполнил домашнее задание за study_date число. 

Мы хотим, чтобы наши студенты учились, работали над собой, достигали своих целей, но это возможно только когда мы работаем с родителями сообща. Поэтому просим вас принять меры, чтобы ребёнок выполнял все задания в срок

С уважением,
Администрация IT Academy

——

Assalomu alaykum payer_name!

Sizni IT-ACADEMY maʼmuriyati student_name talaba study_date sanasida berilgan vazifani bajarmaganligi haqida xabar beradi.

Biz o'quvchilarimiz o'qishlarini, o’z ustida ishlashlarini, o'z maqsadlariga erishishlarini xohlaymiz, lekin bunga faqat ota-onalar bilan birgalikda ishlaganda erishimiz mumkin. Shuning uchun biz sizdan bolaning barcha vazifalarni o'z vaqtida bajarishi uchun choralar ko'rishingizni so'raymiz.

Hurmat bilan,
IT Academy ma'muriyati
"""


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)


def send_otp_to_phone(phone_number, student_name, payer_name, study_date, is_available=True, homework_done=True):
    try:
        if not is_available:
            message = message_available\
                .replace("payer_name", payer_name)\
                .replace("student_name",student_name)\
                .replace("study_date", study_date)
        elif not homework_done:
            message = message_homework \
                .replace("payer_name", payer_name) \
                .replace("student_name", student_name) \
                .replace("study_date", study_date)

        if env('smsgateway') == '1':

            credentials = {
                "login": env('login'),
                "password": env('password'),
                "data": [{"phone": str(phone_number), "text": message}]
            }
            url = env('url_swg')
        else:
            credentials = {
                "key": env("token"),
                "phone": str(phone_number),
                "message": message
            }
            url = env('url')
        logger.info(url)
        logger.info(credentials)
        session = requests.session()
        adapter = TlsAdapter(ssl.OP_NO_SSLv2)
        session.mount("https://", adapter)
        try:
            response = session.request(method='POST', url=url, json=credentials)

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
    except Exception as er:
        logger.error(str(er))

