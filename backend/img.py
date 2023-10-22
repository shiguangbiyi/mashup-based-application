import requests
from bs4 import BeautifulSoup

def baidu_image_search(query):
    # 构建搜索URL
    search_url = f'https://image.baidu.com/search/index?tn=baiduimage&word={query}'

    # 发送HTTP请求
    response = requests.get(search_url)

    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取图片信息
        image_info = soup.find_all('img')

        for img in image_info:
            # 获取图片链接和描述
            img_src = img.get('src')
            img_desc = img.get('alt')

            # 打印图片信息
            print(f'图片链接: {img_src}')
            print(f'图片描述: {img_desc}')
            print('---')

    else:
        print('请求失败')

if __name__ == "__main__":
    query = "猫"  # 设置你要搜索的关键词
    print(query)
    baidu_image_search(query)
