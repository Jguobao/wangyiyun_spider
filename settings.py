#coding=utf-8

class Settings:
    """初始化网易云爬虫设置的类"""

    def __init__(self):
        self.start_url = ""
        # 某类歌单页url 此示例为华语热门歌单页
        self.song_sheets_start_page = "https://music.163.com/discover/playlist/?order=hot&cat=华语&offset=0"
        self.song_sheets_format_page = "https://music.163.com/discover/playlist/?order=hot&cat=华语&offset={}"
        # 一个歌单的url
        self.url = "https://music.163.com/playlist?id=2498061427"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}