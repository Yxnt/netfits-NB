#!/usr/bin/env python3
import requests
import logging
import re

FORMAT = logging.Formatter('%(asctime)-15s %(levelno)s %(message)s')
logger = logging.getLogger()
filehandler = logging.FileHandler('yunqiang.log', encoding='utf-8')
filehandler.setFormatter(FORMAT)
logger.addHandler(filehandler)
logger.setLevel(logging.INFO)


class common(object):
    openid = ''
    header = {}
    status = 0

    def __init__(self, id):
        self.id = id

    def post(self, url, headers, body):
        response = requests.post(url, params=body, headers=headers).json()
        return response

    def loginfo(self, msg):
        logger.info(msg)


class wechat(common):
    openid = ''
    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.8 NetType/WIFI Language/zh_CN'
    }
    body = {
        'openid': openid,
    }

    def __cid(self):
        self.loginfo("====微信开始====")
        url = 'https://reg.netpas.com.cn/weixin/api/bind.htm'
        self.body['gear_id'] = self.id
        response = self.post(url, body=self.body, headers=self.header)
        if response['status'] == 0:
            msg = "设备ID：{ID}绑定成功".format(ID=self.id)
            self.status = 1
            self.loginfo(msg)
            print(msg)

        else:
            msg = "设备ID：{ID}绑定失败".format(ID=self.id)
            self.status = 0
            self.loginfo(msg)
            print(msg)

    def __yj(self):
        self.body['task'] = 12
        url = 'https://reg.netpas.com.cn/weixin/shark-ajax.htm'
        response = self.post(url, body=self.body, headers=self.header)
        if response['status'] == 0:
            '''返回摇奖成功获取的nb数量'''
            msg = "设备ID：{ID} 获取NB数量为{NB}".format(ID=self.id, NB=response['nb'])
            self.loginfo(msg)
            print(msg)
        elif response['status'] == 3:
            time = re.match(r'.*(\d{1,2}:\d{1,2}:\d{1,2}).*', response['error']).group(1)
            msg = "设备ID：{ID}摇奖失败，等待时间{TIME}后尝试".format(ID=self.id, TIME=time)
            self.loginfo(msg)
            print(msg)

        self.loginfo("====微信结束====")

    def run(self):

        self.__cid()
        if self.status == 0:
            self.__yj()


class weibo(common):
    openid = ''

    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.8 NetType/WIFI Language/zh_CN'
    }
    body = {
        'openid': openid
    }

    def __cid(self):
        self.loginfo("====微博开始====")
        url = 'https://reg.netpas.com.cn/weibo/api/bind.htm'
        self.body['gear_id'] = self.id

        response = self.post(url, body=self.body, headers=self.header)

        if response['status'] == 0:
            msg = "设备ID：{ID}绑定成功".format(ID=self.id)
            self.status = 1
            self.loginfo(msg)
            print(msg)

        else:
            msg = "设备ID：{ID}绑定失败".format(ID=self.id)
            self.status = 0
            self.loginfo(msg)
            print(msg)

    def __yj(self):
        self.body['task'] = 13
        url = 'https://reg.netpas.com.cn/weibo/shark-ajax.htm'

        response = self.post(url, body=self.body, headers=self.header)
        if response['status'] == 0:
            '''返回摇奖成功获取的nb数量'''
            msg = "设备ID：{ID} 获取NB数量为{NB}".format(ID=self.id, NB=response['nb'])
            self.loginfo(msg)
            print(msg)
        elif response['status'] == 3:
            time = re.match(r'.*(\d{1,2}:\d{1,2}:\d{1,2}).*', response['error']).group(1)
            msg = "设备ID：{ID}摇奖失败，等待时间{TIME}后尝试".format(ID=self.id, TIME=time)
            self.loginfo(msg)
            print(msg)
        self.loginfo("====微博结束====")

    def run(self):
        if self.status == 0:
            self.__yj()


def main():
    with open('yunqiang.cfg', 'r') as f:
        for i in f:
            ID = i.strip()
            wx = wechat(ID)
            wx.run()
            wb = weibo(ID)
            wb.run()


if __name__ == '__main__':
    main()
