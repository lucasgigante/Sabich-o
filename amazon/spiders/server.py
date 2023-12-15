import csv
import scrapydo
import os

from flask import Flask , render_template, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from amazon.spiders.remove_duplicates import remove_duplicates
from amazon.spiders.limpagem import preprocess
from amazon.spiders.modelo import CNN

from amazon.spiders.amazon_search import AmazonSearchSpider
from amazon.spiders.amazon_reviews import AmazonReviewsSpider

app = Flask(__name__)

scrapydo.setup()
crawl_runner = CrawlerRunner()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['produto'] # Getting the Input Amazon Product URL
        global produto
        produto = s
        return redirect(url_for('search')) # Passing to the Scrape function

@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == 'POST':
        r = request.form['fetchreviews'] # Getting the Input Amazon Product URL
        global produtoreviews
        produtoreviews = r
        return redirect(url_for('reviews')) # Passing to the Scrape function

    scrape_with_crochet(spider=AmazonSearchSpider,produto=produto) # Passing that URL to our Scraping Function


    with open("data/search_page.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        header = next(reader)
        return render_template("table.html", header=header, rows=reader)

@app.route('/reviews')
def reviews():

    file_path = 'data/reviews.csv'

    scrape_with_crochet(spider=AmazonReviewsSpider,produto=produtoreviews)

    if (not os.path.exists(file_path) or not os.path.isfile(file_path)):
        return 'ERROR'

    if os.path.getsize(file_path) == 0:
        return 'Não foram encontradas reviews para este produto :('

    remove_duplicates(file_path, 'opinion')

    preprocess(file_path)

    CNN(file_path)

    with open(file_path, encoding="utf8") as file:

        reader = csv.reader(file)
        header = next(reader)
        return render_template("table.html", header=header, rows=reader)

def scrape_with_crochet(spider, produto):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = scrapydo.run_spider(spider, category = produto)
    return eventual

def _crawler_result(item, response, spider):
    print ('ok')

if __name__ == '__main__':
  app.run(debug=True)