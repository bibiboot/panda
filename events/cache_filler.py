from django.core.cache import get_cache
from events.models import Artist, Songs

r = get_cache('events')

def getKey(artist):
    artist = artist.replace(" ", "_")
    return "%s_info" % (artist)

def fill_artist_info():
    for a in Artist.objects.all():
        key = getKey(a.name)
        print key
        value = { 'origin': a.origin, 'genre': a.genre, 'mood': a.mood, 'era': a.era , 'name': a.name } 
        r._client.set(key, value)

def build_random_list():
    for s in Songs.objects.all():
        r._client.lpush('random', (s.sid, s.song, s.artist))

def main():
    fill_artist_info()
    build_random_list()

main()
