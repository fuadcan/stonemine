from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import StoneMineItem
from datetime import datetime
import pandas as pd
import re


class StonemineSpider(CrawlSpider):
    name = "stonemine"
    allowed_domains = ["alibabadogaltas.com.tr"]
    start_urls = ["https://www.alibabadogaltas.com.tr/dogal-tas-diziler"]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class,"productPager")]//a[@class="next"]',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class,"productDescription detailLink")]',)), callback="parse_items", follow= False),
    )
    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = StoneMineItem()
        item["link"] = response.request.url
        #
        #
        title            = hxs.xpath('//h1[@id="productName"]/text()').extract()
        details          = hxs.xpath('//div[@id="productDetailTab"]//text()').extract()
        price            = hxs.xpath('//span[@class="product-price"]/text()').extract()
        #
        title  = "".join(title)
        price  = "".join(price)
        item['title'] = title
        item['price'] = price
        #
        details = re.findall("[^\n]+\n+:\n+[^\n]+","".join(details),flags=re.U) 
        details = pd.DataFrame([d.split(":") for d in details]).applymap(lambda x: x.strip())
        details = pd.concat([details,pd.DataFrame([["title",title],["price",price]])]).values.tolist()
        details = "\n".join(["|".join(detail) for detail in details])
        # details = details.drop([0],axis=1)[1].to_dict()    
        item["details"] = details
        #
        return(item)
