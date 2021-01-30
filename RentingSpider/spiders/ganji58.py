import scrapy

from RentingSpider.items import RentingspiderItem


class Ganji58Spider(scrapy.Spider):
    name = 'ganji58'
    allowed_domains = ['sh.58.com/chuzu/pn1/']
    start_urls = ['http://sh.58.com/chuzu/pn1/']

    def parse(self, response, **kwargs):
        renting_item = RentingspiderItem()
        house_list = response.xpath("//ul[@class='house-list']/li[@class='house-cell']")
        for house_item in house_list:
            renting_item['cover'] = house_item.xpath("./div[@class='img-list']/a/img/@lazy_src").extract_first()
            title = house_item.xpath(
                "./div[@class='des']/h2/a[@class='strongbox']/text()").extract_first()
            title = title.replace(" ", "")
            renting_item['title'] = title.strip()
            renting_item['house_net_url'] = house_item.xpath(
                "./div[@class='des']/h2/a[@class='strongbox']/@href").extract_first()
            renting_item['rent'] = int(house_item.xpath(
                "./div[@class='list-li-right']/div[@class='money']/b[@class='strongbox']/text()").extract_first())
            renting_item['rent_unit'] = "元/月"
            renting_item['platform'] = '58ganji'
            renting_item['source'] = house_item.xpath(
                "./div[@class='des']/div[@class='jjr']/span/span/@title").extract_first()
            location_list = house_item.xpath("./div[@class='des']/p[@class='infor']/a/text()").extract()
            if len(location_list) == 1:
                renting_item['area_city_community'] = location_list[0]
            elif len(location_list) > 1:
                renting_item['area_city_community'] = location_list[0]
                renting_item['area_city_street'] = location_list[1]
            house_type = house_item.xpath("./div[@class='des']/p/text()").extract_first()
            house_type = house_type.strip().replace(" ", "")
            renting_item['house_type'] = house_type
            house_address_list = house_item.xpath("./div[@class='des']/p/text()").extract()
            house_address = ''
            if len(house_address_list) > 1:
                house_address = house_address_list[len(house_address_list) - 1].strip()
            renting_item['city_street_full_name'] = renting_item['area_city_community'] + "-" + renting_item[
                'area_city_street'] + "-" + house_address
            yield renting_item

        a_next = response.xpath("//div[@class='pager']/a[@class='next']")
        if a_next is not None:
            next_url = a_next.xpath("./@href").extract_first()
            yield scrapy.Request(url=next_url, callback=self.parse, method="GET", dont_filter=True)
