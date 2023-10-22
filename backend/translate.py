from flask import request
import hashlib
import requests

def translate_text(keyword):
    appid = '20231021001854591'
    secret_key = 'RwJIAjG6RnU9MVSqHeVx'
    salt = '123456'
    text = keyword

    # Concatenate strings
    string1 = appid + text + salt + secret_key

    # Calculate MD5
    md5 = hashlib.md5()
    md5.update(string1.encode('utf-8'))
    sign = md5.hexdigest()

    target_language = 'en'

    url = f'https://fanyi-api.baidu.com/api/trans/vip/translate'
    params = {
        'q': text,
        'from': 'auto',
        'to': target_language,
        'appid': appid,
        'salt': salt,
        'sign': sign,
    }

    response = requests.get(url, params=params)
    result = response.json()
    translated_text = result['trans_result'][0]['dst']
    translated_text = translated_text.replace("City", "").replace("Lake", "")
    print(translated_text)
    return translated_text

