#!/usr/bin/python
# -*- coding: UTF-8 -*-

from UserInfo import UserInfo
from init2 import *

class UserVotesData:

    '''UserVotesData.
Используется для хранения и загрузки данных об оценках пользователя.

Может принимать в конструкторе:
1. id пользователя (как число или строку);
2. Объект UserInfo.

Имеет методы:
getUserInfo()
getData()
loadData()
loadDataFromSite()
loadDataFromFolder(folder)
loadDataFromTable(sheet)'''

    eye = 0
    fields = ['nameRus', 'nameEng', 'filmId', 'link', 'vote', 'date']

    def __init__(self, userInfo):

        if userInfo.__class__ == UserInfo:
            self.userInfo = userInfo
        else:
            self.userInfo = UserInfo(userInfo)
        self.data = []

    def getData(self):
        '''Метод getData().
Возвращает данные об оценках пользователя.'''
        if self.data == []:
            print 'Данные ещё не загружены'
        return self.data

    def getUserInfo(self):
        '''Метод getUserInfo().
Возвращает информацию о пользователе (класс UserInfo).'''
        return self.userInfo

    def __loadDataInterface(self, offline = None, folder = None, isPrint = True):

        if offline == None:
            offline = settings.getMode()

        def getDataFromPage(page):
            def getDataAboutFilm(divItem):

                if divItem.find('div', UserVotesData.fields[0]) == None:
                    return None

                sz = divItem.find('a')['href'].find('film/') + len('film/')
                film_id = divItem.find('a')['href'][sz:-1]
                film_link = settings.getMainLink() + 'film/' + str(film_id) + '/'
                return {
                         UserVotesData.fields[0] : divItem.find('div', UserVotesData.fields[0]).text,
                         UserVotesData.fields[1] : divItem.find('div', UserVotesData.fields[1]).text,
                         UserVotesData.fields[2] : film_id,
                         UserVotesData.fields[3] : film_link,
                         UserVotesData.fields[4] : divItem.find('div', UserVotesData.fields[4]).text if divItem.find('div', UserVotesData.fields[4]).text != '' else str(UserVotesData.eye),
                         UserVotesData.fields[5] : divItem.find('div', UserVotesData.fields[5]).text
                       }

            userFilms = bs4.BeautifulSoup(page, 'lxml').find_all('div', 'item')
            return [getDataAboutFilm(film) for film in userFilms]

        pageNumber = 1
        userVotesData = []
        if isPrint:
            print 'Get user data:', self.userInfo.getNick()

        link = ''
        files = []
        page = ''

        if offline:
            all_files = os.listdir(folder)
            for f in all_files:
                if 'htm' in f:
                    files.append(f)
            file_r = open(os.path.join(folder, files[0]))
            page = file_r.read()
            file_r.close()

        else:
            link = self.userInfo.getLink() + '/votes/list/ord/date/page/'
            page = settings.getSession().get(link).text

        numberOfFilms = bs4.BeautifulSoup(page, 'lxml').find_all('h2', {'class': 'main_title'})[0].string
        numberOfFilms = int(numberOfFilms[numberOfFilms.index('(') + 1 : numberOfFilms.index(')')])

        ts = time.time()
        t1 = ts
        while True:

            page = ''
            if offline:
                if pageNumber <= len(files):
                    file_r = open(os.path.join(folder, files[pageNumber - 1]))
                    page = file_r.read()
                    file_r.close()
                else:
                    page = ''
            else:
                page = settings.getSession().get(link + str(pageNumber)).text

            data = getDataFromPage(page)
            
            while True:
                try:
                    data.remove(None)
                except:
                    break

            userVotesData += data
            pageNumber += 1

            t2 = time.time()
            if isPrint:
                print 'Load', str((len(userVotesData) * 100.0) / numberOfFilms) + '%...'
                print 'Time:', (t2-t1), 'seconds'
            t1 = t2

            if len(userVotesData) == numberOfFilms:
                if isPrint:
                    print 'Load done'
                    print 'Time:', (t2-ts), 'seconds'
                break

        self.data = userVotesData

        return self
    
    def loadDataFromFolder(self, folder = None, isPrint = True):
        '''Метод loadDataFromSite(folder).
Загружает оценки пользователя из папки, название которой -- id пользователя.
Параметр folder позволяет выбрать папку, в которой находится папка с данными. По умолчанию папка ищется в директории, откуда вызывается программа.
Параметр isPrint отвечает за вывод вспомогательной информации о загрузке.'''
        if folder == None:
            folder = os.path.join('.', self.userInfo.getID())
        return self.__loadDataInterface(offline = True, folder = folder, isPrint = isPrint)
        
    def loadDataFromSite(self, isPrint = True):
        '''Метод loadDataFromSite().
Загружает оценки пользователя с сайта.
Параметр isPrint отвечает за вывод вспомогательной информации о загрузке.'''
        return self.__loadDataInterface(offline = False, isPrint = isPrint)
        
    def loadData(self, isPrint = True):
        '''Метод loadData().
Загружает оценки пользователя в соответствии со значением переменной settings.OFFLINE_MODE.
Параметр isPrint отвечает за вывод вспомогательной информации о загрузке.'''
        if settings.getMode():
            return self.loadDataFromFolder(isPrint = isPrint)
        else:
            return self.loadDataFromSite(isPrint = isPrint)

    def loadDataFromTable(self, sheet):
        '''Метод loadDataFromTable(sheet).
Загружает оценки пользователя из .xls-таблицы. Подробнее смотри класс DataVotesTablesLoader.'''
        row = sheet.row_values(0)
        
        usedFields = {}
        
        for idx in xrange(len(row)):
            usedFields[idx] = row[idx] 
        
        self.data = []
        sz = len(settings.getMainLink() + 'film/') + 1
        for idx in range(1, sheet.nrows):
            row = sheet.row_values(idx)
            dataAboutFilm = {}
            for jdx in xrange(len(row)):
                dataAboutFilm[usedFields[jdx]] = row[jdx]
            dataAboutFilm['filmId'] = dataAboutFilm['link'][sz:-1]
            self.data += [dataAboutFilm]
        return self
