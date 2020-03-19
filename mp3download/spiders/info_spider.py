import scrapy
from ..items import Mp3DownloadItem


class InfoSpider(scrapy.Spider):
    """ Get Info from the website """

    name = "info"
    start_urls = ['https://www.masstamilan.io/tag/A']

    PAGE_QUERY = '?page='
    PAGE_INDEX = 1

    def parse(self, response):
        self.logger.info("Movie Data Fetching Spider")
        divs = response.xpath(
                '//div[@class="botlist"]/div[@class="botitem"]/a/div/div[@class="info"]')
        movie_info = Mp3DownloadItem()

        for element in divs:
            movie_info['movie_name'] = element.xpath('normalize-space(.//h1/text())').get()
            movie_info['stars'] = element.xpath('normalize-space(.//p[@class="description"]/text()[2])').get()
            movie_info['music'] = element.xpath('normalize-space(.//p[@class="description"]/text()[4])').get()
            movie_info['director'] = element.xpath('normalize-space(.//p[@class="description"]/text()[6])').get()

            yield movie_info

        # yield {
        #     'movie_name': response.xpath("//div[@class='info']/h1/text()").getall(),
        # }
        #
        # if InfoSpider.PAGE_INDEX <= 5:
        #     InfoSpider.PAGE_INDEX += 1
        #
        # next_page = f'{InfoSpider.start_urls[0]}{InfoSpider.PAGE_QUERY}{InfoSpider.PAGE_INDEX}'
        #
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
