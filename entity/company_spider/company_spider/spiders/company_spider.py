from scrapy.spiders import Spider
from ..items import CompanySpiderItem


class CompanySpider(Spider):
    name = "wiki"
    start_urls = [
        # 'file:///D:/workspace/python/sentiment-analysis/entity/SH_companys.html',
        'file:///D:/workspace/python/sentiment-analysis/entity/SZ_002.html',
        'file:///D:/workspace/python/sentiment-analysis/entity/SZ_300.html',
        'file:///D:/workspace/python/sentiment-analysis/entity/SZ_company.html'
    ]

    def parse(self, response):
        item = CompanySpiderItem()
        title = response.xpath('//h1[@class="firstHeading"]/text()').extract()
        ths = response.xpath('//table[@class="wikitable"]/tbody/tr/th//text()').extract()
        cols = []
        for th in ths:
            if cols.count(th) == 0:
                cols.append(th)
        tds = response.xpath('//table[@class="wikitable"]/tbody/tr/td')
        i = 0
        data = []
        content = []
        for td in tds:
            text = "".join(td.xpath('.//text()').extract()).replace('\r\n', '').strip()
            content.append(text)
            i += 1
            if (i == len(cols)):
                data.append(content)
                content = []
                i = 0
        item['data'] = data
        item['title'] = title
        item['cols'] = cols
        yield item
