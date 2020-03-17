from bs4 import BeautifulSoup
import requests,time,os,random,string

"""
爬虫学习程序，爬取http://jandan.net/ooxx 煎蛋网妹子图
"""
def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str



def getOoxx(folder='ooxx',url='http://jandan.net/ooxx'):
    os.mkdir(folder)
    os.chdir(folder)
    while True:

        ssion = requests.session()
        html_data = ssion.get(url)
        ssion.close()
        time.sleep(1)
        soup = BeautifulSoup(html_data.text,'lxml')

        img_list = soup.select("ol.commentlist > li > div > div.row > div.text > p > img")

        for x in img_list:
            img=x.get('src')
            ssion=requests.session()
            response = ssion.get('http:'+img)
            ssion.close()
            #print(response.content)
            with open(generate_random_str()+'.jpg','wb') as f:
                f.write(response.content)
        url = 'http:' + soup.select('div.comments > div.cp-pagenavi > a.previous-comment-page')[0].get('href')


if __name__ == "__main__":
    getOoxx()