import sys, json
import urllib2,re,urllib
import pdb
from django.core.cache import get_cache
import MySQLdb

# CircleGesture [{"center":[-12.2686,125.568,-23.6326],"normal":[0.0901181,0.00440694,-0.995921],
# "progress":1.03339,"radius":22.953,"id":39,"handIds":[42],"pointableIds":[18],"duration":524417,"state":"stop","type":"circle"}]

jsons = "[{\"position\":[6.25641,114.305,-15.591],\"direction\":[0.226298,-0.973463,-0.034035],\"progress\":1,\"id\":46,\"handIds\":[96],\"pointableIds\":[68],\"duration\":108158,\"state\":\"stop\",\"type\":\"keyTap\"}]"

# SwipeGesture [{"startPosition":[0.521091,370.012,76.9022],"position":[-158.064,71.3015,102.012],
# "direction":[-0.475146,-0.871916,0.118318],"speed":1381.22,"id":48,"handIds":[53],"pointableIds":[100],"duration":108320,"state":"stop","type":"swipe"}]

# fast tempo: fast	very fast   medium tempo: medium slow	medium fast   slow tempo: slow	very slow
r = get_cache('events')

def getNext_Music_Info(json,song_object):  # main function
	responseJson = json
	response = []  # output file: singer,song
	rating = [song_object.first,song_object.second]
	gesture = responseJson["type"]
	if gesture == "circle":# circle, big means like slow pace of this singer
		radius = responseJson["radius"]
		if float(radius) >= 100:
			rate = upgrade(rate,-1)
		else:
			rate = upgrade(rate,1)
		return fetch_next_song(song_object.artist,rate[0],rate[1])
	elif gesture == "keyTap": # keytap means we do not like this kind of singer
		random_singer = get_random_non_similar(song_object.artist)
		return fetch_next_song(random_singer,'','')
	else: # swipe
                pdb.set_trace()
		y_axis = responseJson["direction"].split(',')[1]
		speed = responseJson["speed"]
		level = get_quality(speed)
		if y_axis < 0:
			level *= -1
		rate = upgrade(rating,level)
		return fetch_next_song('',rate[0],rate[1])

def getNosimilar_singer(singer): 
	response = r._client.get(singer)
	similar_list = eval(response)
	return similar_list

def get_total_singer_list(singer):
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='pan',port=3306)
	cur = conn.cursor()
	roster = []
	count = cur.execute("select c.name from events_artist c where c.name <> %s", str(singer))
	result = cur.fetchall()
	for r in result:
		roster.append(r)
	conn.commit()
	cur.close()
	conn.close()
	return roster

def fetch_next_song(artist,first,second):
	conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='pan',port=3306)
	cur = conn.cursor()
	if artist != '' and first != '' and second != '':
		print 'playing in 1'
		count = cur.execute("select c.song from events_songs c where c.first = %s and c.second = %s and c.artist= %s",(first,second,artist))
	elif artist == '':
		print 'playing in 2'
		count = cur.execute("select c.song from events_songs c where c.first = %s and c.second = %s",(first,second))
	else :
		print 'playing in 3'
		count = cur.execute("select c.song from events_songs c where c.artist = %s", artist)
	result = cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	return result[0]

def get_random_non_similar(singer):
        pdb.set_trace()
	similar = getNosimilar_singer(singer)
	roster = get_total_singer_list(singer)
	similar = set(roster)-set(similar)
	random_singer = similar[random.random()*len(similar)]
	return random_singer

def get_quality(speed):
	level = 0
	if speed >= 0 and speed < 30:
		level = 1
	elif speed >= 30 and speed < 60:
		level = 2
	elif speed >= 60 and speed < 90:
		level = 3
	elif speed >= 90 and speed < 120:
		level = 4
	elif speed >= 120 and speed < 150:
		level = 5
	elif speed >= 150 and speed < 180:
		level = 6
	else:
		level = 7
	return level

def upgrate(rate,single):
 	ratings = {}
 	rating = [['slow tempo','very slow'],['slow tempo','slow']
 	,['medium tempo','medium slow'],['medium tempo','static'],
 	['medium tempo','medium fast'],['fast tempo','fast'],['fast tempo','very fast']]
 	i = 1
 	for item in rating:
 		ratings[i] = item
 		i += 1
 	keys = ratings.keys()
 	values = ratings.values()
 	if (single > 0): #upgrade
 		if rate in values:
 			if values.index(rate) == 7:
 				return rate
 			else:
 				try:
 					new_index = keys[values.index(rate)]+single
 					if new_index > 7:
 						return ratings[7]
 					return ratings[new_index]
 					# values.index(ratings[rate]+1)]
 				except Exception,e:
 					print e
 	else:  #degrade
 		if rate in values:
 			if values.index(rate) == 0:
 				return rate
 			else:
 				try:
 					# return keys[values.index(ratings[rate]-1)]
 					new_index = keys[values.index(rate)]+single
 					if new_index < 0:
 						return ratings[0]
 					return ratings[new_index]
 				except Exception,e:
 					print e
# rate = ['slow tempo','very slow']
# print upgrate(rate,-3)
# print get_total_singer_list('Fergie')
# print fetch_next_song('','Medium Tempo','Medium Slow')
# ddata = eval(jsons)
# print type(ddata[0])
# print ddata[0]["type"]
# getNosimilar_singer('Lady Gaga')

