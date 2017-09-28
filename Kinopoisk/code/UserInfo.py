#!/usr/bin/python
# -*- coding: UTF-8 -*-

from init2 import *

class UserInfo:

    '''UserInfo.
Используется для хранения данных о информации пользователе.

Может принимать в конструкторе id пользователя как число или строку.

Имеет методы:
getID()
getLink()
getNick()
getFriends()'''

    def __init__(self, id):

        if type(id) != int and type(id) != str:
            print 'UserInfo wrong format: only int or str'
            raise TypeError
        
        self.id = str(id)
        self.friends = []

        page = ''
        if settings.getMode():
            folder = os.path.join('.', self.id)
            files = os.listdir(folder)
            for f in files:
                if 'htm' in f:
                    file_r = open(os.path.join(folder, f))
                    page = file_r.read()
                    file_r.close()
                    break
        else:
            page = settings.getSession().get(self.getLink()).text
        try:
            title = bs4.BeautifulSoup(page, 'lxml').find('title').contents[0]
            start = title.index(' ') + 1
            try:
                end = title.index('-') - 1
            except:
                end = len(title)
            self.nick = title[start : end]
        except:
            print 'Error: nick not found'
            self.nick = 'None'

    def getID(self):
        '''Метод getID().
Возвращает id пользователя.'''
        return self.id

    def getLink(self):
        '''Метод getLink().
Возвращает ссылку на пользователя.'''
        return settings.getMainLink() + 'user/' + self.id
    
    def getFriends(self, friendsUpdate = False):
        '''Метод getFriends().
Возвращает список из id пользователей, являющихся другом для текущего.
Параметр friendsUpdate позволяет обновить информацию, загрузив с сайта. По умолчанию False. При первом использовании должен быть установлен True.'''
        if friendsUpdate:
            link = self.getLink() + '/community/friends/'
            page = settings.getSession().get(link).text
            sz = len('/user/')
            self.friends = [int(f.contents[1]['href'][sz : -1]) for f in bs4.BeautifulSoup(page, 'lxml').find_all('p', { 'class' : 'profile_name' })]
        if self.friends == []:
            print 'Error: use "friendsUpdate = True"'
            return self.friends
        return self.friends
    
    def getNick(self):
        '''Метод getNick().
Возвращает ник пользователя.'''
        return self.nick
