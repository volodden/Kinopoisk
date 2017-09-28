#!/usr/bin/python
# -*- coding: UTF-8 -*-

from init2 import *

class TopStats:

	'''AboutTop.
Создан исключительно для статистики фильмов из Топ250 Кинопоиска.

Имеет методы:
loadData()'''

	def __init__(self):

		self.daysData = []
		self.films = 250

	def loadData(self, days = 10):

		'''Метод loadData().
Загружает данные из Топ250 Кинопоиска.

Параметр days позволяет задать нужно количество дней, по умолчанию 10.'''

		if days < 1:
			days = 10

		link = settings.getMainLink() + 'top/'
		
		self.daysData = []

		date = 'Today'

		for d in xrange(days):

			page = settings.getSession().get(link).text

			self.daysData.append((date, []))

			filmsSoup = bs4.BeautifulSoup(page, 'lxml')
			
			pday = filmsSoup.find_all('a', {'class': 'all'})
			for x in pday:
				if u"предыдущий" in x.string:
					pday = x
					break

			filmsSoup = filmsSoup.find_all('a', {'class' : 'all' })#, 'data-popup-info' : 'enabled'})

			isPrev = False
			for x in xrange(len(filmsSoup)):
				try:
					if u"предыдущий" in filmsSoup[x].string:
						if isPrev:
							break
						isPrev = True
						continue
				except:
					pass

				if not isPrev or u"следующий" in filmsSoup[x].string:
					continue

				self.daysData[d][1].append(filmsSoup[x].text)

				try:
					print filmsSoup[x].find('a').text
				except:
					pass

			print 'Day', date, 'is loaded.'

			link = settings.getMainLink() + pday['href'][1:]
			date = link[link.index('day/') + 4:-6]

		self.daysData.reverse()	

	def saveToXLS(self, filename = 'top250.xls'):

		'''Метод saveToXLS().
Сохраняет ранее загруженные файлы в .xlx-таблицу.

Параметр filename позволяет указать имя файла, по умолчанию "top250.xls".'''

		if self.daysData < 1:
			return

		book = xlwt.Workbook()

		sheet = book.add_sheet('Top250')

		row = sheet.row(0)
		for j in xrange(len(self.daysData)):
			row.write(j, self.daysData[j][0])

		for i in xrange(self.films):
			row = sheet.row(i + 1)
			for j in xrange(len(self.daysData)):
				row.write(j, self.daysData[j][1][i])

		book.save(filename)
