# coding=utf-8
from parse_url import parse_url
from lxml import etree
import requests
import re
'''
url="https://music.163.com/playlist?id=2584113381"
html_str = parse_url(url)
html_str_etree = etree.HTML(html_str)
li_list_etree = html_str_etree.xpath("//ul[@class='f-hide']/li/a/text()")
with open('2.html','w',encoding='utf-8') as f:
    f.write(html_str)
'''


class WyySpider:
    def __init__(self):
        self.start_url = ""
        self.url = "https://music.163.com/playlist?id=2498061427"  # 一个歌单的url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_song_sheet(self, html_str):
        html_str_etree = etree.HTML(html_str)
        item={}
        # item['song_sheet_description'] = html_str_etree.xpath("//meta[@name='description']/@content")[0]
        # item['song_sheet_num'] = html_str_etree.xpath("//span[@id='playlist-track-count']/text()")[0]
        # item['song_sheet'] = html_str_etree.xpath("//ul[@class='f-hide']/li/a/text()")
        # item['song_sheet_href'] = html_str_etree.xpath("//ul[@class='f-hide']/li/a/@href")[0]
        # item['song_sheet_tags'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/i/text()")[0]
        # item['song_sheet_tags_href'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/@href")[0]
        # item['song_sheet_save_num'] = html_str_etree.xpath("//a[@class='u-btni u-btni-fav ']/@data-count")[0]
        # item['song_sheet_play_num'] = html_str_etree.xpath("//strong[@id='play-count']/text()")[0]
        item['歌单描述'] = html_str_etree.xpath("//meta[@name='description']/@content")[0]
        item['作者'] = html_str_etree.xpath("//a[@class='u-btni u-btni-share ']/@data-res-author")[0]
        item['歌曲数量'] = html_str_etree.xpath("//span[@id='playlist-track-count']/text()")[0]
        item['歌单表'] = html_str_etree.xpath("//ul[@class='f-hide']/li/a/text()")
        item['歌单链接'] = html_str_etree.xpath("//ul[@class='f-hide']/li/a/@href")
        item['歌单标签'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/i/text()")[0]
        item['歌单标签链接'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/@href")[0]
        item['收藏数'] = html_str_etree.xpath("//a[@class='u-btni u-btni-fav ']/@data-count")[0]
        item['播放数'] = html_str_etree.xpath("//strong[@id='play-count']/text()")[0]
        item['script_detail']= html_str_etree.xpath("//script[@type='application/ld+json']/text()")[0]
        song_list = {i: item['歌单链接'][item['歌单表'].index(i)] for i in item['歌单表']}
        ret = re.findall(r'.*<span id="cnt_comment_count">(\d+)</span>.*', html_str, re.S)
        #print(ret)
        print(song_list)
        print(item['script_detail'])

        print(item)
    def run(self):
        html_str = self.parse_url(self.url)
        song_sheet = self.get_song_sheet(html_str)

if __name__ == '__main__':
    wyy = WyySpider()
    wyy.run()
