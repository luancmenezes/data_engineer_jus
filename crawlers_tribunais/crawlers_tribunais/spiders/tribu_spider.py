from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.http.request import Request
from scrapy.utils.response import open_in_browser
from crawlers_tribunais.items import CrawlersTribunaisItem

def foundTrb(num_process):
    uf = num_process.split('.')[-2]
    uf_trb = {
        '26':'tjsp',
        '12':'tjms'
    }
    return uf_trb[uf]
    


class TribuSpider(Spider):
    name = 'tribunal'
    consult_process_url = 'https://esaj.tjsp.jus.br/cpopg/open.do'
    start_urls = [
        # consult_process_url,
        'https://esaj.tjsp.jus.br/cpopg/open.do',#1º grau
        'https://esaj.tjsp.jus.br/cposg/open.do', #2º grau
        # 'https://esaj.tjsp.jus.br/cposgcr/open.do', #2º grau turma recursal
        'https://esaj.tjms.jus.br/cpopg5/open.do',
        # 'https://esaj.tjms.jus.br/cposg5/open.do'
    ]

    def parse(self,response):
        data_tbjs_1 = {
            'dadosConsulta.valorConsulta' : '1002298-86.2015.8.26.0271',
            'cbPesquisa':'NUMPROC',
            'dadosConsulta.localPesquisa.cdLocal':'-1',
            'dadosConsulta.tipoNuProcesso':'SAJ'
        }
        data_tbjs_2 = {
            'dePesquisa' : '1002298-86.2015.8.26.0271',
            'cbPesquisa':'NUMPROC',
            'localPesquisa.cdLocal':'-1',
            'tipoNuProcesso':'SAJ',
            'paginaConsulta':'1'
        }
        data_tjms_1 = {
            'dadosConsulta.localPesquisa.cdLocal': '-1',
            'cbPesquisa': 'NUMPROC',
            'dadosConsulta.tipoNuProcesso': 'SAJ',
            'dadosConsulta.valorConsulta': '0821901-51.2018.8.12.0001',
            'uuidCaptcha': 'sajcaptcha_19f9ec880b8648a28f8f74d4ca0f444f'
        } 
        data_tjms_2 = {
            'paginaConsulta': '1',
            'localPesquisa.cdLocal': '-1',
            'cbPesquisa': 'NUMPROC',
            'tipoNuProcesso': 'SAJ',
            'dePesquisa':' 0821901-51.2018.8.12.0001',
            'pbEnviar': 'Pesquisar'     
        } 


        if('cpopg' == response.request.url.split('/')[-2]):
            yield FormRequest.from_response(response, formdata=data_tbjs_1, callback=self.parse_tbj, meta={'degree':'tbjs'})
        elif('cposg' == response.request.url.split('/')[-2]):
            yield FormRequest.from_response(response, formdata=data_tbjs_2, callback=self.parse_tbjs_2)
        elif('cpopg5' == response.request.url.split('/')[-2]):
            yield FormRequest.from_response(response, formdata=data_tjms_1, callback=self.parse_tbj, meta={'degree':'tjms'})

       
    def parse_tbjs_2(self,response):
        links = response.xpath('//a[contains(@class,"linkProcesso")]/@href').extract()
        for url in links:
            page = response.urljoin(url)
            yield Request(page, callback=self.parse_tbj, meta={'degree':'tbjs_2'})    

    def parse_tbj(self,response):
        # open_in_browser(response)
        
        degree = response.meta["degree"]
        

        item = CrawlersTribunaisItem()
        moviments = []
        dic = dict()

        if (degree == 'tbjs'):
            item['vl_acao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[10]//span/text()').extract_first().split()[1]
            item['dt_distribuicao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first().split()[0]
            item['juiz'] =  response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[9]//span/text()').extract_first()
        elif(degree == 'tjms' ):
            item['vl_acao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[9]//span/text()').extract_first().strip()
            item['dt_distribuicao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[5]//span/text()').extract_first()[:10]
            item['juiz'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[8]//span/text()').extract_first()
            item['vara'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first()
        elif (degree == 'tbjs_2' or degree != 'tbjs_2'):
            try:
                item['processo'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td[2]//table//span/text()').extract_first().strip()
                item['vara'] = '2ª Vara Cível '
            except:
                pass
        
        item['classe'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[2]\
                        //span[contains(@class,"")][@id=""]//span/text()').extract_first()
        item['area'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td/text()')[-1].extract().strip() 
        item['assunto'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[4]//span/text()').extract_first()
        #2nd nao existe
        # list_process_1
        item['pt_processo'] = [value.strip().replace(':','')for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[1]/span/text()').extract()]
        # list_process_2 = [value.strip() for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[2]/text()').extract()\
                    #  if bool(value.strip()) ]
        # list_process_3 = [value.strip().replace(':','') for value in response.xpath('//table[@id="tableTodasPartes"]//tr[contains(@class, "fundoClaro")]//td[2]/span/text()').extract()]                                                                                                                              
        
        qtd = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/text()')
        for v1 in range(1,len(qtd)): 
            for v2 in range(1,4,2): 
                path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/text()'.format(v1,v2))  
                if v2 == 1:  
                    dic['data_mov'] = path.extract()[0].strip()  
                else:  
                    try:
                        dic['mov'] = path.extract()[0].strip() + '\n' 
                        path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/span/text()'.format(v1,v2))  
                        dic['mov']  +=  path.extract()[0].strip()
                    except:
                        pass      
                moviments.append(dic)         
        item['list_movimentacoes'] = moviments
        yield item
