#ptt文章查詢器
from bs4 import BeautifulSoup as bs
from wordcloud import WordCloud
import requests
import jieba
import matplotlib.pyplot as plt

f = open('article.txt','w',encoding='UTF-8')
f.write('')
f.close()
s = requests.session()
#s.post('https://www.ptt.cc/ask/over18', data = {'from': '/bbs/Gossiping/index.html', 'yes': 'yes'})
next_page_url = 'https://www.ptt.cc/bbs/'+input('輸入看板名稱:')+'/index.html'
mm_min , dd_min = map(int,input('輸入日期(僅會查詢該日期以後的文章)(mm dd)').split(' '))
val_min = int(input('搜尋推文數高於多少(<0則搜噓文數)的文章:'))
if next_page_url == 'https://www.ptt.cc/bbs/gossiping/index.html' or next_page_url =='https://www.ptt.cc/bbs/Gossiping/index.html':
  s.post('https://www.ptt.cc/ask/over18', data = {'from': '/bbs/Gossiping/index.html', 'yes': 'yes'})
date_flag = True
count = 0
while date_flag:
  count += 1
  res = s.get(next_page_url)
  #print(res.text)
  soup = bs(res.text, 'html.parser')
  div_tags = soup.find_all('div', {'class': 'title'})
  val_tags = soup.find_all('div', {'class': 'nrec'})
  date_tags = soup.find_all('div', {'class': 'date'})
  btn = soup.select('div.btn-group > a')
  up_page_href = btn[3]['href']
  article_list = []
  pushval_list = []
  artinfo_list = []
  for val_tag in val_tags:
    num_tag= val_tag.find('span')
    #print(num_tag)
    if num_tag is None:
      pushval_list.append(0)
    else:
      pushval_list.append(num_tag.text)
  #f = open('article.txt','a',encoding='UTF-8')
  for div_tag in div_tags:
    a_tag = div_tag.find('a')
    if a_tag is not None:
      article_list.append(a_tag.text)
      #f.write(a_tag.text+'\n')
    else:
      article_list.append('本文章已被刪除')
  f.close()
  for date_tag in date_tags:
    #print(date_tag)
    d_tag = date_tag.get_text()
    artinfo_list.append(d_tag)
  article_list.reverse()
  pushval_list.reverse()
  artinfo_list.reverse()
  f = open('article.txt','a',encoding='UTF-8')
  for date,val,title in zip(artinfo_list,pushval_list,article_list):
    #print(val,type(val))
    if title !='本文章已被刪除':
      appe = title[(title.find(']')+1):]
    f.write(appe+'\n')

    m,d = map(int,date.split('/'))
    #print(m,d)
    if (m<mm_min or (m == mm_min and d < dd_min)) and count!=1:
      date_flag = False
      break
    if type(val) == str:
      if val == '爆':
        val = 100
      elif val[0] == 'X':
        if val == 'XX':
          val = int(-100)
        else: 
          val = int(val[1])*-10
      val = int(val)
      #print(val)
    if val_min>=0:
      if val>=val_min:
        if (val == 100):
          print(date,'爆',title,sep = '\t')
        else:
          print(date,val,title,sep = '\t')
    else:
      if val<=val_min:
        if (val == -100):
          print(date,'XX',title,sep = '\t')
        else:
          print(date,('X'+str(int(val/-10))),title,sep = '\t')
  f.close()
  if (date_flag) == False:
    break
  next_page_url = 'https://www.ptt.cc' + up_page_href

with open('article.txt','r',encoding = 'UTF-8') as rfile:
  text = rfile.read()
jieba.set_dictionary('/content/drive/MyDrive/Colab Notebooks/python 爬蟲/dict.txt.big')
wlist = jieba.cut(text)
words = " ".join(wlist)
wc = WordCloud(width = 1080,height = 1080,scale = 3,min_font_size=50,max_font_size=300,background_color='white',collocations=False,font_path='/content/drive/MyDrive/Colab Notebooks/python 爬蟲/SourceHanSansTW-Regular.otf').generate(words)
plt.imshow(wc)
plt.axis("off")
plt.show()
