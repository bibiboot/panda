import sys, pygn, json
import urllib2,re,urllib
import pdb
import xml.etree.ElementTree
from django.core.cache import get_cache
from events.models import Songs, Artist
import redis
import MySQLdb
##user info
clientID = '8815616-776914A742B081EE5CD62AFEC4832AD6' # Enter your Client ID from developer.gracenote.com here
userID = '263552150766199473-C1C2A1AD1EADCB34D85E39CBDF52D34D' # Get a User ID from pygn.register() - Only register once per end-user
last_fm_key = '420cfad98109ee4c043dc082bcdd494f'
last_fm_secret = 'a03e99cd9b015dee314d151f45645683'

r = get_cache('events')
	


def get_all_artists(artist,total):
	sim_list = get_similar_artist(artist)
	r._client.set(artist,sim_list)
        # sim = r._client.get(artist)
	# sim_list = eval(sim)
	if len(sim_list) == 0:
		print "No redis record"
		sim_list = get_similar_artist(artist)
		r._client.set(artist,sim_list) # insert current singer into redis
	if len(sim_list) == 0:
		print "wrong singer name"
		return sim_list
	# for artist in sim_list:
	# 	if artist in total:
	# 		continue
	# 	try:
	# 		avail_artist = Artist.objects.filter(name=artist)
	# 		if len(avail_artist) == 1: 
	# 			continue  	
	# 		search_artist_info(artist) # insert current singer into db
	# 	except Exception, e:
	# 		print 'Unable to add ' + artist
	# 		print e
	return sim_list

def get_all_artists_similar():
	for artist in Artist.objects.all():
		try:
			print remove_extra(artist.name)
			print get_similar_artist(artist.name, 'SIMILAR ARTIST')
		except Exception, e:
			print 'Unable to get similar ' + artist.name
			print e

def remove_extra(word):
	word = word.replace('\\u00','')
	word = word.replace('\u00','')
	return word

#Library calls starts here

def get_similar_artist(artist_name):
	#http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=420cfad98109ee4c043dc082bcdd494f&format=json
	persons = []
	url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar'
	values = {'artist' : artist_name,
		  	  'api_key':last_fm_key,
		  	  'format':'json'}
	try:
		data = urllib.urlencode(values)
		req = urllib2.Request(url,data)
		response = urllib2.urlopen(req)
		responseJSON = response.read()
		ddata = eval(responseJSON)
		similars = ddata["similarartists"]["artist"]
		for artist in similars:
			persons.append(remove_extra(artist["name"]))
			persons = list(set(persons))
			# r._client.set(artist_name, artist['name']) 
		r._client.set(artist_name,persons) 
	except Exception,e:
		print e
		pass   
	return persons


def search_artist_info(artist_name):
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name)
	newjson = json.dumps(result,sort_keys=True,indent=4)
	ddata = eval(newjson)
	artist_era = []
	artist_img = ddata["artist_image_url"]
	artist_origin = []
	artist_type = []
	artist_genre = []
	artist_mood = []
	for x,item in ddata["artist_era"].items():
		artist_era.append(item["TEXT"])
	for x, item in ddata["artist_origin"].items():
		artist_origin.append(item["TEXT"])
	for x, item in ddata["artist_type"].items():
		artist_type.append(item["TEXT"])
	for x, item in ddata["genre"].items():
		artist_genre.append(item["TEXT"])
	for x, item in ddata["mood"].items():
		artist_mood.append(item["TEXT"])
	Artist.objects.create(name=artist_name, era=artist_era, origin=artist_origin, genre=artist_genre, mood=artist_mood, img=artist_img)      

def search_albums(artist_name):
	albums = []
	result = pygn.get_discography(clientID=clientID, userID=userID, artist=artist_name)
	newjson = json.dumps(result, sort_keys=True, indent=4)
	ddata = eval(newjson)
	for item in ddata:
		albums.append(item["album_title"])
	return albums

def search_songs(artist_name,albums):
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name, album=albums)
	return titles

def search_quality(artist_name,track_name):
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name, track=track_name)
	newjson = json.dumps(result, sort_keys=True, indent=4) 
	ddata = eval(newjson)
	first_layer = ddata["tempo"]["1"]["TEXT"]
	second_layer = ddata["tempo"]["2"]["TEXT"]
	return first_layer,second_layer

def total_work(artists):
	LOG = open('log.dat','w')
	for artist in artists:
		duplicate = []
		albums = search_albums(artist)
		for album in albums:
			songs = search_songs(artist,album)
			for song in songs:
				if song not in duplicate:
					duplicate.append(song)
					try:
						first,second = search_quality(artist,str(song))
						print artist+"\t"+song+"\t"+first+"\t"+second
						Songs.objects.create(artist=artist, song=song, first=first, second=second)
					except Exception,e:
						LOG.write(str(e)+"\n")
						print e
						pass
def make_database(curr,total):
	similar_list = []
	persons = set()
	for person in curr:
		person = remove_extra(person)
		if   person not in total: # not duplicate artist
			similar_list = get_all_artists(person,total)
			if len(similar_list) == 0:
				print "wrong singer name"
				continue
			persons = persons | set(similar_list)
			total.append(person)
			list1 = []
			list1.append(person)
			total_work(list1)
	return list(persons),total



def main():
	curr = ['Lady Gaga'] # seed list
	total = []
	# iteration = 10
	# for i in range (iteration):
	curr,total = make_database(curr,total)

# main()
# get_similar_artist('Lady Gaga')
# init = ['Lady Gaga']
total = []
similar_list = get_all_artists('Lady Gaga',total)
for item in similar_list:
	get_all_artists(item,total)
# print r._client.get('Rihanna')
