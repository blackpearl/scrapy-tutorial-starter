import scrapy
from ..items import Mp3DownloadItem


class InfoSpider(scrapy.Spider):
    """ Get Info from the website """

    name = "info"
    # start_urls = ['https://www.masstamilan.io/tag/A',
    #               'https://www.masstamilan.io/tag/B',
    #               'https://www.masstamilan.io/tag/C',
    #               'https://www.masstamilan.io/tag/D',
    #               'https://www.masstamilan.io/tag/E',
    #               'https://www.masstamilan.io/tag/F',
    #               'https://www.masstamilan.io/tag/G',
    #               'https://www.masstamilan.io/tag/H',
    #               'https://www.masstamilan.io/tag/I',
    #               'https://www.masstamilan.io/tag/J',
    #               'https://www.masstamilan.io/tag/K',
    #               'https://www.masstamilan.io/tag/L',
    #               'https://www.masstamilan.io/tag/M',
    #               'https://www.masstamilan.io/tag/N',
    #               'https://www.masstamilan.io/tag/O',
    #               'https://www.masstamilan.io/tag/P',
    #               'https://www.masstamilan.io/tag/Q',
    #               'https://www.masstamilan.io/tag/R',
    #               'https://www.masstamilan.io/tag/S',
    #               'https://www.masstamilan.io/tag/T',
    #               'https://www.masstamilan.io/tag/U',
    #               'https://www.masstamilan.io/tag/V',
    #               'https://www.masstamilan.io/tag/W',
    #               'https://www.masstamilan.io/tag/X',
    #               'https://www.masstamilan.io/tag/Y',
    #               'https://www.masstamilan.io/tag/Z',
    #               'https://www.masstamilan.io/tag/0',
    #               'https://www.masstamilan.io/tag/1',
    #               'https://www.masstamilan.io/tag/2',
    #               'https://www.masstamilan.io/tag/3',
    #               'https://www.masstamilan.io/tag/4',
    #               'https://www.masstamilan.io/tag/5',
    #               'https://www.masstamilan.io/tag/6',
    #               'https://www.masstamilan.io/tag/7',
    #               'https://www.masstamilan.io/tag/8',
    #               'https://www.masstamilan.io/tag/9',
    #               ]
    start_urls = ['https://www.masstamilan.io/tag/A', ]

    domain = 'https://www.masstamilan.io'

    def parse(self, response):
        self.logger.info(f"Fetching {response.url}")
        divs = response.xpath(
            '//div[@class="botlist"]/div[@class="botitem"]/a')

        for element in divs:
            movie_info = Mp3DownloadItem()
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

        if downloader:
            movie_full['link'] = self.domain + downloader
        else:
            movie_full['link'] = "NA"

        return movie_full
