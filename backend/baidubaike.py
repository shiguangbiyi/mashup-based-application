import requests
from bs4 import BeautifulSoup

def get_baike_summary(keyword):
    url = f"https://baike.baidu.com/item/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    summary_tag = soup.find('div', class_='lemma-summary')
    if summary_tag:
        return summary_tag.get_text(strip=True)
    else:
        return "没有找到相关词条的简述。"

# 测试代码
print(get_baike_summary("广州"))
