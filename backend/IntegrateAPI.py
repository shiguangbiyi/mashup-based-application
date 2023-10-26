from flask import Flask, request
from flask_cors import CORS
from summary import get_summary
from weather import get_weather_info_as_json
from img import get_city_img
from news import get_wangyi_news
from economic import get_worldbank_data
from baseinfo import get_base_info

app = Flask(__name__)
CORS(app)

@app.route('/get_summary', methods=['GET'])
def get_summary_wiki_baidu_sougou():
    keyword = request.args.get('keyword')
    return get_summary(keyword)
@app.route('/get_weather', methods=['GET'])
def get_weather():
    keyword = request.args.get('keyword')
    return get_weather_info_as_json(keyword)

@app.route('/get_bing_img', methods=['GET'])
def get_image():
    keyword = request.args.get('keyword')
    return get_city_img(keyword)

@app.route('/get_news', methods=['GET'])
def get_news():
    city_chinese = request.args.get('keyword')
    return get_wangyi_news(city_chinese)

@app.route('/get_worldbank_data', methods=['GET'])
def get_economic():
    keyword = request.args.get('keyword')
    return get_worldbank_data(keyword)

@app.route('/get_sougou_data', methods=['GET'])
def get_baseinfo():
    keyword = request.args.get('keyword')
    return get_base_info(keyword)

if __name__ == '__main__':
    app.run(debug=True)