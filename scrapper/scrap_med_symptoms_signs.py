import scrapy, os

import logging
logger = logging.getLogger('symptomssignsspider')


class SymptonsSignsSpider(scrapy.Spider):
    name = 'symptomssignsspider'
    file_path = '/home/amit-kumar/GDrive/Repositories/GitHub/deep-learning-python/data/symptoms_signs/'
    start_urls = ['https://www.medicinenet.com/symptoms_and_signs/alpha_a.htm']

    def parse_article_page(self, response):
        content = '.'.join(response.css('.apPage>p').extract())

        if content is not None:
            fname = os.path.join(SymptonsSignsSpider.file_path, response.meta.get('name'))
            with open(fname, "w+") as f:
                f.write(content.encode("utf8"))

        yield {'content': content}

    def parse_page(self, response):
        for title in response.css('.AZ_results>ul>li'):
            name = title.css('a ::text').extract_first()

            name = name.replace(' Symptoms and Signs', '')\
                .replace('/', ' ')\
                .replace(' ', '_')

            for article_page in title.css('a'):
                yield response.follow(article_page, self.parse_article_page, meta={'name': name})

    def parse(self, response):

        for page in response.css('#pageContainer>#A_Z>ul>li>a'):
            yield response.follow(page, self.parse_page)