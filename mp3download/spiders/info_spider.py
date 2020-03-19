import scrapy
from ..items import Mp3DownloadItem


class InfoSpider(scrapy.Spider):
    """ Get Info from the website """

    name = "info"
    start_urls = ['https://www.masstamilan.io/tag/A']

    domain = 'https://www.masstamilan.io'

    def parse(self, response):
        self.logger.info("Movie Data Fetching Spider")
        divs = response.xpath(
            '//div[@class="botlist"]/div[@class="botitem"]/a')
        movie_info = Mp3DownloadItem()

        for element in divs:
            movie_info['movie_name'] = element.xpath('normalize-space(.//div/div[@class="info"]/h1/text())').get()
            movie_info['stars'] = element.xpath(
                'normalize-space(.//div/div[@class="info"]/p[@class="description"]/text()[2])').get()
            movie_info['music'] = element.xpath(
                'normalize-space(.//div/div[@class="info"]/p[@class="description"]/text()[4])').get()
            movie_info['director'] = element.xpath(
                'normalize-space(.//div/div[@class="info"]/p[@class="description"]/text()[6])').get()
            movie_link = response.urljoin(element.xpath(
                'normalize-space(.//@href)').get())

            yield scrapy.Request(movie_link, callback=self.parse_movie, meta={'item': movie_info})

        next_page = response.xpath('//nav[@class="pagination"]/span[@class="next"]/a/@href').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_movie(self, response):
        movie_full = response.meta['item']
        downloader = response.xpath("//h2[@class='ziparea normal']/a[@class='dlink anim'][1]/@href").get()
        movie_full['link'] = self.domain + downloader
        return movie_full
