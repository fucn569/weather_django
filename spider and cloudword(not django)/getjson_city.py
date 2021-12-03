import json
import time
import random
import requests

class get_weather():
    def __init__( self ):
        print("self")
        self.province_url = 'http://www.nmc.cn/f/rest/province/'
        self.base_url1 = 'http://www.nmc.cn/f/rest/real/'
        self.pro = {}
        self.province_code = {}
        self.get_provice(self.province_url)

    def open_url( self, url ):
        print("open_url")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        response = requests.get(url,headers=headers)
        html = response.text
        return html

    def get_city( self, url ):
        print("get_city")
        html = self.open_url(url)
        target = json.loads(html)
        ls = {}
        for i in target:
            ls[i['city']] = 'http://www.nmc.cn/f/rest/real/' + i['code']
        return ls

    def get_provice( self, url ):
        print("get_provice")
        html = self.open_url(url)
        target = json.loads(html)
        print(target)
        for each in target:
            self.province_code[each['name']] = 'http://www.nmc.cn/f/rest/province/' + each['code']  # 省份:code
        for each in target:
            # 每一个省对应所有城市名和城市名代号
            ls=self.get_city(self.province_code[each['name']])
            time.sleep(random.randint(1,9)/10)
            for key,value in ls.items():
                self.pro[key] = value  # 得到每个省对应的每个市


def main():
    w = get_weather()
    print("writing.......")
    with open('weather_all.json', 'w',encoding='utf-8') as f:
        json.dump(w.pro, f,ensure_ascii=False,indent=2)
        print("finish")


if __name__ == '__main__':
    main()
