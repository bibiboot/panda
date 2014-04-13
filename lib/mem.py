import logging
from django.core.cache import get_cache, cache

logg = logging.getLogger("travelLogger")
logg_stats = logging.getLogger("travelLoggerSTATS")


def get_key(key):
    return key.replace(" ", "_")

def get_data(key):
    found=False
    data = cache.get(get_key(key))
    if data:
       found=True
    logg_stats.info("Cache\tGet\t%s\t%s", key, found)
    return data

def set_data(data, key):
    data = cache.set(get_key(key), data, EXPIRY_TIME)
    logg_stats.info("Cache\tSet\t%s", key)
