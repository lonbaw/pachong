#!/usr/bin/env python
# coding=utf-8

import os,time,json,requests,itertools
from requests.adapters import HTTPAdapter
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import json
import re
import time
import requests
import urllib.parse
import xlwt,os
from bs4 import BeautifulSoup
import tornado.web
from tornado.options import define, options

define('port',help='run on the given port', type=int)
cur_dir = os.path.abspath(os.path.dirname(__file__))



# 一个cookie过期时间还未定
headers = {
    "Host": "capi.tianyancha.com",
    "Connection": "keep-alive",
    "Origin": "https://dis.tianyancha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie":"TYCID=babeddc0a22211eabeb80d9af7081601; undefined=babeddc0a22211eabeb80d9af7081601; ssuid=4462633083; bannerFlag=false; RTYCID=c49cbd651c4147f59faed7b31a70c23d; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1590808065; CT_TYCID=9ad7da6a94cb49a493d3c9980c8ad2ba; _ga=GA1.2.440302769.1590808066; _gid=GA1.2.680241161.1590808066; tyc-user-phone=%255B%252213650885588%2522%255D; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522contactNumber%2522%253A%252215959290047%2522%252C%2522schoolName%2522%253A%2522%25E6%25B8%2585%25E5%258D%258E%25E5%25A4%25A7%25E5%25AD%25A6%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522integrity%2522%253A%252290%2525%2522%252C%2522state%2522%253A5%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%25221013%2522%252C%2522schoolGid%2522%253A%2522516739%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%2522296%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzY1MDg4NTU4OCIsImlhdCI6MTU5MDgwODEyMCwiZXhwIjoxNjIyMzQ0MTIwfQ.mru7S-KMCtgefpNl9wQTq-yg-xzto8yf6MPyYupoHu_ZJw8iCBmhz58_yUVpWfWPlsgiv06GS9vX61PXcgLPng%2522%252C%2522schoolAuthStatus%2522%253A%25222%2522%252C%2522vipToTime%2522%253A%25221678289054490%2522%252C%2522schoolLogo%2522%253A%2522https%253A%252F%252Fimg5.tianyancha.com%252Fschool_logo%252Fedb1d57ad7106de0708b485dc134ae3a_gkcx.png%2540!f_200x200%2522%252C%2522companyAlias%2522%253A%2522%25E7%25AE%2580%25E5%258D%2595%25E5%25AD%25A6%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522industry%2522%253A%2522%25E9%2587%2591%25E8%259E%258D%25E4%25B8%259A%2522%252C%2522companyAuthStatus%2522%253A%25222%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522post%2522%253A%2522%25E8%25B4%25A2%25E5%258A%25A1%257C%25E4%25BA%25BA%25E5%258A%259B%25E8%25B5%2584%25E6%25BA%2590%257C%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E8%25B5%25B7%25E9%25A3%259E%25EF%25BC%2581%2522%252C%2522headPicUrl%2522%253A%2522https%253A%252F%252Fcdn.tianyancha.com%252Fuser%252Fheadpic%252Fc42519641a2c4eba93c48beebcc97fb0.png%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522companyName%2522%253A%2522%25E7%25AE%2580%25E5%258D%2595%25E5%25AD%25A6%25EF%25BC%2588%25E5%258E%25A6%25E9%2597%25A8%25EF%25BC%2589%25E6%2595%2599%25E8%2582%25B2%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2522%252C%2522educationBackground%2522%253A%2522%25E5%25B0%258F%25E5%25AD%25A6%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522companyLogo%2522%253A%2522https%253A%252F%252Fimg5.tianyancha.com%252Flogo%252Flll%252F82dd5063f36bf5e9935e45b2fa22a18d.png%2540!f_200x200%2522%252C%2522realName%2522%253A%2522%25E5%2591%25A8%25E5%25AE%2587%25E9%2587%258F%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252250%2522%252C%2522companyGid%2522%253A%25223092280088%2522%252C%2522mobile%2522%253A%252213650885588%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzY1MDg4NTU4OCIsImlhdCI6MTU5MDgwODEyMCwiZXhwIjoxNjIyMzQ0MTIwfQ.mru7S-KMCtgefpNl9wQTq-yg-xzto8yf6MPyYupoHu_ZJw8iCBmhz58_yUVpWfWPlsgiv06GS9vX61PXcgLPng; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1590808131; _gat_gtag_UA_123487620_1=1; cloud_token=8bd0490783a14df2945a92acc513de7c; cloud_utm=26666174a3e4479f863f1387f535e895; rtoken=c01d6f17e5b146afbaf6a47175dbd351; _rutm=afbcf9dad0e74154ae47fb0773334259"
}

#提取Headers里的cookies，getCompanyId函数会用到
Cookies=dict()
for x in headers['Cookie'].split('; '):
    name,value=x.split('=')
    Cookies[name]=value

#print(Cookies)
# js里有段默认值t.default,这里直接debug拿到默认值转换的数组
default_list = [
    ["6", "b", "t", "f", "2", "z", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y", "k", "j",
     "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"],
    ["1", "8", "o", "s", "z", "u", "n", "v", "m", "b", "9", "f", "d", "7", "h", "c", "p", "y", "2", "0", "3", "j", "-",
     "i", "l", "k", "t", "q", "4", "6", "r", "a", "w", "5", "e", "x", "g"],
    ["s", "6", "h", "0", "p", "g", "3", "n", "m", "y", "l", "d", "x", "e", "a", "k", "z", "u", "f", "4", "r", "b", "-",
     "7", "o", "c", "i", "8", "v", "2", "1", "9", "q", "w", "t", "j", "5"],
    ["x", "7", "0", "d", "i", "g", "a", "c", "t", "h", "u", "p", "f", "6", "v", "e", "q", "4", "b", "5", "k", "w", "9",
     "s", "-", "j", "l", "y", "3", "o", "n", "z", "m", "2", "1", "r", "8"],
    ["z", "j", "3", "l", "1", "u", "s", "4", "5", "g", "c", "h", "7", "o", "t", "2", "k", "a", "-", "e", "x", "y", "b",
     "n", "8", "i", "6", "q", "p", "0", "d", "r", "v", "m", "w", "f", "9"],
    ["j", "h", "p", "x", "3", "d", "6", "5", "8", "k", "t", "l", "z", "b", "4", "n", "r", "v", "y", "m", "g", "a", "0",
     "1", "c", "9", "-", "2", "7", "q", "e", "w", "u", "s", "f", "o", "i"],
    ["8", "q", "-", "u", "d", "k", "7", "t", "z", "4", "x", "f", "v", "w", "p", "2", "e", "9", "o", "m", "5", "g", "1",
     "j", "i", "n", "6", "3", "r", "l", "b", "h", "y", "c", "a", "s", "0"],
    ["d", "4", "9", "m", "o", "i", "5", "k", "q", "n", "c", "s", "6", "b", "j", "y", "x", "l", "a", "v", "3", "t", "u",
     "h", "-", "r", "z", "2", "0", "7", "g", "p", "8", "f", "1", "w", "e"],
    ["7", "-", "g", "x", "6", "5", "n", "u", "q", "z", "w", "t", "m", "0", "h", "o", "y", "p", "i", "f", "k", "s", "9",
     "l", "r", "1", "2", "v", "4", "e", "8", "c", "b", "a", "d", "j", "3"],
    ["1", "t", "8", "z", "o", "f", "l", "5", "2", "y", "q", "9", "p", "g", "r", "x", "e", "s", "d", "4", "n", "b", "u",
     "a", "m", "c", "h", "j", "3", "v", "i", "0", "-", "w", "7", "k", "6"],
]

def getCompanyInfo(id):
    headers["Referer"]="https://dis.tianyancha.com/dis/tree?graphId={}&origin=https%3A%2F%2Fwww.tianyancha.com&mobile=&time=15753515647237b28&full=1".format(id)
    # 需要查找的id
    #id = '1698375'
    s = requests.session()

    def getfnstr(data):
        fnstr = ""
        for i in data.split(','):
            fnstr += chr(int(i))
        return fnstr

    def getSogo(default_list, id):
        r = str(ord(id[0]))
        return default_list[int(r[1])]

    def getfxckStr(fxck, window_sogo):
        fxckStr = ""
        for i in fxck.split(','):
            fxckStr += window_sogo[int(i)]
        return fxckStr
    def addnode(nodeinfo):
        message['allNodeinfo'].append(nodeinfo)
    def addedges(edges):
        message['edges'].append(edges)

    # 编写递归函数
    def getnodeinfo():
        # 请求nextNode
        nonlocal i
        nonlocal level
        message_allnodeinfo_dict_bak=message['allNodeinfo'].copy()
        for x in message_allnodeinfo_dict_bak:
            #print('x',x)
            if not x['check']:
                if x['hasnode'] ==True:
                    res3_params={
                        'id':x['nodeid'],
                        'indexId': id,
                        'direction': 'up'
                    }
                    res3 = s.get('https://capi.tianyancha.com/cloud-equity-provider/v4/equity/nextnode.json',params=res3_params,headers=headers)
                    #print(res3.text)
                    for onenode in json.loads(res3.text)['data']:
                        level+=1
                        #print('onenode',onenode)
                        tmpdict = {
                            "name": onenode['name'],
                            "percent": onenode['percent'],
                            "nodeid": onenode['id'],
                            "hasnode": onenode['hasNode'],
                            "level": level,
                            "check": False
                        }
                        print('开始增加node')
                        if tmpdict['percent'] != '100%':
                            addnode(tmpdict)
                        else:
                            tmpdict['level']=level-1
                            addnode(tmpdict)

                        # 添加连接关系
                        edgeinfo={
                            'sourcenode': res3_params['id'],
                            'destinationnode': tmpdict['nodeid']
                        }
                        print('开始添加edge')
                        addedges(edgeinfo)
                        # 修改标记，记录为已经建立连接关系
                        print('结束添加 edge')
                        x['check']=True

        i+=1
        if i > len(message['allNodeinfo']):
            return
        #递归
        print('开始递归，次数')
        getnodeinfo()


    # 获取前置参数 random为13位时间戳
    res1 = s.get("https://capi.tianyancha.com/cloud-equity-provider/v4/qq/name.json?id={}?random={}".format(id, str(
        int(time.time() * 1000))), headers=headers)
    data_dict = json.loads(res1.content)["data"]
    #print(data_dict.get('v'))

    # 调用加密函数,获取cloud_token 以及cloud_utm
    fnstr = getfnstr(data_dict.get('v'))
    #print(fnstr)
    cookie_token = re.search('cookie=\'cloud_token\=(.*?)\;', fnstr).group(1)
    wtf_return = re.search('return\'(.*?)\'', fnstr).group(1)
    window_sogo = getSogo(default_list, id)
    # cloud_utm
    fxckStr = getfxckStr(wtf_return, window_sogo)
    headers["Cookie"] = headers["Cookie"] + " cloud_utm=" + fxckStr + "; cloud_token=" + cookie_token + ';'
    #print(headers["Cookie"])
    # 请求indexNode
    res2 = s.get('https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id={}'.format(id),
                 headers=headers)
    text = json.loads(res2.text)
    message={
        "allNodeinfo":[],
        "edges":[]
    }


    for holder in text['data']['holderList']:
        tmpdict={
            "name" : holder['name'],
            "percent" : holder['percent'],
            "nodeid" : holder['id'],
            "hasnode": holder['hasNode'],
            "level": 1,
            "check": False
        }
        addnode(tmpdict)


    level = 1
    # 递归参数
    i = len(message['allNodeinfo'])
    # 一级股东确认后，紧接着确认二级股东
    getnodeinfo()

    print(message)
    s.close()
    return message


def getCompanyId(keyword):
    s=requests.session()
    #keyword= '百度'
    startUrl = 'https://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % urllib.parse.quote(keyword)
    #print(startUrl)
    resultPage = s.get(startUrl,verify=False,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"},cookies=Cookies)
    soup = BeautifulSoup(resultPage.text,'lxml')
    #rint(soup)
    cmplist=soup.select('.result-list > .search-item > .search-result-single   > .content > .header > .name')
    cmpid_name=[]
    for each in cmplist:
        cmpid_name.append((each.get('href')[35::],each.get_text()))
    s.close()
    dict_cmp = {value: key for key, value in cmpid_name}

    return dict_cmp

def write2excel2(message,excel_sheet_name):
    excel_info=[(x['name'],x['level'],x['percent']) for x in message['allNodeinfo']]
    #print(excel_info)
    # 定义excel的表头
    excel_header = ['企业名', '级别', '持股百分比']
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    sheet = book.add_sheet(excel_sheet_name,
                           cell_overwrite_ok=True)  # # 其中第一个参数是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False

    # 设置excel 表头
    i = 0  # 表头从第0行开始
    for k in excel_header:
        sheet.write(0, i, k)
        i += 1
    #获取数据
    row = 1  # 数据内容从第一行开始

    for company in excel_info:
        # 数据写入excel
        m = 0  # 从第0列开始

        for column in company:
            sheet.write(row, m, column)
            m += 1
        # 行 + 1，进入下一行
        row += 1
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'static/file/' + excel_sheet_name + '.xls')
        book.save(file_path)
        print('生成成功,文件路径为:',file_path)
        return excel_sheet_name+'.xls'
    except Exception:
        print('文件生成失败')
        return False

class IndexHandler(tornado.web.RequestHandler):
    def post(self):

        keyword=self.get_argument('keyword')
        cp=getCompanyId(keyword)
        result=[x for x in cp]
        result_of_cmp=[{"name": y } for y in result]
        self.write(json.dumps(result_of_cmp))
        # if keyword in result:
        #     message=getCompanyInfo(cp[keyword])
        #     self.write(json.dumps(message["allNodeinfo"]))
        # else:
        #     self.write(json.dumps(result_of_cmp))

class DaochuHandler(tornado.web.RequestHandler):
    def post(self):

        cmp_name=self.get_argument("cmp_full_name")
        cp=getCompanyId(cmp_name)
        message = getCompanyInfo(cp[cmp_name])
        file_path=write2excel2(message, cp[cmp_name])
        self.write('http://localhost:8888/static/file/'+file_path)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',IndexHandler),
            (r'/export', DaochuHandler),
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static')
        }

        super(Application, self).__init__(handlers, **settings, debug=True)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
