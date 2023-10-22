import requests
from flask import Flask, request,jsonify
from flask_cors import CORS
from translate import translate_text

app = Flask(__name__)
CORS(app)

import json

def transfer(data):
    # 创建一个新的列表，用于存储每个条目的字典
    result_list = []

    # 迭代documents中的每个条目，并提取display_title和url
    for key, value in data["documents"].items():
        display_title = value.get("display_title")
        url = value.get("url")
        if display_title and url:
            item = {"title": display_title, "url": url}
            result_list.append(item)
    # 将列表转换为JSON格式
    filtered_json = json.dumps(result_list, indent=4)

    # 返回新的JSON数据
    return filtered_json


@app.route('/get_worldbank_data', methods=['GET'])
def get_worldbank_data():
    keyword = request.args.get('keyword')
    url = f'https://search.worldbank.org/api/v2/wds?format=json&qterm={keyword}&fl=docdt,count'
    response = requests.get(url)
    data = response.json()
    result = transfer(data)
    return result

if __name__ == '__main__':
    app.run(debug=True,port=5002)
