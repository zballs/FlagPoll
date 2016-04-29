from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import re

from yelp_review.items import YelpReviewItem

GOVT_AGENCIES = ['thomas-jefferson-memorial-washington',
                 'fenway-park-boston',
                 'chicago-passport-agency-chicago',
                 'u-s-social-security-administration-new-york',
                 'space-needle-seattle',
                 'vizcaya-museum-and-gardens-miami-3',
                 'los-angeles-public-library-los-angeles-3',
                 'williams-waterwall-houston',
                 'project-row-houses-houston',
                 'motor-vehicle-division-tag-office-atlanta',
                 'city-hall-san-francisco',
                 'hart-plaza-detroit-2',
                 'baltimore-harbor-tunnel-baltimore-2',
                 'independence-hall-philadelphia',
                 'the-metro-kansas-city']

def PageLinks(self, response):
    reviewsPerPage = 40
    sel = Selector(response)
    totalReviews = int(sel.xpath('//div[@class="rating-info clearfix"]//span[@itemprop="reviewCount"]/text()').extract()[0].strip().split(' ')[0])
    pages = [Request(url=response.url + '?start=' + str(reviewsPerPage*(n+1)), callback=self.parse) for n in range(totalReviews/reviewsPerPage)]
    return pages

class YelpSpider(Spider):
    name = "yelp_spider"
    allowed_domains = ["yelp.com"]
    start_urls = ['http://www.yelp.com/biz/%s' % s for s in GOVT_AGENCIES]

    def parse(self, response):
        requests = []

        sel = Selector(response)
        reviews = sel.xpath('//div[@class="review-content"]')

        for rev in reviews:
            item = YelpReviewItem()
            item['review'] = rev.xpath('.//p[@itemprop="description"]/text()').extract()
            yield item

        if response.url.find('?start=') == -1:
            requests += PageLinks(self, response)
            for req in requests:
                yield req