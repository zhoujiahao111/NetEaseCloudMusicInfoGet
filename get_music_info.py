# coding=utf-8
'''
在浏览器， 你的主页，开f12， 查看网络并刷新页面，找到record?csrf_token=xxxxxxx
之后复制该请求的cookie到 [self.主页Cookie]
再点击载荷，查看这个请求post的数据，复制到[self.登录信息]

第二个是访问https://music.163.com/#/user/level
开f12， 查看网络并刷新页面，找到level?csrf_token=xxxxxxx
复制该请求的cookie到 [等级Cookie]
再点击载荷，查看这个请求post的数据，复制到[self.等级登录信息]

[self.榜单数量] 可自定义，最高100
'''

import requests
import json


class 网易云类:
    def __init__(self):
        self.主页Cookie = ''
        self.等级Cookie = ''
        self.登录信息 = {
            'params': '',
            'encSecKey': ''}
        self.等级登录信息 = {
            'params': '',
            "encSecKey": ""}
        self.榜单数量 = 10

        self.会话 = requests.Session()
        self.账号信息 = {'Content-Type': 'application/x-www-form-urlencoded',
                         'Cookie': self.主页Cookie, 'Origin': 'https://music.163.com',
                         'Referer': 'https://music.163.com/user/songs/rank?id=367831881',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'}

        self.等级账号信息 = {'Content-Type': 'application/x-www-form-urlencoded',
                             'Cookie': self.等级Cookie, 'Origin': 'https://music.163.com',
                             'Referer': 'https://music.163.com/user/level',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'}

        self.获取等级方法()
        self.获取音乐单方法()

    def 获取等级方法(self):
        链接 = "https://music.163.com/weapi/user/level"
        会话结果 = self.会话。post(url=链接, data=self.等级登录信息, headers=self.等级账号信息)

        等级信息 = json.loads(会话结果.text)['data']
        print("距离升级还需听{}首歌"。format(等级信息["nextPlayCount"] - 等级信息["nowPlayCount"]))

    def 获取音乐单方法(self):
        链接 = "https://music.163.com/weapi/v1/play/record"
        会话结果 = self.会话。post(url=链接, data=self.登录信息, headers=self.账号信息)

        音乐单信息 = json.loads(会话结果.text)

        self.获取听歌榜单方法(音乐单信息['weekData']， '每周')
        self.获取听歌榜单方法(音乐单信息['allData']， '全部')

    def 获取听歌榜单方法(self, 数据: list, 类型):
        if self.榜单数量 > len(数据):
            self.榜单数量 = len(数据)

        print(('\n每周听歌量前' if 类型 == '每周' else '\n全部听歌量前') + str(self.榜单数量))
        for i in range(0， self.榜单数量):
            音乐信息 = 数据[i]
            print('第{}名: {}  听歌次数:{}次'。format(str(i + 1), 音乐信息['song']['name'], 音乐信息['playCount']))


网易云类()
