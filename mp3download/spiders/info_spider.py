import scrapy


class InfoSpider(scrapy.Spider):
    """ Get Info from the website """

    name = "info"
    start_urls = ['https://www.masstamilan.io/music/a.r.rahman']

    PAGE_QUERY = '?page='
    PAGE_INDEX = 1

    def parse(self, response):
        self.logger.info("Sample Spider")
        yield {
            'movie_name': response.xpath("//div[@class='info']/h1/text()").getall(),
        }

        if InfoSpider.PAGE_INDEX <= 5:
            InfoSpider.PAGE_INDEX += 1

        next_page = f'{InfoSpider.start_urls[0]}{InfoSpider.PAGE_QUERY}{InfoSpider.PAGE_INDEX}'

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
