# NetEaseCloudMusicInfoGet
获取网易云音乐升级剩余听歌量，每周听歌量排名，全部听歌量排名
使用中文变量名

在浏览器， 你的主页，开f12， 查看网络并刷新页面，找到record?csrf_token=xxxxxxx
之后复制该请求的cookie到 [self.主页Cookie]
再点击载荷，查看这个请求post的数据，复制到[self.登录信息]

第二个是访问https://music.163.com/#/user/level
开f12， 查看网络并刷新页面，找到level?csrf_token=xxxxxxx
复制该请求的cookie到 [等级Cookie]
再点击载荷，查看这个请求post的数据，复制到[self.等级登录信息]

[self.榜单数量] 可自定义，最高100
