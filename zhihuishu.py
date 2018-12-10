try:
    from PIL import Image
except ImportError:
    import image

import requests
import pytesseract
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %('
                                               'message)s')


class Zhihuishu(object):

    def __init__(self):
        self.authcode_png = 'https://urp.tfswufe.edu.cn/cas/captcha.jpg'
        self.request_url = 'https://urp.tfswufe.edu.cn/cas/login?service=http%3A%2F%2Fportal.tfswufe.edu.cn%2Fweb' \
                           '%2Fguest '
        self.header = {
            'Referer': 'https://urp.tfswufe.edu.cn/cas/login?service=http%3A%2F%2Fportal.tfswufe.edu.cn%2Fweb%2Fguest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.110 Safari/537.36',
        }
        self.post_data = {
            'username': '41502646',
            'password': '016455',
            'authcode': '',
        }

    def get_authcode(self):
        # response_authcode_png = requests.get(self.authcode_png)
        # authcode_png = response_authcode_png.content
        # try:
        #     os.remove('./authcode.jpg')
        # except IOError:
        #     pass
        # with open('./authcode.jpg', 'wb') as f:
        #     f.write(authcode_png)
        authcode = pytesseract.image_to_string(Image.open('./authcode.jpg'))
        self.post_data['authcode'] = authcode
        logging.info(authcode)

    def do_login(self):
        self.get_authcode()
        logging.info(self.post_data)
        # response = requests.post(self.request_url, data=self.post_data, headers=self.header)
        # logging.info(response.status_code)
        # logging.info(response.text)


if __name__ == '__main__':
    zhs = Zhihuishu()
    zhs.do_login()
