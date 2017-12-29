#!/usr/bin/env python3
import os
import requests
import logging
import re
import pickle

FORMAT = logging.Formatter('%(asctime)-15s %(levelno)s %(message)s')
logger = logging.getLogger()
filehandler = logging.FileHandler('yunqiang.log', encoding='utf-8')
filehandler.setFormatter(FORMAT)
logger.addHandler(filehandler)
logger.setLevel(logging.INFO)


class wechat():
    openid = ''
    headers = {"Content-Type": "application/json",
               "User-Agent": "Netpas/2.6.1 iPhone9,1/11.1.2 [cc.netpas.ios-connector]"}
    body = {
        'openid': openid,
    }

    def loginfo(self, msg):
        logger.info(msg)

    def post(self, url, headers, body):
        response = requests.post(url, params=body, headers=headers).json()
        return response

    def __cid(self, id):
        self.loginfo("====微信开始====")
        url = 'https://reg.netpas.com.cn/weixin/api/bind.htm'
        self.body['gear_id'] = id
        response = self.post(url, body=self.body, headers=self.headers)
        if response['status'] == 0:
            msg = "设备ID：{ID}绑定成功".format(ID=id)
            self.status = 1
            print(msg)

        else:
            msg = "设备ID：{ID}绑定失败".format(ID=id)
            self.status = 0
            print(msg)

    def __yj(self, id):
        self.body['task'] = 12
        url = 'https://reg.netpas.com.cn/weixin/shark-ajax.htm'
        response = self.post(url, body=self.body, headers=self.headers)
        if response['status'] == 0:
            '''返回摇奖成功获取的nb数量'''
            msg = "设备ID：{ID} 获取NB数量为{NB}".format(ID=id, NB=response['nb'])

            print(msg)
        elif response['status'] == 3:
            time = re.search(r'(([01]?\d|2[0-3]):[0-5]?\d:[0-5]?\d)', response['error']).group(1)
            msg = "设备ID：{ID}摇奖失败，等待{TIME}后尝试".format(ID=id, TIME=time)
            self.loginfo(msg)
            print(msg)

        self.loginfo("====微信结束====")

    def get_nb(self):
        response = requests.post("https://api.netfits.co/ios26/info.htm",
                                 json={"gid": "37942842", "rid": "37047376"},
                                 headers=self.headers)
        return response.json()['nb']

    def run(self):
        if os.path.exists('data'):
            with open('data', 'rb') as file:
                for i in pickle.load(file):
                    self.__cid(i)
                    self.__yj(i)
            print("剩余NB数量：%d" % self.get_nb())

            return 0

        response = requests.post("https://api.netfits.co/ios26/group.htm",
                                 json={"gid": "37942842", "rid": "37047376"},
                                 headers=self.headers)
        if response.status_code == 200:
            with open('data', 'wb') as file:
                pickle.dump([i["gid"] for i in response.json()['list']], file)

            for i in response.json()['list']:
                self.__cid(i['gid'])
                self.__yj(i['gid'])
            print("剩余NB数量：%d" % self.get_nb())
            return 0


# class weibo(common):
#     openid = ''
#
#     header = {
#         'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.8 NetType/WIFI Language/zh_CN'
#     }
#     body = {
#         'openid': openid
#     }
#
#     def __cid(self):
#         self.loginfo("====微博开始====")
#         url = 'https://reg.netpas.com.cn/weibo/api/bind.htm'
#         self.body['gear_id'] = self.id
#
#         response = self.post(url, body=self.body, headers=self.header)
#
#         if response['status'] == 0:
#             msg = "设备ID：{ID}绑定成功".format(ID=self.id)
#             self.status = 1
#             self.loginfo(msg)
#             print(msg)
#
#         else:
#             msg = "设备ID：{ID}绑定失败".format(ID=self.id)
#             self.status = 0
#             self.loginfo(msg)
#             print(msg)
#
#     def __yj(self):
#         self.body['task'] = 13
#         url = 'https://reg.netpas.com.cn/weibo/shark-ajax.htm'
#
#         response = self.post(url, body=self.body, headers=self.header)
#         if response['status'] == 0:
#             '''返回摇奖成功获取的nb数量'''
#             msg = "设备ID：{ID} 获取NB数量为{NB}".format(ID=self.id, NB=response['nb'])
#             self.loginfo(msg)
#             print(msg)
#         elif response['status'] == 3:
#             time = re.match(r'.*(\d{1,2}:\d{1,2}:\d{1,2}).*', response['error']).group(1)
#             msg = "设备ID：{ID}摇奖失败，等待时间{TIME}后尝试".format(ID=self.id, TIME=time)
#             self.loginfo(msg)
#             print(msg)
#         self.loginfo("====微博结束====")
#
#     def run(self):
#         if self.status == 0:
#             self.__yj()


# def main():
#     with open('yunqiang.cfg', 'r') as f:
#         for i in f:
#             ID = i.strip()
#             wx = wechat(ID)
#             wx.run()
#             # wb = weibo(ID)
#             # wb.run()


if __name__ == '__main__':

    wechat().run()
