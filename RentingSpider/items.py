# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentingspiderItem(scrapy.Item):
    # define the fields for your item here like:

    # 房租信息总概描述title
    title = scrapy.Field()
    # //div/p/a[@class='twoline']

    # 租房信息URL地址
    house_net_url = scrapy.Field()

    # 小区全路径
    city_street_full_name = scrapy.Field()

    # 一级区域
    area_city_region = scrapy.Field()
    # //div[@class='content__list--item--main']/p[@class='content__list--item--des']

    # 二级区域
    area_city_community = scrapy.Field()

    # 小区名称
    area_city_street = scrapy.Field()

    # 房屋封面
    cover = scrapy.Field()
    # //a[@class='content__list--item--aside']/img/@src

    # 租金金额
    rent = scrapy.Field()
    # //span[@class='content__list--item-price']

    # 租金单位
    rent_unit = scrapy.Field()

    # 房屋户型
    house_type = scrapy.Field()

    # 房租来源
    source = scrapy.Field()
    # //div[@class='content__list--item--main']/p[@class='content__list--item--brand oneline']/span[@class='brand']

    # 平台
    platform = scrapy.Field()

    # 房屋标签
    tags = scrapy.Field()
    # //p[@class='content__list--item--bottom oneline']

    # 更新时间
    update_time = scrapy.Field()

    # 更新时间-用于排序,将moment时间展示格式转换为可排序类型
    """
    排序方式为：
    今天-10
    xx天前-100 + xx
    xx月前-1000 + xx
    xx年前-10000 + xx
    """
    update_time_sortable = scrapy.Field()

    pass
