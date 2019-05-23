import scrapy
from scrapy.http.request import Request

class TribuSpider(scrapy.Spider):
    name = 'imoveis'
    start_urls = [
        'https://esaj.tjsp.jus.br/cpopg/open.do',
        'https://esaj.tjsp.jus.br/cposg/open.do',
        'https://esaj.tjsp.jus.br/cposgcr/open.do',
        'https://esaj.tjms.jus.br/cpopg5/open.do',
        'https://esaj.tjms.jus.br/cposg5/open.do'
    ]
