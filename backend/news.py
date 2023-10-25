import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_news', methods=['GET'])
def get_news():
    city_chinese = request.args.get('keyword')
    url = f'https://c.3g.163.com/nc/article/local/{city_chinese}/0-20.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        news_data = []
        if city_chinese in data:
            news_list = data[city_chinese]
            for news in news_list:
                title = news['title']
                news_url = news['url']
                if news_url != '':
                    news_item = {'title': title, 'url': news_url}
                    news_data.append(news_item)

        json_data = json.dumps(news_data, ensure_ascii=False, indent=2)
        print(json_data)
        return json_data

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True,port=5004)
