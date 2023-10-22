import urllib
import json
import os

def search_img(keyword):
    search_url = 'http://image.baidu.com/i?tn=baiduimagejson&width=&height=&word=%s&rn=100&pn=0' %(keyword)

    resp = urllib.urlopen(search_url)
    resp_js = json.loads(resp.read().decode('gbk'))
    print(resp_js)
    if resp_js['data']:
        for x in resp_js['data']:
            url = x['objURL']
            try:
                print("downloading :" + url)
                save_to_disk(url, keyword)
            except Exception as e:
                pass

    else:
        return None


def save_to_disk(url, folder):
    base_dir = os.path.dirname(__file__)
    folder = os.path.join(base_dir, folder)
    if not os.path.isdir(folder):
      print('Creating ' + folder)
      os.makedirs(folder)

    filename = url.split('/')[-1]
    fpath = os.path.join(folder, filename.encode('utf8'))
    if os.path.exists(fpath):
        return

    resp = urllib.urlopen(url)
    data = resp.read()
    f = open(fpath, 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    keyword = input('请输入关键词')
    search_img(keyword)