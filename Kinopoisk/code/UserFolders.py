#!/usr/bin/python
# -*- coding: UTF-8 -*-

from UserInfo import UserInfo
from init2 import *

class UserFolders:
    '''UserFolders.
Используется для хранения и получения данных о папках пользователя.

Принимает в конструкторе:
1. id пользователя (как число или строку);
2. Объект UserInfo.

Имеет методы:
getFoldersInfo()
loadData()'''
    
    def __init__(self, userInfo):
        
        if userInfo.__class__ != UserInfo:
            userInfo = UserInfo(userInfo)

        self.ids = userInfo.getID()
        self.foldersData = []
        
    def constructLink(self, ids):
        return settings.getMainLink() + 'user/' + str(ids) + '/movies/'
        
    def getFoldersInfo(self):
        '''Метод getFoldersInfo().
Возвращает данные о папках пользователя. Если ранее не использовался метод loadData(), то он вызывается внутри.'''
        if len(self.foldersData) == 0:
            self.loadData()
        return self.foldersData
        
    def loadData(self):
        '''Метод loadData().
Загружает с сайта данные о папках пользователя.'''
        
        link = self.constructLink(self.ids)
        page = settings.getSession().get(link).text
        soup = bs4.BeautifulSoup(page, 'lxml')
        folders = soup.find_all('div', {'class': 'item' })
        
        def getNameAndNumberFilms(folder):

            info = {}
            if folder.font == None:
                #Научиться определять ссылку на первую папку
                #Вариант с открытием второй папки не подходит, так как её может не быть.
                #Вариант с известным id папки Буду смотреть тоже не прдходит.
                info['Name'] = folder.a.text
                folderLink = folder.a['href']
                info['ShortLink'] = int(folderLink[folderLink.index('type')+5:-6])
            else:
                info['Name'] = folder.font.text
                info['ShortLink'] = None
            info['Number'] = int(folder.i.text[1:-1])

            return info

        self.foldersData = []
        for f in folders:
            try:
                self.foldersData.append(getNameAndNumberFilms(f))
            except:
                break

        def loadFolder(folder):

            films = []

            if folder['ShortLink'] == None:
                link = self.constructLink(self.ids)        
            else:
                link = self.constructLink(self.ids) + 'list/type/' + str(folder['ShortLink'])

            page = settings.getSession().get(link).text
            soup = bs4.BeautifulSoup(page, 'lxml')

            while True:

                folders = soup.find_all('a', {'class': 'name' })

                for f in folders:
                    if f['href'].find('film') == -1:
                        continue
                    films.append(int(f['href'][6:-1]))

                if len(films) == folder['Number']:
                    break

                link = settings.getMainLink()[:-1] + soup.find_all('li', {'class': 'arr' })[2].a['href'] #2 -- пока что MagicNumber
                page = settings.getSession().get(link).text
                soup = bs4.BeautifulSoup(page, 'lxml')

            films.sort()
            return films

        for f in self.foldersData:
            f['Films'] = loadFolder(f)

        return self
