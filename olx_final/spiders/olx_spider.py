from scrapy.spiders import Spider
from scrapy import Selector
from olx_final.items import OlxItem
import scrapy



class MySpider(Spider):
    name = "olx"
    allowed_domains = ["olx.co.ke"]
    start_urls = ["https://www.olx.co.ke/electronics-video/?page=%s" % page for page in xrange(1,100)]
    # start_urls = ["https://www.olx.co.ke/electronics-video/"]

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//table/tbody/tr/td[@class='offer ']")
        items = []
        for titles in titles:
            item = OlxItem()
            item["summary"] = titles.xpath('table/@summary').extract()
            item["image"] = titles.xpath('table/tbody/tr/td/a/img/@src').extract()
            link = titles.xpath('table/tbody/tr/td/a/@href').extract()
            item['link'] = titles.xpath('table/tbody/tr/td/a/@href').extract()
            item["name"] = titles.xpath('table/tbody/tr/td/a/img/@alt').extract()
            item["category"] = titles.xpath('normalize-space(table/tbody/tr/td/div/p[@class="color-9 lheight16 margintop5"]/small/text())').extract()
            item["cost"] = titles.xpath('table/tbody/tr/td/div/p[@class="price"]/strong/text()').extract()
            item["cost_terms"] = titles.xpath('table/tbody/tr/td/div/span/text()').extract()
            item["created"] = titles.xpath('normalize-space(table/tbody/tr/td/div/p[@class="color-9 lheight16 marginbott5 x-normal"]/text())').extract()
            item["location"] = titles.xpath('normalize-space(table/tbody/tr/td/div/p/small/span/text())').extract()
            request = scrapy.Request(link[0], callback=self.parse_dir_contents)
            request.meta['item'] = item
            items.append(request)
        return items

    def parse_dir_contents(self, response):
        hxs = Selector(response)
        item = response.meta['item']
        item['desc'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/div/div/p/text())').extract()
        item['name2'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/h1/text())').extract()
        item['location2'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/p/span/span/strong/text())').extract()
        item['created2'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/p/small/span/text())').extract()
        item['user_type'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/div/table/tr/td/table/tr/td/strong/a/text())').extract()
        item['user'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/div/p/span[@class="block color-5 brkword xx-large"]/text())').extract()
        item['user_since'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/div/p/span[@class="block color-5 normal margintop5 sinceline"]/text())').extract()
        item['users_products_link'] = hxs.xpath('normalize-space(.//body/div/section/div/div/div/div/div/div/div/p/span/a/@href)').extract()
        return item