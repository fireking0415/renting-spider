import scrapy

from ..items import RentingspiderItem


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['ke.com/']
    current_page_no = 1
    start_urls = ['http://sh.zu.ke.com/zufang/pg1/']
    page_total_size = -1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = 'http://sh.zu.ke.com'

    def parse(self, response, **kwargs):
        renting_item = RentingspiderItem()
        page_result_list = response.xpath("//div[@class='content__list--item']")
        for item in page_result_list:

            title = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--title']/a[@class='twoline']/text()").extract_first()

            if title != None:
                title = title.strip()
                renting_item['title'] = title

            renting_item['house_net_url'] = self.base_url + item.xpath(
                "./a[@class='content__list--item--aside']/@href").extract_first().strip()

            city_info_array = item.xpath(
                "./div[@class='content__list--item--main']/p[@class='content__list--item--des']/a/text()").extract()

            street_full_name = '-'.join(city_info_array)
            renting_item['city_street_full_name'] = street_full_name

            if len(city_info_array) >= 1:
                renting_item['area_city_region'] = city_info_array[0]

            if len(city_info_array) >= 2:
                renting_item['area_city_community'] = city_info_array[1]

            if len(city_info_array) >= 3:
                renting_item['area_city_street'] = city_info_array[2]

            renting_item['cover'] = item.xpath("./a[@class='content__list--item--aside']/img/@src").extract()

            rent_str = item.xpath(
                "./div[@class='content__list--item--main']/span[@class='content__list--item-price']/em/text()").extract_first().strip()
            rent_str = rent_str.replace(' ', '')
            if rent_str.find("-") > 0:
                renting_item['rent'] = int(rent_str.split('-')[1])
            else:
                renting_item['rent'] = int(rent_str)

            renting_item['rent_unit'] = item.xpath(
                "./div[@class='content__list--item--main']/span[@class='content__list--item-price']/text()").extract_first().strip()

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
                renting_item['update_time'] = update_time[0].strip()
                renting_item['update_time_sortable'] = self._cal_update_time_sortable(update_time[0].strip())

            yield renting_item

        self.current_page_no += 1
        if self.page_total_size == -1:
            self.page_total_size = int(response.xpath(
                "//div[@class='content__pg']/@data-totalpage").extract_first())

        if self.current_page_no <= self.page_total_size:
            next_url = 'http://sh.zu.ke.com/zufang/pg{}/'.format(str(self.current_page_no))
            # 准备抓取下一页数据
            yield scrapy.Request(url=next_url, callback=self.parse, method="GET", dont_filter=True)

    @staticmethod
    def _cal_update_time_sortable(update_time_str):
        """
        根据moment格式的字符串展示，转换为一个可排序的字段
        :return: 排序字段、根据时间变化、时间越旧，数字越大
        """
        if update_time_str.find('天前') > 0:
            return 100 + int(update_time_str.split('天前')[0])
        elif update_time_str.find('个月前') > 0:
            return 1000 + int(update_time_str.split('个月前')[0])
        elif update_time_str.find('年前') > 0:
            return 10000 + int(update_time_str.split('年前')[0])
        else:
            return 10
