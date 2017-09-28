#!/usr/bin/python
# -*- coding: UTF-8 -*-

from init2 import *
from UserVotesData import UserVotesData

class DataVotesTablesLoader:

    '''DataVotesTablesLoader.
Используется для получения информации из ранее сгенерированных таблиц.

Принимает в конструкторе нзвание файла .xls.

Имеет методы:
loadData()'''
    
    def __init__(self, filename):
        
        self.filename = ''
        try:
            f = open(filename)
            f.close()
            self.filename = filename
        except:
            print 'File does not exist'
            
    def loadData(self):
        '''Метод loadData().
Запускает процесс считывания и выдаёт list из UserVotesData.'''
        
        if self.filename == '':
            return []
        
        self.book = xlrd.open_workbook(self.filename)
        sheets = self.book.sheet_names()
        
        def getName(sheet_name):
            return str(sheet_name[:sheet_name.index('-')-1])
            
        if len(sheets) == 1:
            sheet = self.book.sheet_by_name(sheets[0])
            return [UserVotesData(getName(sheets[0])).loadDataFromTable(sheet)]
        else:
            userVotesData = []
            for idx in xrange(len(sheets)):
                if 'Comparable' in sheets[idx]:
                    continue
                sheet = self.book.sheet_by_name(sheets[idx])
                userVotesData += [UserVotesData(getName(sheets[idx])).loadDataFromTable(sheet)]
            return userVotesData
