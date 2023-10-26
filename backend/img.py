from bs4 import BeautifulSoup
import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_bing_img', methods=['GET'])
def get_city_img():
    keyword = request.args.get('keyword')
    url = f'https://cn.bing.com/images/search?q={keyword}&first=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    info_tags = soup.find_all('img', class_="mimg rms_img")
    print(info_tags)

    # 提取每个标签中的 src 属性
    src_list = []
    for tag in info_tags:
        if 'src' in tag.attrs:
            src_list.append(tag['src'])

    return src_list

if __name__ == '__main__':
    app.run(debug=True,port=5003)
