import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def get_baike_summary(keyword):
    url = f"https://baike.baidu.com/item/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    summary_tag = soup.find('div', class_='lemma-summary')
    if summary_tag:
        summary_text = summary_tag.get_text(strip=True)
        return re.sub(r'\[\d+\]', '', summary_text)
    else:
        return "没有找到相关词条的简述。"

def get_wikipedia_summary(title):
    url = f"https://zh.wikipedia.org/wiki/{title}"
    try:
        response = requests.get(url, timeout=3)  # 设置超时时间为5秒
        response.raise_for_status()  # 检查是否有错误
        soup = BeautifulSoup(response.text, 'html.parser')

        summary_paragraphs = soup.select('div.mw-parser-output > p')
        summary_text = ' '.join([p.text for p in summary_paragraphs if p.text.strip() != ''])

        if not summary_text:
            summary_text = "没有找到相关词条的简述。"
        else:
            summary_text = re.sub(r'\[\d+\]', '', summary_text)  # 去除[数字]文段
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        summary_text = "没有找到相关词条的简述。"

    return summary_text

@app.route('/get_summary', methods=['GET'])
def get_summary():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Please provide a keyword parameter'}), 400

    summary1 = get_baike_summary(keyword)
    summary2 = get_wikipedia_summary(keyword)
    response_data = {}
    if summary1 or summary2:
        if summary1:
            response_data['summary1'] = summary1
        if summary2:
            response_data['summary2'] = summary2
        print(response_data)
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Failed to retrieve summary'}), 500

if __name__ == '__main__':
    app.run(debug=True)
