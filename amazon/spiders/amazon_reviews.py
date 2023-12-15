import scrapy
import os, sys
from urllib.parse import urljoin
import pandas as pd

class AmazonReviewsSpider(scrapy.Spider):

    file_dir = os.path.dirname(__file__)
    sys.path.append(file_dir)

    name = "amazon_reviews"

    myBaseUrl = ''
    count = 0
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.myBaseUrl = category

    custom_settings = {
        'FEEDS': { 'data/reviews.csv': { 'format': 'csv',}}
        }

    def start_requests(self):
        file = 'data/reviews.csv'
        search_file = 'data/search_page.csv'
        if (os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
            print("file deleted")
        else:
            print("file not found")
        df = pd.read_csv(search_file)
        asin = self.myBaseUrl

        amazon_reviews_url = f'https://www.amazon.com.br/product-reviews/{asin}/'
        yield scrapy.Request(url=amazon_reviews_url, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': 0})

    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        print("TESTE:" + next_page_relative_url)
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com.br/', next_page_relative_url)
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews,
                                 meta={'asin': asin, 'retry_count': retry_count})

        # Adding this retry_count here so we retry any amazon js rendered review pages
        elif retry_count < 6:
            retry_count = retry_count + 1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=True,
                                 meta={'asin': asin, 'retry_count': retry_count})

        ## Parse Product Reviews
        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:

            #if self.count >= 15:
                #print(self.count)
                #break
            #se for quinto produto stop no crawler

            # Check if the review contains a non-breaking space
            if '\xa0' in review_element.get():
                continue  # Skip the row if a non-breaking space is found

            yield {
                #"rating": review_element.css("*[data-hook*=review-star-rating] ::text").get()[0],
                "opinion": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                # "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                # "location_and_date": review_element.css("span[data-hook=review-date] ::text").get(),
                # "verified": bool(review_element.css("span[data-hook=avp-badge] ::text").get()),
            }

            #self.count += 1
