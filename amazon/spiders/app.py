import csv
import scrapydo
import os

from flask import Flask , render_template, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from remove_duplicates import remove_duplicates
from limpagem import preprocess
from modelo import CNN

from amazon_search import AmazonSearchSpider
from amazon_reviews import AmazonReviewsSpider

app = Flask(__name__)

scrapydo.setup()
crawl_runner = CrawlerRunner()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':

        caminho_do_arquivo = '/data/search_page.csv'

        # Use a função remove do módulo os para deletar o arquivo
        try:
            os.remove(caminho_do_arquivo)
            print(f'O arquivo {caminho_do_arquivo} foi deletado com sucesso.')
        except FileNotFoundError:
            print(f'O arquivo {caminho_do_arquivo} não foi encontrado.')
        except Exception as e:
            print(f'Ocorreu um erro ao tentar deletar o arquivo: {e}')


        s = request.form['productName'] # Getting the Input Amazon Product URL
        global produto
        produto = s
        print(produto)
        return redirect(url_for('loading')) # Passing to the Scrape function


@app.route('/loading', methods=['POST', 'GET'])
def loading():
    if request.method == 'POST':
        # Server-side processing for the POST request
        redirect(url_for('results'))

    caminho_do_arquivo = 'data/search_page.csv'

    # Use a função remove do módulo os para deletar o arquivo
    try:
        os.remove(caminho_do_arquivo)
        print(f'O arquivo {caminho_do_arquivo} foi deletado com sucesso.')
    except FileNotFoundError:
        print(f'O arquivo {caminho_do_arquivo} não foi encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro ao tentar deletar o arquivo: {e}')


    scrape_with_crochet(spider=AmazonSearchSpider, produto=produto)
    print("produto nome " + produto)
    # Render the 'loading.html' template for GET requests
    return render_template('loading.html')


@app.route('/results', methods=['GET','POST'])
def results():

    if request.method == 'POST':
        r1 = request.form['input-form'] # Getting the Input Amazon Product URL
        price = request.form['price']
        thumb = request.form['thumb']
        url = request.form['url']
        title = request.form['title']
        
        global produtoreviews
        produtoreviews = r1

        global preco
        preco = price

        global titulo
        titulo = title

        global caminho
        caminho = url

        global imagem
        imagem = thumb

        print(produtoreviews)
        print(price)
        print(thumb)
        print(url)
        print(title)

        return redirect(url_for('reviews')) # Passing to the Scrape function


    with open("data/search_page.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        header = next(reader)
        return render_template("results.html", header=header, rows=reader)

@app.route('/reviews')
def reviews():

    file_path = 'data/reviews.csv'

    # Use a função remove do módulo os para deletar o arquivo
    try:
        os.remove(file_path)
        print(f'O arquivo {file_path} foi deletado com sucesso.')
    except FileNotFoundError:
        print(f'O arquivo {file_path} não foi encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro ao tentar deletar o arquivo: {e}')

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
        return render_template("reviews.html", header=header, rows=reader, link=produtoreviews,  preco=preco, titulo=titulo, caminho=caminho, imagem=imagem)



def scrape_with_crochet(spider, produto):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = scrapydo.run_spider(spider, category=produto)
    return eventual


def _crawler_result(item, response, spider):
    print('ok')



if __name__ == '__main__':
    app.run(debug=True)