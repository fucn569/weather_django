# 收集文本做词云用
import requests
from bs4 import BeautifulSoup 

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
url = 'https://m.weather.com.cn/news/index.shtml'
response = requests.get(url,headers=headers)
response.encoding = 'utf-8'
html=response.text
# print(html)
soup = BeautifulSoup(response.text,'lxml')
# print(soup.prettify())
t1_list=soup.find_all(attrs={'class':'info-title'})
t2_list=soup.find_all(attrs={'class':'swiper-slide'})
for i in t1_list:
    with open('1.txt','a',encoding='utf-8') as f:
        f.write(i.string)
        f.close()
for i in t2_list:
    j=i.find(name='p')
    with open('1.txt','a',encoding='utf-8') as f:
        f.write(j.string)
        f.close()



