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
from os import path
from datetime import datetime


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
        self.上一次时间戳, self.上一次剩余听歌量 = self.读取配置文件方法()
        self.当前时间戳 = self.获取当前时间戳方法()
        self.当前剩余听歌量 = self.获取当前剩余听歌量方法()

        if self.上一次时间戳 == '暂无记录':
            print('暂无上次打开的记录')
        else:
            print(f'上次打开的记录: {self.转成格式化时间方法(self.上一次时间戳)} 还需:{self.上一次剩余听歌量}')

        print(self.转成格式化时间方法(self.当前时间戳) + " 距离升级还需听{}首歌".format(self.当前剩余听歌量))
        self.预测听完天数方法()
        self.获取音乐单方法()

    def 获取当前剩余听歌量方法(self) -> int:
        链接 = "https://music.163.com/weapi/user/level"
        会话结果 = self.会话.post(url=链接, data=self.等级登录信息, headers=self.等级账号信息)

        等级信息 = json.loads(会话结果.text)['data']
        听歌量 = 等级信息["nextPlayCount"] - 等级信息["nowPlayCount"]

        self.保存数据至配置文件方法(听歌量)
        return 听歌量

    def 读取配置文件方法(self) -> tuple:
        if not path.exists('config.config'):
            文件 = open('config.config', 'w', encoding='utf-8')
            文件.close()
            return '暂无记录', ''

        with open('config.config', 'r', encoding='utf-8') as 文件:
            内容 = 文件.read()
            if 内容 != '':
                内容 = 内容.split(' ')
                return int(内容[0]), int(内容[1])

        return '暂无记录', ''

    def 保存数据至配置文件方法(self, 听歌量: int) -> None:
        with open('config.config', 'w', encoding='utf-8') as 文件:
            文件.write(str(self.获取当前时间戳方法()) + ' ' + str(听歌量))

    def 获取当前时间戳方法(self) -> int:
        return int(datetime.now().timestamp())

    def 转成格式化时间方法(self, 时间戳: int) -> str:
        return datetime.fromtimestamp(时间戳).strftime('%Y-%m-%d %H:%M:%S')

    def 获取音乐单方法(self) -> None:
        链接 = "https://music.163.com/weapi/v1/play/record"
        会话结果 = self.会话.post(url=链接, data=self.登录信息, headers=self.账号信息)

        音乐单信息 = json.loads(会话结果.text)

        self.输出听歌榜单方法(音乐单信息['weekData'], '每周')
        self.输出听歌榜单方法(音乐单信息['allData'], '全部')

    def 输出听歌榜单方法(self, 数据: list, 类型: str, 数量=10) -> None:
        if self.榜单数量 > len(数据):
            self.榜单数量 = len(数据)

        print(('\n每周听歌量前' if 类型 == '每周' else '\n全部听歌量前') + str(self.榜单数量))
        for i in range(0, self.榜单数量):
            音乐信息 = 数据[i]
            print('第{}名: {}  听歌次数:{}次'.format(str(i + 1), 音乐信息['song']['name'], 音乐信息['playCount']))

    def 预测听完天数方法(self) -> None:
        try:
            每天减少的听歌量 = 86400 / (
                    (self.当前时间戳 - self.上一次时间戳) / (self.上一次剩余听歌量 - self.当前剩余听歌量))
            每天减少的听歌量 = 每天减少的听歌量 if 每天减少的听歌量 <= 300 else 300
            print(f'预计还需{int(self.当前剩余听歌量 / 每天减少的听歌量)}天听完')
        except:
            print('间隔时间过小，无法预测剩余听完的时间')

网易云类()
