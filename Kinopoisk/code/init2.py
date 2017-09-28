#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import bs4
import xlwt
import xlrd
import os
import time

class InitialSettings():

	'''Используемые модули:
requests
bs4
xlwt
xlrd
os
time

Имеющиеся классы:
CollectorUsersID
UserInfo
UserVotesData
DataVotesPresenter
DataVotesTablesLoader
UserFolders
TopStats'''

	def __init__(self):
		self.MAINLINK = 'https://www.kinopoisk.ru/'
		self.OFFLINE_MODE = False

		self.SESSION = requests.Session() 
		self.SESSION.headers.update({ 'Referer': self.MAINLINK,
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
			})

	def getMode(self):
		return self.OFFLINE_MODE

	def setMode(self, newMode):
		self.OFFLINE_MODE = newMode

	def printMode(self):
		print 'Current Mode is', 'offline' if self.OFFLINE_MODE else 'online'

	def getMainLink(self):
		return self.MAINLINK

	def getSession(self):
		return self.SESSION

settings = InitialSettings()
