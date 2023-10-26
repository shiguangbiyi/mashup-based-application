import requests
import json

def transfer(data):
    result_list = []

    for key, value in data["documents"].items():
        display_title = value.get("display_title")
        url = value.get("url")
        if display_title and url:
            item = {"title": display_title, "url": url}
            result_list.append(item)
    filtered_json = json.dumps(result_list, indent=4)

    return filtered_json


def get_worldbank_data(keyword):
    url = f'https://search.worldbank.org/api/v2/wds?format=json&qterm={keyword}&fl=docdt,count'
    response = requests.get(url)
    data = response.json()
    result = transfer(data)
    return result

