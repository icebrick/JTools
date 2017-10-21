from builtins import object
import hashlib
import requests


class Transfer(object):
    '''Transfer between Chinese and English using baidu transfer API'''
    def __init__(self, account_file_path=None):
        # Baidu translate api base url
        self.urlbase = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
        # Get the appid password and md5_salt from a local file
        if account_file_path == None:
            account_file_path = 'baidu_api_account.txt'
        with open(account_file_path, 'r') as f:
            self.appid, self.pw, self.salt = f.read().splitlines()

    def gen_md5(self, str):
        '''Generate the md5 according to the api requirement'''
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def is_chinese(self, uchar):
        '''Check if the string is Chinese'''
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False

    def is_alphabet(self, uchar):
        '''Check if the string is alphabet(English)'''
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False

    def run(self):
        '''Begin the transfer process'''
        # Wait for the user's input until 'q' is entered
        while True:
            q = input('Please input the word need be translated:\n')
            if q == 'q':
                break
            if self.is_chinese(q):
                from_lang = 'zh'
                to_lang = 'en'
            elif self.is_alphabet(q):
                from_lang = 'en'
                to_lang = 'zh'
            else:
                print('Input invalid!\n')
                continue
            sign = self.gen_md5((str(self.appid)+q+str(self.salt)+self.pw).encode('utf-8'))

            payload = {'q': q,
                       'from': from_lang,
                       'to': to_lang,
                       'appid': self.appid,
                       'salt': self.salt,
                       'sign': sign}

            res = requests.get(self.urlbase, params=payload)
            dst = res.json()['trans_result'][0]['dst']
            print(dst)

if __name__ == '__main__':
    Transfer().run()

