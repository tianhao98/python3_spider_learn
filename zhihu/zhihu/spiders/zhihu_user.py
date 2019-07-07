# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from zhihu.items import ZhihuItem
import json

class ZhihuUserSpider(scrapy.Spider):
    name = 'zhihu_user'
    allowed_domains = ['www.zhihu.com']
    user = 'Talyer-Wei'
    # start_urls = ['http://www.zhihu.com/']

    # 用户信息
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 关注列表信息
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}'
    follows_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit={limit}'

    # 分析列表信息
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit={limit}'

    # 开始请求一个用户，解析他的用户信息
    def start_requests(self):
        yield Request(url=self.user_url.format(user=self.user, include=self.user_include), callback=self.user_parse)

    # 解析用户信息，根据url_token调用用户的关注列表
    def user_parse(self, response):
        user_item = ZhihuItem()
        results = json.loads(response.text)
        for field in user_item.fields:
            if field in results.keys():
                user_item[field] = results.get(field)
        yield user_item

        # 开始解析用户所有关注列表用户，粉丝列表
        yield Request(url=self.follows_url.format(user=results.get('url_token'), include=self.follows_include, limit=20, offset=0), callback=self.follow_parse)
        yield Request(url=self.followers_url.format(user=results.get('url_token'), include=self.followers_include, limit=20, offset=0), callback=self.followers_parse)


    # 获取关注列表用户，根据列表解析每个用户信息
    def follow_parse(self, response):
        self.apiurl = 'https://www.zhihu.com/api/v4'
        results = json.loads(response.text)

        # 获取的所有关注用户，回调解析用户信息函数
        for user in results.get('data'):
            yield Request(url=self.user_url.format(user=user.get('url_token'), include=self.user_include), callback=self.user_parse)

        # 判断是否最后一页，不是的话继续回调解析下一项关注页面用户
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_url = results.get('paging').get('next')
            yield Request(url=self.apiurl+next_url.split('https://www.zhihu.com')[1], callback=self.follow_parse)

    # 获取粉丝列表用户，根据列表解析遍历每个用户信息
    def followers_parse(self, resppnse):
        self.apiurl = 'https://www.zhihu.com/api/v4'
        results = json.loads(resppnse.text)

        # 获取的所有粉丝用户，回调解析用户信息函数
        for user in results.get('data'):
            yield Request(url=self.user_url.format(user=user.get('url_token'), include=self.user_include), callback=self.user_parse)

        # 判断是否最后一页，不是的话继续回调解析下一项关注页面用户
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_url = results.get('paging').get('next')
            yield Request(url=self.apiurl+next_url.split('https://www.zhihu.com')[1], callback=self.followers_parse)

