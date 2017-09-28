#!/usr/bin/python
# -*- coding: UTF-8 -*-

from UserVotesData import UserVotesData
from init2 import *

class DataVotesPresenter:

    '''DataVotesPresenter.
Используется для визуализации данных о пользователях.

Может принимать в конструкторе:
1. Объект UserInfo;
2. List из UserInfo.

Имеет методы:
saveToXLS(filename)'''
    
    def __init__(self, usersVotesData):
        if type(usersVotesData) != list:
            usersVotesData = [usersVotesData]
        
        self.usersVotesData = []
        for userVotesData in usersVotesData:
            if userVotesData.__class__ == UserVotesData:
                self.usersVotesData.append(userVotesData)
                
        self.book = None
    
    def saveToXLS(self, filename = 'kinopoisk.data.xls', sorts = 1):
        '''Метод saveToXLS(filename) сохраняет информацию в xls:<br>
1. Если пользователей несколько - первая страница сравнивательная.<br>
2. Страницы пользователей с информацией о них.

Параметр filename -- название файла, где будут находиться данные. По умолчанию - "kinopoisk.data.xls".
Параметр sorts - число или список чисел с номерами сортировок. По умолчанию - 1.
Доступные значения:
1:
По количеству пользователей, оценивших фильм.
В случае равенства -- сначала те, которые смотрел первый пользователь (когда фильмов 1, то наоборот).
В случае равенство -- по сумме оценок.
2:
По средней оценке фильма, не считая фильмы без оценки.
В случае равенство -- по количеству пользователей, оценивших фильм.
В случае равенства -- по количеству ненулевых оценок.
В случае равенства -- сначала те, которые смотрел первый пользователь (когда фильмов 1, то наоборот).'''

        if len(self.usersVotesData) == 0:
            return

        def savePersonalPage(userVotesData):
            sheet = self.book.add_sheet(str(userVotesData.getUserInfo().getID()) + ' - ' + userVotesData.getUserInfo().getNick())
            data = userVotesData.getData()
            row = sheet.row(0)

            usedFields = []
            usedFields.append(UserVotesData.fields.index('nameRus'))
            usedFields.append(UserVotesData.fields.index('nameEng'))
            usedFields.append(UserVotesData.fields.index('link'))
            usedFields.append(UserVotesData.fields.index('vote'))
            usedFields.append(UserVotesData.fields.index('date'))

            f = 0
            for field in usedFields:
                row.write(f, UserVotesData.fields[field])
                f += 1

            for indexFilm in xrange(len(data)):
                row = sheet.row(indexFilm + 1)

                f = 0
                for i in usedFields:
                    row.write(f, data[indexFilm][UserVotesData.fields[i]])
                    f += 1
        
        def saveComparatorPage(sortFunctionV = 1):
            
            films_links = []
            films_names = []
            nicks = [userVotesData.getUserInfo().getNick() for userVotesData in self.usersVotesData]
            table = []

            for idx in xrange(len(self.usersVotesData)):
                data = self.usersVotesData[idx].getData()
                for description in data:
                    if description['link'] in films_links:
                        k = films_links.index(description['link'])
                        table[k][idx] = description['vote']
                    else:
                        films_links.append(description['link'])
                        films_names.append(description['nameRus'])
                        table.append(['' for userVotesData in self.usersVotesData])
                        table[-1][idx] = description['vote']

            def getDataAboutVotes(votes):
                s_all = 0
                s_sum = 0
                s_zero = 0
                for idx in xrange(1, len(votes)):
                    if votes[idx] != '':
                        s_all += 1
                        s_sum += int(votes[idx])
                        if votes[idx] == '0':
                            s_zero += 1
                first = 1 if votes[1] != '' else 0

                return (s_all, s_sum, s_zero, first)

            def sortFunctionN1(votes):
                (s_all, s_sum, s_zero, first) = getDataAboutVotes(votes)
                answer = 0
                if s_all != 1:
                    answer = (s_all, first, s_sum)
                else:
                    answer = (s_all, 1-first, s_sum)
                return answer

            def sortFunctionN2(votes):
                (s_all, s_sum, s_zero, first) = getDataAboutVotes(votes)
                avg = 0 if (s_all == s_zero) else float(s_sum) / float(s_all - s_zero)
                if s_all != 1:
                    answer = (avg, s_all, -s_zero, first)
                else:
                    answer = (avg, s_all, -s_zero, 1-first)
                return answer


            for idx in xrange(len(table)):
                table[idx] = [films_names[idx]] + table[idx]

            if sortFunctionV == 1:
                table.sort(key=sortFunctionN1, reverse=True)
            elif sortFunctionV == 2:
                table.sort(key=sortFunctionN2, reverse=True)
            else:
                raise ValueError

            sheet = self.book.add_sheet('Comparable V' + str(sortFunctionV))
            row = sheet.row(0)
            row.write(0, 'Films')
            [row.write(i + 1, nicks[i]) for i in xrange(len(nicks))]

            for i in xrange(len(table)):
                row = sheet.row(i + 1)
                [row.write(j, table[i][j]) for j in xrange(len(table[i]))]

        self.book = xlwt.Workbook()

        if len(self.usersVotesData) > 1:
            if type(sorts) != list:
                sorts = [sorts]
            for x in sorts:
                saveComparatorPage(x)
    
        for userVotesData in self.usersVotesData:
            savePersonalPage(userVotesData)
        
        self.book.save(filename)
