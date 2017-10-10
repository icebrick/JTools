import hashlib
import requests

def gen_md5(str):
    # generate the md5 according to the api requirement
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def is_chinese(uchar):
    # if the string is chinese
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_alphabet(uchar):
    # if the string is alphabet
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

# Baidu translate api base url
urlbase = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
# Get the appid password and md5_salt from a local file
with open('baidu_api_account.txt', 'r') as f:
    appid, pw, salt = f.read().splitlines()

# Wait for the user's input until 'q' is entered
while True:
    q = input('Please input the word need be translated:\n')
    if q == 'q':
        break
    if is_chinese(q):
        from_lang = 'zh'
        to_lang = 'en'
    elif is_alphabet(q):
        from_lang = 'en'
        to_lang = 'zh'
    else:
        print('Input invalid!\n')
        continue
    sign = gen_md5((str(appid)+q+str(salt)+pw).encode('utf-8'))

    payload = {'q': q,
               'from': from_lang,
               'to': to_lang,
               'appid': appid,
               'salt': salt,
               'sign': sign}

    res = requests.get(urlbase, params=payload)
    dst = res.json()['trans_result'][0]['dst']
    print(dst)

