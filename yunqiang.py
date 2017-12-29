#!/usr/bin/env python3
import os
import requests
import re
import pickle



class wechat():
    openid = ''
    headers = {"Content-Type": "application/json",
               "User-Agent": "Netpas/2.6.1 iPhone9,1/11.1.2 [cc.netpas.ios-connector]"}
    body = {
        'openid': openid,
    }

    def post(self, url, headers, body):
        response = requests.post(url, params=body, headers=headers).json()
        return response

    def __cid(self, id):
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
            print(msg)

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


if __name__ == '__main__':

    wechat().run()
