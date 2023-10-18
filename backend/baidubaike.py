import requests
from bs4 import BeautifulSoup


def get_baike_description(keyword):
    url = f"https://baike.baidu.com/item/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    description_tag = soup.find('div', class_='lemma-summary')
    if description_tag:
        description = description_tag.get_text().strip()
        return description
    else:
        return "无法找到词条描述"


# 使用方法
keyword = "广州"  # 将这里替换为你想查询的词条
print(get_baike_description(keyword))
