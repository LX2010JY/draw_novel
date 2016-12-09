#coding:utf-8

import requests
from bs4 import BeautifulSoup
import io
import sys

def draw(url,headers):
    res = requests.get(url,headers=headers)
    res.encoding='gbk'
    return res.text

def novel(url,headers,title):
    res = requests.get(url,headers=headers)
    res.encoding='gbk'
    html = res.text
    BsObj = BeautifulSoup(html,"html.parser")

    content = BsObj.find('div',{'id':'content'})
    with(open('./novel/我真是大明星.txt','a',encoding='utf-8')) as f:
        f.write('\n'+title+'\n')
        f.write(content.get_text())
    print('获取'+url+'成功')
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    url = "http://www.00ksw.com/html/15/15344/"
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie'      : 'BAIDU_SSP_lcr=http://zhannei.baidu.com/cse/search?s=10977942222484467615&q=%CE%D2%D5%E6%CA%C7%B4%F3%C3%F7%D0%C7; adwinnum=4; Hm_lvt_5501568a6d02946f5182460c1b0af1c7=1481262147,1481262197,1481262430,1481262596; Hm_lpvt_5501568a6d02946f5182460c1b0af1c7=1481262596; CNZZDATA1426290=cnzz_eid%3D783723357-1481257211-null%26ntime%3D1481257211'
    }
    html = draw(url,headers)
    # with(open('./novel/index.txt','w',encoding='utf8')) as f:
    #     f.write(html)
    BsObj = BeautifulSoup(html,"html.parser")
    a = BsObj.find('div',{'id':'list'})
    dl = a.find('dl')
    dd = dl.find_all('dd')
    for d in dd:
        a = d.find('a')
        href = url+a.get('href')
        title = a.get_text()
        novel(href,headers,title)

