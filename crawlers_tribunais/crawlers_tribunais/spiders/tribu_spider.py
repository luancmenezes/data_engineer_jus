import scrapy
from scrapy.http.request import Request
from crawlers_tribunais.items import CrawlersTribunaisItem

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
        item = CrawlersTribunaisItem()
        moviments = list
        dic = dict()

        item['classe'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[2]\
                            //span[contains(@class,"")][@id=""]//span/text()').extract_first()
        item['area'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td/text()')[-1].extract().strip() 
        item['assunto'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[4]//span/text()').extract_first()
        item['dt_distribuicao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first().split()[0]
        item['juiz'] =  response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[9]//span/text()').extract_first()
        item['vl_acao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[10]//span/text()').extract_first().split()[1]
        # list_process_1
        item['pt_processo'] = [value.strip().replace(':','')for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[1]/span/text()').extract()]
        # list_process_2 = [value.strip() for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[2]/text()').extract()\
                    #  if bool(value.strip()) ]
        # list_process_3 = [value.strip().replace(':','') for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[2]/span/text()').extract()]                                                                                                                              
        
        qtd = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/text()')
        for v1 in range(1,len(qtd)): 
            for v2 in range(1,4,2): 
                print (v2) 
                path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/text()'.format(v1,v2))  
                if v2 == 1:  
                    dic['data_mov'] = path.extract()[0].strip()  
                else:  
                    dic['mov'] = path.extract()[0].strip() + '\n' 
                    path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/span/text()'.format(v1,v2))  
                    dic['mov']  +=  path.extract()[0].strip()      
            moviments.append(dic)         
        item['list_movimentacoes'] = moviments
        yield item