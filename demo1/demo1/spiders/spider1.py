# -*- coding: utf-8 -*-
import scrapy

import json
import requests
import re
from demo1.items import Demo1Item


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['nces.com.cn']
    # start_urls = ['http://www.nces.com.cn/servlet/Servlet']

    def start_requests(self):
        url = 'http://www.nces.com.cn/servlet/Servlet'
        # 向队列中加入post请求
        for x in range(1,1858):

            yield scrapy.FormRequest(
                url=url,
                formdata={
                    'cls': 'article',
                    'act': 'listDiaryByUsertypeTeamid',
                    'dd': '1579166529447',
                    'cp': str(x),
                    'ipp': '18',
                    'usertype': "'学生'",
                    'teamid': '1'
                },
                callback=self.parse
            )

    def parse(self, response):
        # print(response.text)
        contents = response.xpath("//content")
        # print(contents)
        # print("=" * 40)
        for content in contents:

            title = content.xpath("./title/text()").get()
            labels = content.xpath("./labels/text()").get()
            source = content.xpath("./source/text()").get()
            userid = content.xpath("./userid/text()").get()
            url = "http://www.nces.com.cn" + content.xpath("./staticfilename/text()").get()
            realname = content.xpath("./realname/text()").get()
            aliasname = content.xpath("./aliasname/text()").get()


            createTime = content.xpath("./createtime/text()").get()
            item = Demo1Item(
                title=title,
                labels=labels,
                source=source,
                userid=userid,
                url=url,
                realname=realname,
                aliasname=aliasname,
                createTime=createTime
            )

            yield scrapy.Request(url,meta={"item": item}, callback=self.get_content)
            # print({
            #     "title": title,
            #     "labels": labels,
            #     "source":source,
            #     "userid": userid,
            #     "url": url,
            #     "realname": realname,
            #     "aliasname": aliasname,
            #     "createTime": createTime
            # })

            # yield item

    def get_content(self, response):
        words = response.xpath("//div[@class='article-content']").getall()
        words = "".join(words).strip()
        words = re.sub(r"\s", "", words)
        words = re.sub(r"<.+?>", "", words)
        item = response.meta["item"]
        item["words"] = words
        print(item)
        yield item