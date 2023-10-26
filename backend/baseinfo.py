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

def get_baike_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    info_tag = soup.find('div', class_="base-list-wrap")

    abs_tag_first = soup.find('div',class_='abstract-first')
    abs_tag_second = soup.find('div', class_='abstract-second')
    print(abs_tag_first)
    print(abs_tag_second)
    html_content = str(abs_tag_first)+str(abs_tag_second)

    soup = BeautifulSoup(html_content, 'html.parser')

    text_content = soup.get_text()
    text_content = re.sub(r'\[\d+\]', '', text_content)
    print(text_content)

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


def get_base_info(keyword):
    print(keyword)
    url = f'https://baike.sogou.com/m/fullLemma?key={keyword}'
    return get_baike_info(url)
