from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import re

from yelp_review.items import YelpReviewItem

GOVT_AGENCIES = ['grand-central-terminal-new-york',
                'us-post-office-boston-7',
                'tampa-airport-post-office-tampa',
                'social-security-administration-sacramento-3',
                'oregon-dmv-portland',
                'minnesota-dmv-st-paul-sears-saint-paul-2',
                'arkansas-state-capitol-little-rock',
                'passport-canada-toronto'
                ]

                # Training Set
                # ['thomas-jefferson-memorial-washington',
                #  'fenway-park-boston',
                #  'chicago-passport-agency-chicago',
                #  'u-s-social-security-administration-new-york',
                #  'space-needle-seattle',
                #  'vizcaya-museum-and-gardens-miami-3',
                #  'los-angeles-public-library-los-angeles-3',
                #  'project-row-houses-houston',
                #  'motor-vehicle-division-tag-office-atlanta',
                #  'city-hall-san-francisco',
                #  'hart-plaza-detroit-2',
                #  'baltimore-harbor-tunnel-baltimore-2',
                #  'independence-hall-philadelphia',
                #  'the-metro-kansas-city',
                #  'civic-space-park-phoenix',
                #  'city-of-new-orleans-new-orleans-2',
                #  'metropolitan-government-of-nashville-and-davidson-county-nashville-163',
                #  'city-of-cleveland-cleveland-2',
                #  'southern-nevada-health-district-las-vegas-6',
                #  'glenarm-recreation-center-denver',
                #  'chicago-loop-express-secretary-of-state-facility-dmv-chicago',
                #  'classen-tag-agency-oklahoma-city',
                #  'salt-lake-city-public-library-salt-lake-city-2',
                #  'boise-depot-boise'
                #  ]

def PageLinks(self, response):
    reviewsPerPage = 4
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
        elements = sel.xpath('//div[@class="review-content"]')

        for elem in elements:
            item = YelpReviewItem()
            rating = float(elem.xpath('.//meta[@itemprop="ratingValue"]/@content').extract()[0])
            if (rating >= 1.0 and rating <= 2.0) or rating == 5.0:
                if rating == 5.0:
                    item['rating'] = 1
                else: 
                    item['rating'] = -1
                item['review'] = elem.xpath('.//p[@itemprop="description"]/text()').extract()
                yield item

        if response.url.find('?start=') == -1:
            requests += PageLinks(self, response)
            for req in requests:
                yield req