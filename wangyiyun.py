# coding=utf-8
from lxml import etree
import requests
import re
import json
from tools_wyy import MongoHelper
from settings import Settings


class WyySpider:
    def __init__(self):
        """初始化"""
        settings = Settings()
        self.song_sheets_start_page = settings.song_sheets_start_page
        self.song_sheets_format_page = settings.song_sheets_format_page
        self.url = settings.url
        self.headers = settings.headers
        self.mongo_db = MongoHelper(db="wangyiyun", collection="wyy")

    def parse_url(self, url):
        """解析url返回html_str"""
        response = requests.get(url, headers=self.headers)
        return response.content.decode()
    def get_sheets_page_list(self,html_start_page):
        """
        因为歌单列表页都是有规律的，所以根据此一次生成所有page页的url
        :param html_start_page:
        :return:
        """
        sheets_url_list=[]
        start_page_etree = etree.HTML(html_start_page)
        end_num = start_page_etree.xpath("//div[@id='m-pl-pager']//a[last()-1]/text()")[0]
        end_num=int(end_num)
        for n in range(1,end_num):
            n=n*35
            url = self.song_sheets_format_page.format(n)
            print(url)
            sheets_url_list.append(url)
        return sheets_url_list
    def get_sheet_list_url(self, html_str):
        """

        :param html_str: 歌单列表页的html
        :return: 返回字典的列表，
        """
        sheet_list = []
        html_str_etree = etree.HTML(html_str)
        # print(html_str)
        song_sheet_li_list = html_str_etree.xpath("//ul[@id='m-pl-container']/li")
        for li in song_sheet_li_list:
            item = {}
            item["sheet_name"] = li.xpath(".//div/a[@class='msk']/@title")[0]
            item["sheet_href"] = "https://music.163.com" + li.xpath(".//div/a[@class='msk']/@href")[0]
            item["sheet_img"] = li.xpath(".//div/img[1]/@src")[0]
            item["play_numbers"] = li.xpath(".//div/span[@class='nb']/text()")[0]
            item["author"] = li.xpath(".//a[@class='nm nm-icn f-thide s-fc3']/@title")[0]
            item["author_href"] = li.xpath(".//a[@class='nm nm-icn f-thide s-fc3']/@href")[0]
            sheet_list.append(item)
        return sheet_list

    def get_song_sheet(self, html_str):
        """获取某个歌单信息"""
        html_str_etree = etree.HTML(html_str)
        item = {}
        item['歌单描述'] = html_str_etree.xpath("//meta[@name='description']/@content")[0].strip()
        item['作者'] = html_str_etree.xpath("//a[@class='u-btni u-btni-share ']/@data-res-author")[0].strip()
        item['歌曲数量'] = html_str_etree.xpath("//span[@id='playlist-track-count']/text()")[0].strip()
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
        item['收藏数'] = html_str_etree.xpath("//a[@class='u-btni u-btni-fav ']/@data-count")[0].strip()
        item['播放数'] = html_str_etree.xpath("//strong[@id='play-count']/text()")[0].strip()
        item['script_detail'] = html_str_etree.xpath("//script[@type='application/ld+json']/text()")[0].strip()
        ret = re.findall(r'.*<span id="cnt_comment_count">(\d+)</span>.*', html_str, re.S)
        return item

    def save_json_data(self, json_data):
        """json数据存储"""
        with open("1.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=0, indent=2))
    def save_txt(self, data):
        with open("1.json","a",encoding="utf-8") as f:
            f.write(data)

    def save_json_to_db(self, json_data):
        """json数据存储到mongodb中"""
        self.mongo_db.insert_one(json_data)
        print("保存完毕")

    def db_find(self):
        """查询数据"""
        print("查询所有...")
        self.mongo_db.find()


    def run(self):
        """逻辑主函数"""
        sheet_list_html_str = self.parse_url(self.song_sheets_start_page)
        sheets_url_list = self.get_sheets_page_list(sheet_list_html_str)
        print(sheets_url_list)
        sheet_list = self.get_sheet_list_url(sheet_list_html_str)
        # for sheet in sheet_list:
        #     sheet_url = sheet["sheet_href"]
        #     html_str = self.parse_url(sheet_url)
        #     song_sheet = self.get_song_sheet(html_str)
        #     print(song_sheet)
            # self.save_json_data(song_sheet)
            # self.save_txt(",\n")
        # self.save_json_to_db(song_sheet)


if __name__ == '__main__':
    wyy = WyySpider()
    wyy.run()

    # wyy.save_json_to_db(data)
    # wyy.db_find()
