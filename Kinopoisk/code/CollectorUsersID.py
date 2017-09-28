#!/usr/bin/python
# -*- coding: UTF-8 -*-

class CollectorUsersID:

    '''CollectorUsersID 
Используется для получения id пользователей, с которыми будет произведена работа.
Все id содержатся в единственном числе, дубликаты удаляются.
Итерируемый.

Может принимать в конструкторе:
1. id пользователя (как число);
2. Cсылку на профиль пользователя (строка);
3. Список, включаяющий в себя элементы вида 1 или 2.

Имеет методы:
getUsersID(data)
removeUsersID(data)
size()'''

    def __init__(self, data):
        self.usersID = []
        self.number = 0
        
        if type(data) == int or type(data) == str:
            data = [data]
        if type(data) == list:
            for id in data:
                if type(id) == int:
                    self.usersID.append(str(id))
                if type(id) == str:
                    try:
                        startIndex = id.index('user') + 5
                        endIndex = id.index('/', startIndex)
                        self.usersID.append(id[startIndex : endIndex])
                    except:
                        pass
        
        self.__removeDuplicate()

    def addUsersID(self, data):
        '''Метод addUsersID(data).
Добавляет в объект новые id пользователей.
Формат данных - как в конструкторе.'''
        self.usersID += CollectorUsersID(data).usersID
        self.__removeDuplicate()
    
    def removeUsersID(self, data):
        '''Метод removeUsersID(data).
Удаляет переданный id пользователя из объекта, если они там имелись.
Формат данных - как в конструкторе.'''
        removedUsersID = CollectorUsersID(data)
        for userID in removedUsersID.usersID:
            try:
                self.usersID.remove(userID)
            except:
                pass

    def __removeDuplicate(self):
        if len(self.usersID) > 1:
            
            id_index = 0
            while id_index < len(self.usersID):
                
                id = self.usersID[id_index]
                
                copiesNumber = self.usersID.count(id)
                while copiesNumber > 1:
                    self.usersID.pop(self.usersID.index(id, id_index + 1))
                    copiesNumber -= 1
                    
                id_index += 1

    def size(self):
        '''Метод size().
Возвращает количество id пользователей.'''
        return len(self.usersID)
            
    def __iter__(self):
        return self
    
    def next(self):
        if self.number < self.size():
            self.number += 1
            return self.usersID[self.number - 1]
        self.number = 0
        raise StopIteration
