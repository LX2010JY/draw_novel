#coding:utf-8

import requests
from bs4 import BeautifulSoup
import threading
def order_page(url,headers):
    '''
        下载推荐排行榜所有小说，共300多本，测试下了一晚上，才下40多本
    :param url:
    :param headers:
    :return:
    '''
    res = requests.get(url,headers=headers)
    res.encoding = 'gbk'
    response = res.text
    BsObj = BeautifulSoup(response,"html.parser")
    list = {}
    boxs = BsObj.findAll('div',{'class':'box'})
    for box in boxs:
        articals = box.findAll('li',{'class':''})
        for artical in articals:
            href = artical.find('a').get('href')
            title = artical.find('a').get_text()
            if href not in list:
                list[href] = title
    return list

def draw(url,headers,article_name):
    '''
        获取一部小说所有章，并分别下载内容
    :param url:
    :param headers:
    :return:
    '''
    res = requests.get(url,headers=headers)
    res.encoding='gbk'
    html = res.text
    BsObj = BeautifulSoup(html,"html.parser")
    a = BsObj.find('div',{'id':'list'})
    dl = a.find('dl')
    dd = dl.find_all('dd')
    for d in dd:
        a = d.find('a')
        href = url+a.get('href')
        title = a.get_text()
        print('下载【'+article_name+'】中->'+title)
        try:
            novel_dow(href,headers,title,article_name)
        except:
            print('地址:'+href+" "+article_name+"下载失败!!!")
            with(open('./novel/' + article_name + '.txt', 'a', encoding='utf-8')) as f:
                f.write('\n\n' + title + ' 丢失了！！！\n')
            with(open('./novel/error.txt', 'a', encoding='utf-8')) as f:
                f.write(title + href + ' 丢失了！！！\n')

        #finally:
        #    print('next-->')

def novel_dow(url,headers,title,article_name):
    '''
        下载小说每一章的内容
    :param url:
    :param headers:
    :param title:
    :return:
    '''
    res = requests.get(url,headers=headers)
    res.encoding='gbk'
    html = res.text
    BsObj = BeautifulSoup(html,"html.parser")

    content = BsObj.find('div',{'id':'content'})
    content = str(content).replace('<br/>','\n')
    content = content.replace('<div id="content">','')
    content = content.replace('</div>', '')
    content = content.replace('热门推荐:、 、 、 、 、 、 、','')
    with(open('./novel/'+article_name+'.txt','a',encoding='utf-8')) as f:
        f.write('\n\n'+title+'\n')
        f.write(content)






if __name__ == '__main__':

    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # url = "http://www.00ksw.com/html/3/3133/"
    url = "http://www.00ksw.com/s_top/allvote.html"
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    # draw(url,headers,'斗破苍穹3')
    novels = order_page(url,headers)
    n=0
    for novel in novels:
        t = threading.Thread(target=draw,args=(novel,headers,novels[novel]))
        n = n+1
        print('添加第{0}个线程'.format(n))
        t.start()
