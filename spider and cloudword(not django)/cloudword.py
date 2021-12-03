# 制作词云图
import jieba
import wordcloud
import numpy as np
from PIL import Image
import jieba.posseg as psg

mask = np.array(Image.open("1.png"))      #图片路径
fb = open("1.txt","r",encoding="utf-8")    #文本路径
t = fb.read()
fb.close()

# ls=jieba.lcut(t,cut_all=True) # 全模式对应picture3

# ls=jieba.lcut_for_search(t) # 搜索引擎模式对应picture2

# 精简选名词模式
ls = psg.lcut(t)
# ls = [word for word in ls if len(word.strip())>1] 好像在精简模式用不到，排除一个字的
ls = [x.word for x in ls if x.flag=='n'] # 名词
txt = " ".join(ls)
w = wordcloud.WordCloud(font_path="msyhbd.ttc",
                        mask = mask,
                        width = 1920,
                        height = 1080,
                        background_color = "white")
w.generate(txt)
w.to_file("picture.jpg")
print('finish')
