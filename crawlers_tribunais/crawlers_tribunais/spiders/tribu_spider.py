from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.http.request import Request
from scrapy.utils.response import open_in_browser
from crawlers_tribunais.items import CrawlersTribunaisItem
from crawlers_tribunais.formdata import * 

def foundTrb(num_process):
    uf = num_process.split('.')[-2]
    uf_trb = {
        '26':'tjsp',
        '12':'tjms'
    }
    return uf_trb[uf]


class TribuSpider(Spider):
    name = 'tribunal'
    start_urls = [
        'https://esaj.tjsp.jus.br/cpopg/open.do',#1º grau
        'https://esaj.tjsp.jus.br/cposg/open.do', #2º grau
        'https://esaj.tjsp.jus.br/cposgcr/open.do', #2º grau turma recursal
        'https://esaj.tjms.jus.br/cpopg5/open.do',#1º grau
        'https://esaj.tjms.jus.br/cposg5/open.do' #2º grau
    ]

    def parse(self,response):
        tbj_id = foundTrb(self.processo) #define qual é o triibunal pela regra http://www.cnj.jus.br/programas-e-acoes/pj-numeracao-unica
        form = Formdata(self.processo) #define tipo de formulário para acessar informações

        #Condicional para decidir qual informação será crawleada
        if(tbj_id == 'tjsp'):
            yield FormRequest.from_response(response,   formdata=form.tbjs_1(),
                                                        callback=self.parse_tbj,
                                                      meta={'degree':'tjms_2',
                                                                'processo':self.processo,
                                                                'tribunal':tbj_id,
                                                                'grau':'1'})
            yield FormRequest.from_response(response,   formdata=form.tbjs_2(), 
                                                        callback=self.parse_tbjs_2,
                                                        meta={'tribunal':tbj_id,
                                                            'processo':self.processo })
        elif(tbj_id == 'tjms'):
            yield FormRequest.from_response(response,   formdata=form.tbjms_1(), 
                                                        callback=self.parse_tbj, 
                                                        meta={'degree':'tjms',
                                                            'processo':self.processo,
                                                            'tribunal':tbj_id,
                                                            'grau':'1'})
            yield FormRequest.from_response(response,   formdata=form.tbjms_2(),
                                                        callback=self.parse_tbj,
                                                        meta={'degree':'tjms_2',
                                                            'processo':self.processo,
                                                            'tribunal':tbj_id,
                                                            'grau':'2'})

       
    def parse_tbjs_2(self,response):
        #parse para o tribunal de justiçca de SP de 2 grau
        links = response.xpath('//a[contains(@class,"linkProcesso")]/@href').extract()
        for url in links:
            page = response.urljoin(url)
            yield Request(page, callback=self.parse_tbj,
                                meta={'degree':'tbjs_2',
                                'processo':response.meta["processo"],
                                'tribunal':response.meta["tribunal"],
                                'grau':'2'})    

    def parse_tbj(self,response):
        #parse generalista para crawlers
        item = CrawlersTribunaisItem()
        moviments = []
        dic = dict()
        degree = response.meta["degree"]
        item['processo'] = response.meta["processo"]
        item['tribunal'] = response.meta["tribunal"]
        item['grau'] = response.meta["grau"]
        

        if (response.meta["grau"] == '1' and response.meta["tribunal"] == 'tjsp' ):
            item['vl_acao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[10]//span/text()').extract_first().split()[1]
            item['dt_distribuicao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first().split()[0]
            item['juiz'] =  response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[9]//span/text()').extract_first()
        elif(response.meta["grau"] == '1' and response.meta["tribunal"] == 'tjms' ):
            try:
                item['vl_acao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[9]//span/text()').extract_first().strip()
            except:
                pass
            try:    
                item['dt_distribuicao'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[5]//span/text()').extract_first()[:10]
            except:
                pass
            item['juiz'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[8]//span/text()').extract_first()
            item['vara'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[6]//span/text()').extract_first()
        elif(response.meta["grau"] == '2' and response.meta["tribunal"] == 'tjms' ):
            item['juiz'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[7]//span/text()').extract_first()                                                                                                               
        elif (response.meta["grau"] == '2' and response.meta["tribunal"] == 'tjsp' ):
                item['processo_2'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td[2]//table//span/text()').extract_first().strip()
                item['vara'] = '2ª Vara Cível '
            
        item['classe'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[2]\
                            //span[contains(@class,"")][@id=""]//span/text()').extract_first()
        try:
            item['area'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[1]//td/text()')[-1].extract().strip()
        except:
            pass
        item['assunto'] = response.xpath('//table[contains(@class,"secaoFormBody")][@id=""]//tr[4]//span/text()').extract_first()
           
        # Não foi especificado como deveria ser armazenado as partes do processo
        # Foram concatenada as informações   
        item['pt_processo'] = [value.strip().replace(':','')for value in response.xpath('//table[@id="tablePartesPrincipais"]//tr[contains(@class, "fundoClaro")]//td[1]/span/text()').extract()]
        item['pt_processo'] += [value.strip() for value in response.xpath('//table[@id="tablePartesPrincipais"]//tr[contains(@class, "fundoClaro")]//td[2]/text()').extract()]
        item['pt_processo'] += [value.strip().replace(':','') for value in response.xpath('//table[@id="tablePartesPrincipais"]//tr[contains(@class, "fundoClaro")]//td[2]/span/text()').extract()]                                                                                                                              
        
        #Ultima movimentacoes
        qtd = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/text()')
        try:
            for v1 in range(1,len(qtd)): 
                for v2 in range(1,4,2): 
                    path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/text()'.format(v1,v2))  
                    if v2 == 1:  
                        dic['data_mov'] = path.extract()[0].strip()  
                    else:  
                        dic['mov'] = path.extract()[0].strip() + '\n' 
                        path = response.xpath('//*[@id="tabelaUltimasMovimentacoes"]/tr[{}]/td[{}]/span/text()'.format(v1,v2))  
                        dic['mov']  +=  path.extract()[0].strip()
                    moviments.append(dic)         
            item['list_movimentacoes'] = moviments
        except:
            pass
        yield  item
