from django.shortcuts import render
import json
import requests
from bs4 import BeautifulSoup
import random
from pyecharts.charts import Line
from pyecharts import options as opts

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def home(request):
    api=getdatafor_home()
    imag_1=getforroll_home()
    i_1=imag_1['图片']
    i_1t=imag_1['标题']
    imag_2=getforroll_home()
    i_2=imag_2['图片']
    i_2t=imag_2['标题']
    imag_3=getforroll_home()
    i_3=imag_3['图片']
    i_3t=imag_3['标题']
    imag_4=getforroll_home()
    i_4=imag_4['图片']
    i_4t=imag_4['标题']
    return render(request,'home.html',{'api':api,'i_1':i_1,'i_2':i_2,'i_1t':i_1t,'i_2t':i_2t,'i_3':i_3,'i_4':i_4,'i_3t':i_3t,'i_4t':i_4t})

def city(request):
    if request.method=='POST':
        city=request.POST['city']
        dic=getdatafor_city(city)
        dic_pic=getjsonfor_pic(city)
        lis=get_around(city)
        if dic:
            if dic_pic:
                get_render(dic_pic)
                with open('api/render.html','r',encoding='utf-8')as f:
                    html=f.read()
                    f.close()
                soup=BeautifulSoup(html,'lxml')
                body=str(soup.find(name='body'))[6:-8]
                if lis:
                    return render(request,'city.html',{'dic':dic,'body':body,'lis':lis})
                else:
                    return render(request,'city.html',{'dic':dic,'body':body})
            else:
                return render(request,'city.html',{'dic':dic})
        else:
            if dic_pic:
                get_render(dic_pic)
                with open('api/render.html','r',encoding='utf-8')as f:
                    html=f.read()
                    f.close()
                soup=BeautifulSoup(html,'lxml')
                body=str(soup.find(name='body'))[6:-8]
                nf_2='0'
                lis=get_around(city)
                return render(request,'city.html',{'body':body,'nf_2':nf_2,'city':city,'lis':lis})
            else:
                nf='没有找到你想要的(┬＿┬)'
                return render(request,'city.html',{'nf':nf})
    else:
        nf='没有找到你想要的(┬＿┬)'
        return render(request,'city.html',{'nf':nf})

def nav(request):
    name=request.POST['nav']
    if name=='华北':
        lis=get_p_c()[:5]
    elif name=='东北':
        lis=get_p_c()[5:8]
    elif name=='华东':
        lis=get_p_c()[8:15]
    elif name=='华中':
        lis=get_p_c()[15:18]
    elif name=='华南':
        lis=get_p_c()[18:21]
    elif name=='西南':
        lis=get_p_c()[21:26]
    elif name=='西北':
        lis=get_p_c()[26:31]
    elif name=='港澳台':
        lis=get_p_c()[31:]
    com=get_command()
    return render(request,'nav.html',{'lis':lis,'com':com})

def wait(request):
    return render(request,'wait.html',{})



# 以上为django方法，以下为上述调用的爬虫、数据处理函数

# 获取周边景点数据
def get_around(name):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    with open('api/city_code.json', 'r',encoding='utf-8') as f:
        lis=json.load(f)
        f.close()
    lis_d=[]
    for i in lis:
        if name==i['名字']:
            link=i['链接']
            response = requests.get(link,headers=headers)
            response.encoding = 'utf-8'
            html=response.text
            soup = BeautifulSoup(html,'lxml')
            if soup.find(attrs={'class':'aro_view'}).find(name='ul'):
                datas=soup.find(attrs={'class':'aro_view'}).find(name='ul').find_all(name='a')
                for data in datas:
                    dic={}
                    dic['景点']=data.find(name='span').string
                    dic['温度']=data.find(name='i').string
                    dic['链接']=data.attrs['href']
                    lis_d.append(dic)
    return lis_d

# 获取推荐景点数据
def get_command():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    link='http://www.weather.com.cn/weather/101010100.shtml'
    response = requests.get(link,headers=headers)
    response.encoding = 'utf-8'
    html=response.text
    soup = BeautifulSoup(html,'lxml')
    datas=soup.find(attrs={'class':'hotSpot'})
    lis=[]
    comments=datas.find_all(name='li')
    for comment in comments:
        dic={}
        dic['景点']=comment.find(attrs={'class':'name'}).string
        dic['天气']=comment.find(attrs={'class':'weather'}).string
        dic['气温']=comment.find(attrs={'class':'wd'}).string
        dic['旅游指数']=comment.find(attrs={'class':'zs'}).string
        lis.append(dic)
    return(lis)

# 获取导航的省、市数据
def get_p_c():
    with open('api/weather.json','r',encoding='utf-8')as f:
        dic=json.load(f)
        f.close()
    n_lis=[]
    for key,value in dic.items():
        dic_n={}
        lis=[]
        for k,v in value.items():
            lis.append(k)
        dic_n[key]=lis
        n_lis.append(dic_n)
    return(n_lis)

# 渲染pyechart
def get_render(dic):
    line = (Line()
        .add_xaxis(dic['日期'])
        .add_yaxis('最高温', dic['最高温'],
                    is_smooth=True,
                    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
        .add_yaxis('最低温', dic['最低温'],
                    is_smooth=True,
                    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))

        .set_global_opts(title_opts=opts.TitleOpts(title="7天预报曲线"))
        )
    line.render(path='api/render.html')

# 准备图表数据
def getjsonfor_pic(name):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    with open('api/city_code.json', 'r',encoding='utf-8') as f:
        lis=json.load(f)
        f.close()
    dic={}
    date=[]
    gao=[]
    di=[]
    for i in lis:
        if name==i['名字']:
            link=i['链接']
            print(link)
            response = requests.get(link,headers=headers)
            response.encoding = 'utf-8'
            html=response.text
            soup = BeautifulSoup(html,'lxml')
            datas=soup.find(attrs={'class':'t clearfix'}).find_all(name='li')
            for data in datas:
                date.append(data.find(name='h1').string)
                if not data.find(attrs={'class':'tem'}).find(name='span'):
                    # 晚上网站数据会有变化
                    gao.append(int(data.find(attrs={'class':'tem'}).find(name='i').string[:-1]))
                else:
                    gao.append(int(data.find(attrs={'class':'tem'}).find(name='span').string[:-1]))
                    # gao.append(int(data.find(attrs={'class':'tem'}).find(name='span').string))
                di.append(int(data.find(attrs={'class':'tem'}).find(name='i').string[:-1]))
                dic['最低温']=di
                dic['最高温']=gao
                dic['日期']=date
    return dic

# 获取城市天气详细数据
def getdatafor_city(name):
    with open('api/weather_all.json', 'r',encoding='utf-8') as f:
        dic=json.load(f)
        f.close()
    for key,value in dic.items():
        if name == key:
            response = requests.get(value,headers=headers)
            html=response.text
            dic_city={}
            if(html):
                data=json.loads(html)
                dic_city['城市']=name
                dic_city['更新时间']=data['publish_time']
                dic_city['温度']=data['weather']['temperature']
                dic_city['气压']=data['weather']['airpressure']
                dic_city['湿度']=data['weather']['humidity']
                dic_city['降水量']=data['weather']['rain']
                dic_city['天气']=data['weather']['info']
                dic_city['体感温度']=data['weather']['feelst']
                dic_city['风向']=data['wind']['direct']
                dic_city['风力']=data['wind']['power']
                for key,value in dic_city.items():
                    if value == 9999.0 or value=='9999':
                        dic_city[key]='-'
            return dic_city

# 为主页准备数据
def getdatafor_home():
    with open('api/home.json', 'r',encoding='utf-8') as f:
        dic=json.load(f)
        f.close()
    lis=[]
    for city,link in dic.items():
        response = requests.get(link,headers=headers)
        html=response.text
        if(html):
            data=json.loads(html)
            dic_city={}
            dic_city['城市']=city
            dic_city['更新时间']=data['publish_time']
            dic_city['温度']=data['weather']['temperature']
            dic_city['气压']=data['weather']['airpressure']
            dic_city['湿度']=data['weather']['humidity']
            dic_city['降水量']=data['weather']['rain']
            dic_city['天气']=data['weather']['info']
            dic_city['体感温度']=data['weather']['feelst']
            dic_city['风向']=data['wind']['direct']
            dic_city['风力']=data['wind']['power']
            dic_city['图片']=getimagefor_home(city)
            for key,value in dic_city.items():
                if value == 9999.0 or value=='9999':
                    dic_city[key]='-'
            lis.append(dic_city)
    return lis

# 获取主页图片
def getimagefor_home(name):
    with open('api/code.json', 'r',encoding='utf-8') as f:
        dic=json.load(f)
        f.close()
    baseurl = 'http://www.dili360.com/Travel/locality/'
    for key,value in dic.items():
        if name==key:
            url = baseurl+value+'.htm'
            response = requests.get(url,headers=headers)
            html=response.text
            soup = BeautifulSoup(html,'lxml')
            link_lis=soup.find_all(attrs={'class':'thumb-img'})
            link=link_lis[random.randint(1,len(link_lis))-1]
            pic=link.find(name='img').attrs['src']
            while pic[-3:]=='gif':
                link=link_lis[random.randint(1,len(link_lis))-1]
                pic=link.find(name='img').attrs['src']
            # 图片链接结尾rw4是缩略图，rw14是原图，加上这一步则获取原图，但会使主页加载更慢
            # 建议先将图片爬取到本地使用静态文件传入，参考词云图的引入方法
            # pic=pic[:-1]+'14'
            return pic

# 获取轮播图
def getforroll_home():
    base_url = 'http://www.dili360.com/gallery/cate/'
    ran=str(random.randint(1,10))
    url=base_url+ran+'.htm'
    response = requests.get(url,headers=headers)
    html=response.text
    soup = BeautifulSoup(html,'lxml')
    link_lis=soup.find(attrs={'class':'gallery-block-small'}).find_all(name='a')
    dic={}
    if ran=='4':
        a=random.randint(3,13)
    elif ran=='3':
        a=random.randint(0,8)
    elif ran=='8':
        a=random.randint(0,6)
    elif ran=='9':
        a=random.randint(0,18)
    else:
        a=random.randint(0,23)
    link=link_lis[a].find(name='img').attrs['src']
    # 获取原图
    link=link[:-1]+'17'
    title=link_lis[a].attrs['title']
    dic['图片']=link
    dic['标题']=title
    return dic



