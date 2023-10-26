from flask import jsonify
import requests
from bs4 import BeautifulSoup
import re
import json

def clean_data(data):
    cleaned_data = {}
    for key, value in data.items():
        key = re.sub(r'\s+', '', key).strip()
        value = re.sub(r'\[.*?\]', '', value).strip()
        cleaned_data[key] = value

    json_data = json.dumps(cleaned_data, ensure_ascii=False, indent=4)
    return json_data

def get_sougou_summary(keyword):
    url = f'https://baike.sogou.com/m/fullLemma?key={keyword}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        abs_tag_first = soup.find('div',class_='abstract-first')
        abs_tag_second = soup.find('div', class_='abstract-second')
        html_content = str(abs_tag_first)+str(abs_tag_second)
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        text_content = re.sub(r'\[\d+\]', '', text_content)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "没有找到相关词条的简述。"

def get_baidu_summary(keyword):
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
            summary_text = re.sub(r'\[\d+\]', '', summary_text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        summary_text = "没有找到相关词条的简述。"

    return summary_text

def get_summary(keyword):
    if not keyword:
        return jsonify({'error': 'Please provide a keyword parameter'}), 400

    summary1 = get_baidu_summary(keyword)
    summary2 = get_wikipedia_summary(keyword)
    summary3 = get_sougou_summary(keyword)
    response_data = {}
    if summary1 or summary2 or summary3:
        if summary1:
            response_data['summary1'] = summary1
        if summary2:
            response_data['summary2'] = summary2
        if summary3:
            response_data['summary3'] = summary3
        print(response_data)
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Failed to retrieve summary'}), 500
