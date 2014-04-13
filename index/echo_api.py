import pdb
import time
from urllib2 import urlopen
from events.models import Songs

URL = "http://developer.echonest.com/api/v4/song/search?api_key=GECI6ZFFHCTZFO79F&format=json&results=20&artist=%s&title=%s&bucket=id:rdio-US&bucket=tracks"

def dummy():
    return {"response": {"status": {"version": "4.2", "code": 0, "message": "Success"}, "songs": [{"title": "Karma Police", "artist_name": "Radiohead", "artist_foreign_ids": [{"catalog": "rdio-US", "foreign_id": "rdio-US:artist:r91318"}], "tracks": [{"foreign_release_id": "rdio-US:release:a195317", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2351369", "id": "TRHRCSU136E7A7FF4D"}, {"foreign_release_id": "rdio-US:release:a195303", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2351161", "id": "TRLBOBI136E7A7EB8B"}, {"foreign_release_id": "rdio-US:release:a168687", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2025687", "id": "TRHOIEA136E7264F8E"}, {"foreign_release_id": "rdio-US:release:a168685", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2025654", "id": "TRIONEW136E7264D50"}, {"foreign_release_id": "rdio-US:release:a171828", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2062843", "id": "TREJGSZ136E733530A"}, {"foreign_release_id": "rdio-US:release:a1976692", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t21301293", "id": "TRNYDJD13A958F71F5"}, {"foreign_release_id": "rdio-US:release:a3479517", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t36923964", "id": "TREEXLH14151244124"}, {"foreign_release_id": "rdio-US:release:a3479117", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t36916623", "id": "TRBVDNY141512455EA"}, {"foreign_release_id": "rdio-US:release:a3653532", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t38872450", "id": "TRXDAJZ14200AA096A"}, {"foreign_release_id": "rdio-US:release:a196556", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t2366171", "id": "TRTHLTX136E7AE1240"}, {"foreign_release_id": "rdio-US:release:a3999695", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t42705402", "id": "TRVGCHS143C7A7020A"}, {"foreign_release_id": "rdio-US:release:a3999381", "catalog": "rdio-US", "foreign_id": "rdio-US:track:t42701213", "id": "TRHBHZG143C7A6ACF3"}], "artist_id": "ARH6W4X1187B99274F", "id": "SOHJOLH12A6310DFE5"}]}}

def no_required(s):
    try:
        print s.sid
        d = int(s.sid)
        return False
    except Exception,e:
        return True

def call_api(artist, song):
    artist=artist.replace(' ', '%20')
    song=song.replace(' ', '%20')
    baseurl = URL % (artist, song)
    print baseurl
    html=urlopen(baseurl)
    s=html.read()
    #return dummy()
    return s

def get_id(data):
    data = eval(data)
    for s in data['response']['songs']:
        if len(s['tracks'])!=0:
            return s['tracks'][0]['foreign_id'].split(':')[-1]

def is_duplicate(s):
    list_s = Songs.objects.filter(song=s.song).filter(artist=s.artist)
    if len(list_s)>1:
        return True
    return False

def run():
    for s in Songs.objects.all():
        try:
            pdb.set_trace()
            if is_duplicate(s):
                s.delete()
                continue
            if no_required(s): continue
            data = call_api(s.artist, s.song)
            sid = get_id(data)
            print s.song, s.artist
            s.sid = sid
            s.save()
            time.sleep(1)
        except Exception,e:
            print str(e)

def test():
    data = call_api('Lady Gaga', 'Poker Face')
    print get_id(data)

run()
