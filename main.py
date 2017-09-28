#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Kinopoisk
import time

def run():
	ts = time.time()

	id_volodden = 6099159

	i_with_friends = Kinopoisk.CollectorUsersID([id_volodden] + Kinopoisk.UserInfo(id_volodden).getFriends(friendsUpdate = True))
	i_with_friends.removeUsersID([3047075, 14058295])
	dvp = Kinopoisk.DataVotesPresenter([Kinopoisk.UserVotesData(x).loadData() for x in i_with_friends])
	dvp.saveToXLS(filename = 'kinopoisk.data.xls', sorts = [1, 2])

	print 'Done'
	print (time.time() - ts), 'seconds'

def v():

	from matplotlib import pylab as plt
	
	vd = Kinopoisk.UserVotesData(6099159).loadData(isPrint = False).getData()
	vd.reverse()

	ks = 0.0
	ss = 0.0
	votes_a = []

	for x in vd:
	    vote = int(x['vote'])
	    if vote > 0:
	        ks += 1
	        ss += vote

	        votes_a.append(ss / ks)

	fig = plt.figure()
	plt.plot(range(len(votes_a)), votes_a)
	fig.savefig('graph.png')
	plt.show()

def loadTop():
    t = time.time()
    
    top = Kinopoisk.TopStats()
    top.loadData(days = 20)
    top.saveToXLS()
    
    print time.time() - t

if __name__ == "__main__":
	print '\nRun:\n'
	run()
	print '\nLoadTop:\n'
	loadTop()
