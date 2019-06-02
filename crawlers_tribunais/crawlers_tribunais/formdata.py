#!/usr/bin/python
# -*- coding: utf-8 -*-

class Formdata:
    def __init__(self, processo):
        self.processo = processo
    def tbjs_1(self):
        formdata = {
                    'dadosConsulta.valorConsulta' : self.processo,
                    'cbPesquisa':'NUMPROC',
                    'dadosConsulta.localPesquisa.cdLocal':'-1',
                    'dadosConsulta.tipoNuProcesso':'SAJ'
                }
        return formdata
    def tbjs_2(self):
        formdata = {
            'dePesquisa' : self.processo,
            'cbPesquisa':'NUMPROC',
            'localPesquisa.cdLocal':'-1',
            'tipoNuProcesso':'SAJ',
            'paginaConsulta':'1'
        }
        return formdata
    def tbjms_1(self):
        formdata = {
            'dadosConsulta.localPesquisa.cdLocal': '-1',
            'cbPesquisa': 'NUMPROC',
            'dadosConsulta.tipoNuProcesso': 'SAJ',
            'dadosConsulta.valorConsulta': self.processo,
            'uuidCaptcha': 'sajcaptcha_19f9ec880b8648a28f8f74d4ca0f444f'
        }
        return formdata
    def tbjms_2(self):
        formdata = {
            'paginaConsulta': '1',
            'localPesquisa.cdLocal': '-1',
            'cbPesquisa': 'NUMPROC',
            'tipoNuProcesso': 'SAJ',
            'dePesquisa': self.processo  
        }
        return formdata 