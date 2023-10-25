import requests
import json
import datetime
from flask import Flask, request
from flask_cors import CORS

APP_KEY = 'e44b00b4c65364d34961af0e8fd18818'

app = Flask(__name__)
CORS(app)

# 请求API
def url_builder_name(city_name):
    api = 'http://api.openweathermap.org/data/2.5/weather?q='
    unit = 'metric'
    url = api + city_name + '&lang=zh_cn' + '&units=' + unit + '&APPID=' + APP_KEY
    res = requests.get(url)
    return json.loads(res.text)

# 时间格式转换
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%H:%M')
    return converted_time

def pre_processwind(wind):
    if wind > 0.0 and wind < 0.2:
        return 0
    elif wind >= 0.2 and wind < 1.5:
        return 1
    elif wind >= 1.5 and wind < 3.3:
        return 2
    elif wind >= 3.3 and wind < 5.4:
        return 3
    elif wind >= 5.4 and wind < 7.9:
        return 4
    elif wind >= 7.9 and wind < 10.7:
        return 5
    elif wind >= 10.7 and wind < 13.8:
        return 6
    elif wind >= 13.8 and wind < 17.1:
        return 7
    elif wind >= 17.1 and wind < 20.7:
        return 8
    elif wind >= 20.7 and wind < 24.4:
        return 9
    elif wind >= 24.4 and wind < 28.4:
        return 10
    elif wind >= 28.4 and wind < 32.6:
        return 11
    elif wind >= 32.6 and wind < 36.9:
        return 12
def pre_processwinddeg(wind_deg):
    if wind_deg > 22.5 and wind_deg <= 67.5:
        return '东北风'
    elif wind_deg > 67.5 and wind_deg <= 112.5:
        return '东风'
    elif wind_deg > 112.5 and wind_deg <= 157.5:
        return '东南风'
    elif wind_deg > 157.5 and wind_deg <= 202.5:
        return '南风'
    elif wind_deg > 202.5 and wind_deg <= 247.5:
        return '西南风'
    elif wind_deg > 247.5 and wind_deg <= 292.5:
        return '西风'
    elif wind_deg > 292.5 and wind_deg <= 337.5:
        return '西北风'
    elif wind_deg > 337.5 and wind_deg <= 360 or wind_deg > 0 and wind_deg <= 22.5:
        return '北风'


# 提取数据，构建字典
def data_organizer(weather_value):
    data = {
        'city': weather_value.get('name'),
        'country': weather_value.get('sys')['country'],
        'temp': weather_value.get('main')['temp'],
        'temp_max': weather_value.get('main')['temp_max'],
        'temp_min': weather_value.get('main')['temp_min'],
        'humidity': weather_value.get('main')['humidity'],
        'pressure': weather_value.get('main')['pressure'],
        'sky': weather_value.get('weather')[0]['main'],
        'sunrise': time_converter(weather_value.get('sys')['sunrise']),
        'sunset': time_converter(weather_value.get('sys')['sunset']),
        'wind': pre_processwind(weather_value.get('wind')['speed']),
        'wind_deg': pre_processwinddeg(weather_value.get('wind')['deg']),
        'dt': time_converter(weather_value.get('dt')),
        'cloudiness': weather_value.get('clouds')['all'],
        'description': weather_value.get('weather')[0]['description']
    }
    return data

@app.route('/translate', methods=['GET'])
def get_weather_info_as_json():
    keyword = request.args.get('keyword')
    weather_value = url_builder_name(keyword)
    # 构建数据字典
    data = data_organizer(weather_value)
    # 将数据字典转换为 JSON 格式
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    print(json_data)
    return json_data


if __name__ == '__main__':
    app.run(debug=True,port=5001)