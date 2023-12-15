import scrapy
from scrapy.exceptions import CloseSpider
import os, sys
from urllib.parse import urljoin


class AmazonSearchSpider(scrapy.Spider):
    file_dir = os.path.dirname(__file__)
    sys.path.append(file_dir)

    name = "amazon_search"
    myBaseUrl = ''
    count = 0

    def __init__(self, category='', **kwargs):  # The category variable will have the input URL.
        self.myBaseUrl = category

    custom_settings = {
        'FEEDS': {'data/search_page.csv': {'format': 'csv', }},
        'ITEM_CLOSESPIDER': 40
    }

    def start_requests(self):
        file = '/data/search_page.csv'
        if (os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
            print("file deleted")
        else:
            print("file not found")

        keyword_list = [self.myBaseUrl]

        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com.br/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results,
                                 meta={'keyword': keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']

        ## Extract Overview Product Data
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:

            if self.count >= 40:
                raise CloseSpider('item limit')

            relative_url = product.css("h2>a::attr(href)").get()
            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
            product_url = urljoin('https://www.amazon.com.br/', relative_url).split("?")[0]
            yield {
                "thumbnail_url": product.css("img.s-image::attr(src)").get(),
                # "keyword": keyword,
                "url": product_url,
                # "ad": True if "/slredirect/" in product_url else False,
                "title": product.css("h2>a>span::text").get(),
                "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                "asin": asin,
                # "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                # "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                # "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),

            }
            self.count += 1
