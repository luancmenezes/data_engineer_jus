# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlersTribunaisItem(scrapy.Item):
    # Dados a serem coletados:
    n_processo = scrapy.Field()
    tribunal = scrapy.Field()
    grau = scrapy.Field()
    classe = scrapy.Field()
    area = scrapy.Field()
    assunto = scrapy.Field()
    dt_distribuicao = scrapy.Field()
    vl_acao = scrapy.Field()
    juiz = scrapy.Field()
    pt_processo = scrapy.Field()
    list_movimentacoes = scrapy.Field()
    processo = scrapy.Field()
    processo_2 = scrapy.Field()
    vara = scrapy.Field()
    pass
