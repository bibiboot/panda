import pdb
import re
import random
import logging
import simplejson
from datetime import datetime
from operator import itemgetter
from django.http import HttpResponse
from django.template import RequestContext
from django.core.cache import get_cache, cache
from django.shortcuts import render_to_response
from events.models import Songs
from lib.mem import *
from gesture import *


EXPIRY_TIME = 100000
rv = get_cache('events')

logg = logging.getLogger("travelLogger")
logg_stats = logging.getLogger("travelLoggerSTATS")

def make_request_json(request):
    data = {}
    data['position'] = request.GET.get('position', None)
    data['direction'] = request.GET.get('direction', None)
    data['progress'] = request.GET.get('progress', None)
    data['handIds'] = request.GET.get('handIds', None)
    data['pointableIds'] = request.GET.get('pointableIds', None)
    data['state'] = request.GET.get('state', None)
    data['type'] = request.GET.get('type', None)
    data['songid'] = request.GET.get('songid', None)
    return data

def getKey(artist):
    artist = artist.replace(" ", "_")
    return "%s_info"%(artist)

def get_artist_info(artist):
    data = rv._client.get(getKey(artist))
    return eval(data)

def build_artist_info_response(data, songid, song, artist):
    data['tempo'] = "['Tempo1', 'Tempo2']"
    data['info'] ="XXXX"
    data['url'] = 'YYY'
    result = build_response(artist, song, eval(data['era']), eval(data['genre']), eval(data['tempo']), eval(data['origin']), data['url'], data['info'], songid)
    return result 

def build_response(artist, song,
                   eras, genres,
                   tempos, 
                   cities,
                    url,
                    info, songid):
    data = [str(artist), 
            str(song),
            eras[0], eras[1],
            genres[0], genres[1],
            tempos[0], tempos[1],
            cities[0], cities[1],
            url,
            info, str(songid)]
    return data
 
def home(request):
    pdb.set_trace()
    data = logic_template()
    data = rv._client.lrange('random', 70, 71)
    songid, song, artist = eval(data[0])
    data = get_artist_info(artist)
    result = build_artist_info_response(data, songid, song, artist)
    
    return render_to_response('home/events.html',{'data': result }, RequestContext(request, { }) )

def homenext(request):
    """
    When user hits home page, 
    """
    pdb.set_trace()
    try:
        logg_stats.info("Events\t%s\tHome" % ( request.user.username))
        req_data = make_request_json(request)
        song_object = Songs.objects.filter(sid=req_data['songid'])[0]
        song_name = getNext_Music_Info(req_data, song_object)
        print song_name
        
        return HttpResponse(req_data)
    except Exception,e:
        logg_stats.critical(str(e))
        return HttpResponse('{"result":"failed","desc":"No Matches Found"}')

def logic_template():
    data = ['Lady Gaga',
            'Telephone',
            '2001', '2003',
            'Pop', 'EMD', 'Dance',
            'Happy', 'Sad',
            'Rome', 'Italy',
            'http://akamai-b.cdn.cddbp.net/cds/2.0/image-artist/79BD/D0F7/08E9/8855_medium_front.jpg',
            'I am good']
    return data

def logic():
    #Return next song to play based on gesture
    pass

