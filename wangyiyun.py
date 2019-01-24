# coding=utf-8
from lxml import etree
import requests
import re
import json
from tools_wyy import MongoHelper

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
        self.mongo_db = MongoHelper(db="wangyiyun", collection="wyy")

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_song_sheet(self, html_str):
        html_str_etree = etree.HTML(html_str)
        item = {}
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
        song_name_tmp = html_str_etree.xpath("//ul[@class='f-hide']/li/a/text()")
        song_name_tmp = [re.sub(r'\xa0', ' ', i).strip() for i in song_name_tmp]  # 替换里面的不间断字符(\xa0):&nbsp,空格：\x20
        song_name_tmp = [re.sub(r'\.', ' ', i) for i in song_name_tmp]  # 替换里面的"."为空格字符 因为mongo不支持键含有点(.)
        song_href_tmp = html_str_etree.xpath("//ul[@class='f-hide']/li/a/@href")  # https://music.163.com
        song_href_tmp = ["https://music.163.com" + i for i in song_href_tmp]
        song_list = {i: song_href_tmp[song_name_tmp.index(i)] for i in song_name_tmp}
        item['歌单表'] = song_list
        # print(type(html_str_etree))
        # print(etree.tostring(html_str_etree.xpath("//ul[@class='f-hide']/li/a")[-13],encoding='utf-8').decode())
        # item['歌单链接'] = ["https://music.163.com" + i for i in item['歌单链接']]
        item['歌单标签'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/i/text()")
        item['歌单标签链接'] = html_str_etree.xpath("//div[@class='tags f-cb']/a/@href")
        item['收藏数'] = html_str_etree.xpath("//a[@class='u-btni u-btni-fav ']/@data-count")[0]
        item['播放数'] = html_str_etree.xpath("//strong[@id='play-count']/text()")[0]
        item['script_detail'] = html_str_etree.xpath("//script[@type='application/ld+json']/text()")[0]

        ret = re.findall(r'.*<span id="cnt_comment_count">(\d+)</span>.*', html_str, re.S)
        # print(ret)
        # print(song_list)
        # print(item['script_detail'])
        tmp2 = item['script_detail']
        # print(str(tmp2))
        tmp2_dict = json.loads(tmp2)
        return item

    def save_json_data(self, json_data):
        with open("1.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=0, indent=2))

    def save_json_to_db(self, json_data):
        self.mongo_db.insert_one(json_data)
        print("保存完毕")

    def db_find(self):
        self.mongo_db.find()

    def run(self):
        html_str = self.parse_url(self.url)
        song_sheet = self.get_song_sheet(html_str)
        print(song_sheet)
        # self.save_json_data(song_sheet)
        self.save_json_to_db(song_sheet)


if __name__ == '__main__':
    wyy = WyySpider()
    # wyy.run()

    # wyy.save_json_to_db(data)
    wyy.db_find()