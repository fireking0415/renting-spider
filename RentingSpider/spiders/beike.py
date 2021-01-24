import scrapy

from ..items import RentingspiderItem


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['ke.com/']
    start_urls = ['http://sh.zu.ke.com/zufang/pg2/']

    def parse(self, response):
        renting_item = RentingspiderItem()
        page_result_list = response.xpath("//div[@class='content__list--item']")
        for item in page_result_list:

            title = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--title']/a[@class='twoline']/text()").extract_first()

            if title != None:
                title = title.strip()
                renting_item['title'] = title

            city_info_array = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--des']/a/text()").extract()

            if len(city_info_array) >= 1:
                renting_item['area_city_region'] = city_info_array[0]

            if len(city_info_array) >= 2:
                renting_item['area_city_community'] = city_info_array[1]

            if len(city_info_array) >= 3:
                renting_item['area_city_street'] = city_info_array[2]

            renting_item['cover'] = item.xpath("./a[@class='content__list--item--aside']/img/@src").extract()

            renting_item['rent'] = "" + item.xpath(
                "./div[@class='content__list--item--main']/span[@class='content__list--item-price']/em/text()").extract_first() + item.xpath(
                "./div[@class='content__list--item--main']/span[@class='content__list--item-price']/text()").extract_first()

            desc_array = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--des']/text()").extract()

            if len(desc_array) >= 1:
                house_type = ""
                for i in desc_array:
                    house_type += i
                house_type = house_type.replace(' ', '').replace('--', '')
                house_type = house_type.replace('\n', ' ')
                renting_item['house_type'] = house_type.strip()

            renting_item['platform'] = "贝壳"

            renting_item['tags'] = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--bottom oneline']/i/text()").extract()

            source = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--brand oneline']/span[@class='brand']/text()").extract()
            if len(source) >= 1:
                renting_item['source'] = source[0].strip()

            update_time = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--brand oneline']/span[@class='content__list--item--time oneline']/text()").extract()

            if len(update_time) >= 1:
                renting_item['updateTime'] = update_time[0].strip()

            yield renting_item
