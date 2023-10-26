import requests
from bs4 import BeautifulSoup
import re
import json
import time
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def clean_data(data):
    cleaned_data = {}
    for key, value in data.items():
        key = re.sub(r'\s+', '', key).strip()
        value = re.sub(r'\[.*?\]', '', value).strip()
        cleaned_data[key] = value

    # 转换为JSON格式
    json_data = json.dumps(cleaned_data, ensure_ascii=False, indent=4)
    return json_data

def get_baike_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    info_tag = soup.find('div', class_="base-list-wrap")
    print(info_tag)
    if info_tag:
        info_dict = {}
        items = info_tag.find_all('strong')
        values = info_tag.find_all('span')
        for item, value in zip(items, values):
            key = item.get_text(strip=True)
            val = value.get_text(strip=True)
            info_dict[key] = val
        result_json = clean_data(info_dict)
        print(result_json)
        return result_json
    else:
        return "没有找到相关词条的基本信息。"

@app.route('/get_sougou_data', methods=['GET'])
def get_base_info():
    keyword = request.args.get('keyword')
    print(keyword)
    url = 'https://www.sogou.com/web'
    param = {
        'query': keyword
    }
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    # step2 发送请求
    response = requests.get(url=url, params=param, headers=headers)
    # step3 获取响应数据
    soup = BeautifulSoup(response.text, 'html.parser')
    info_tag = soup.find('p', class_ ='star-wiki space-txt')
    info_str = str(info_tag)
    if info_tag:
        url = re.search('href="([^"]+)"', info_str).group(1)
        print(url)
        return get_baike_info(url)
    else:
        print("数据获取异常")
        return "数据获取异常"

if __name__ == '__main__':
    app.run(debug=True,port=5005)