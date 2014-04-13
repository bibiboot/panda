import sys, pygn, json
import urllib2,re,urllib
import pdb
import xml.etree.ElementTree
# import xmltodict
# import mysql
# import 
##user info
clientID = '8815616-776914A742B081EE5CD62AFEC4832AD6' # Enter your Client ID from developer.gracenote.com here
userID = '263552150766199473-C1C2A1AD1EADCB34D85E39CBDF52D34D' # Get a User ID from pygn.register() - Only register once per end-user
last_fm_key = '420cfad98109ee4c043dc082bcdd494f'
last_fm_secret = 'a03e99cd9b015dee314d151f45645683'
filename = 'music_quality.dat'
person_info = 'person.dat'
# regex = '.*?[/\/\u0].*?'

# print '\nSearch for artist "Kings of Convenience"\n'
# result = pygn.search(clientID=clientID, userID=userID, artist='Kings of Convenience')
# print json.dumps(result, sort_keys=True, indent=4)

# print '\nSearch for album "Prism" by "Katy Perry"\n'
# result = pygn.search(clientID=clientID, userID=userID, artist='Katy Perry', album='Teenage Dream')
# print json.dumps(result, sort_keys=True, indent=4)
def get_similar_artist(artist_name,keyword):
	#http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=420cfad98109ee4c043dc082bcdd494f&format=json
	persons = []
	if keyword == 'SIMILAR ARTIST':
		url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar'
		values = {'artist' : artist_name,
			  	  'api_key':last_fm_key,
			  	  'format':'json'}
		data = urllib.urlencode(values)
		req = urllib2.Request(url,data)
		response = urllib2.urlopen(req)
		responseJSON = response.read()
		ddata = eval(responseJSON)
		# print ddata
		similars = ddata["similarartists"]["artist"]
		# print similars
		for artist in similars:
			# m = re.search(regex,artist["name"])
			# if not m.group():
			# artist["name"].replace("\\00e[d]*","")
			persons.append(artist["name"])
		return persons
		# print ddata


def search_artist_info(artist_name):
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name)
	newjson = json.dumps(result,sort_keys=True,indent=4)
	ddata = eval(newjson)
	artist_era = []
	# [ddata["artist_era"]["1"]["TEXT"],ddata["artist_era"]["2"]["TEXT"]]
	artist_img = ddata["artist_image_url"]
	artist_origin = []
	artist_type = []
	artist_genre = []
	artist_mood = []
	for item in ddata["artist_era"]:
		artist_era.append(item["TEXT"])
	for item in ddata["artist_origin"]:
		artist_origin.append(item["TEXT"])
	for item in ddata["artist_type"]:
		artist_type.append(item["TEXT"])
	for item in ddata["artist_genre"]:
		artist_genre.append(item["TEXT"])
	for item in ddata["artist_mood"]:
		artist_mood.append(item["TEXT"])
	return [artist_img,artist_era,artist_name,artist_mood,artist_genre,artist_type]

def search_albums(artist_name):
	albums = []
	print '\nGetting artist discography for'+str(artist_name)+"\n"
	result = pygn.get_discography(clientID=clientID, userID=userID, artist=artist_name)
	newjson = json.dumps(result, sort_keys=True, indent=4)
	ddata = eval(newjson)
	for item in ddata:
		# if item["album_artist_name"] == artist_name:
		albums.append(item["album_title"])
	return albums
	# print albums

def search_songs(artist_name,albums):
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name, album=albums)
	return titles

def search_quality(artist_name,track_name):
	print '\nSearch for track'+artist_name+' by '+str(track_name)+"\n"
	result,titles = pygn.search(clientID=clientID, userID=userID, artist=artist_name, track=track_name)
	newjson = json.dumps(result, sort_keys=True, indent=4) 
	ddata = eval(newjson)
	first_layer = ddata["tempo"]["1"]["TEXT"]
	second_layer = ddata["tempo"]["2"]["TEXT"]
	# bpm = ddata["tempo"]["3"]["TEXT"]
	return first_layer,second_layer

def total_work(filename,artists):
	output = open(filename,'w')
	for artist in artists:
		duplicate = []
		albums = search_albums(artist)
		print albums
		for album in albums:
			songs = search_songs(artist,album)
			for song in songs:
				if song not in duplicate:
					duplicate.append(song)
					try:
						first,second = search_quality(artist,str(song))
						output.write(str(artist)+"\t"+str(song)+"\t"+str(first)+"\t"+str(second))
						output.write("\n")
                                                break
					except:
						# print 'problem on: '+str(song)
						pass
	output.close()
##### main #####
#get_similar_artist('cher')
#artists = ['Lady Gaga']
#total_work(filename,artists)

# titles = search_songs('Kate Perry','Teenage Dream')
# print titles
# first,second = search_quality('Kate Perry','Teenage Dream')
# print first
# print second
# search_songs('Kate Perry')
# albums = search_albums('Lady Gaga')
# print albums

print get_similar_artist('Lady Gaga', 'SIMILAR ARTIST')

# print '\nSearching by album TOC\n'
# result = pygn.search(clientID=clientID, userID=userID, toc='150 20512 30837 50912 64107 78357 90537 110742 126817 144657 153490 160700 175270 186830 201800 218010 237282 244062 262600 272929')
# print json.dumps(result, sort_keys=True, indent=4)

# print '\nGetting artist discography for "Daft Punk"\n'
# result = pygn.get_discography(clientID=clientID, userID=userID, artist='Daft Punk')
# print json.dumps(result, sort_keys=True, indent=4)

