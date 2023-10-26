from bs4 import BeautifulSoup
import requests

def get_city_img(keyword):
    url = f'https://cn.bing.com/images/search?q={keyword}&first=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    info_tags = soup.find_all('img', class_="mimg rms_img")

    src_list = []
    for tag in info_tags:
        if 'src' in tag.attrs:
            src_list.append(tag['src'])

    return src_list
