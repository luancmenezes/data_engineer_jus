import scrapy
from scrapy.http.request import Request

class TribuSpider(scrapy.Spider):
    name = 'tribunal'
    consult_process_url = 'https://esaj.tjsp.jus.br/cpopg/open.do'
    start_urls = [
        consult_process_url
        # 'https://esaj.tjsp.jus.br/cpopg/open.do',
        # 'https://esaj.tjsp.jus.br/cposg/open.do',
        # 'https://esaj.tjsp.jus.br/cposgcr/open.do',
        # 'https://esaj.tjms.jus.br/cpopg5/open.do',
        # 'https://esaj.tjms.jus.br/cposg5/open.do'
    ]

    def parse(self,response):
        data = {
            'dadosConsulta.valorConsulta' : '1002298-86.2015.8.26.0271'
        }
        print("OPAAAAAAAAAAa")
        yield scrapy.FormRequest(url=self.consult_process_url, formdata=data, callback=self.parse_quotes)
    
    def parse_quotes(self,response):
        classe = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[2]\
                            //span[contains(@class,"")][@id=""]//span/text()').extract_first()
        area = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td/text()')[-1].extract().strip() 
        assunto = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[4]//span/text()').extract_first()
        data = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first().split()[0]  
        vl_acao = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[10]//span/text()').extract_first().split()[1]
        yield a

    # yield Request(url, callback=self.parse)