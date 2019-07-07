# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class ZhihuItem(scrapy.Item):
    id = Field()
    url_token = Field()
    name = Field()
    use_default_avatar = Field()
    avatar_url = Field()
    avatar__template = Field()
    is_org = Field()
    type = Field()
    url = Field()
    user_type = Field()
    headline = Field()
    gender = Field()
    is_advertiser = Field()
    vip_info = Field()
    badge = Field()
    allow_message = Field()
    is_following = Field()
    is_followed = Field()
    is_blocking = Field()
    follower_count = Field()
    answer_count = Field()
    articles_count = Field()
    employments = Field()
