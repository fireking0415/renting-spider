import scrapy


class WoaiwojiaSpider(scrapy.Spider):
    name = 'woaiwojia'
    allowed_domains = ['sh.5i5j.com/zufang']
    start_urls = ['http://sh.5i5j.com/zufang/']

    def parse(self, response, **kwargs):
        p_list = response.xpath("//div[@class='list-con-box']/ul[@class='pList']/li")
        for item in p_list:
            print(item.xpath("./div[@class='listImg']/a/img/@src").extract_first())
        pass
