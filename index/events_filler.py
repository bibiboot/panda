#from nltk.corpus import stopwords
from events.models import Event, Meta
from django.core.cache import get_cache
from datetime import datetime
import pdb

#cachedStopWords = stopwords.words("english")

class EventsFiller():
    def __init__(self):
        self.r = get_cache('events')
        self.r._client.flushdb()

    def today(self, da):
        month = str(da.month)
        day = str(da.day)
        if da.month<=9:
            month='0'+month
        if da.day<=9:
            day = '0'+day
    
        to = str(da.year)+''+month+''+day
        return int(to)

    def not_allowed(self, d):
        if d.typeG == 'URL':
            return True
        if d.exact.find("www")>=0:
            return True
        if d.exact.find("http")>=0:
            return True
        if d.exact.find("@")>=0:
            return True
        if d.typeG == 'Person':
            return True
        if d.typeG == 'PersonCareer':
            return True
        if d.exact.strip() == "":
            return True
        if len(d.exact) > 100:
            return True
        return False

    def fetch_meta(self, eventid):
        result = {}
        for d in Meta.objects.filter(eventid=eventid):
            if d.exact is not '':
                if d.categoryName.strip() != "" and d.categoryName != "Law_Crime":
                     category = str(d.categoryName).strip()
                     result[category] = 'Category'
                if self.not_allowed(d):
                    continue
                value = str((d.exact.strip()).title())
                #value = value.replace("#", "")
                #value = value.replace("/", " ")
                if value.find("Food")>=0:
                     print value
                     result['Food'] = 'Category'
                result[value] = 'Entity'
        return result

    def setup(self): 
        """
        Set up the data store
        """
        #sentences = [ "Take out the trash", "Talk to the school bus driver" ]
        now = self.today(datetime.now())
        for e in Event.objects.all().order_by('-start_time'):
            ct = self.today(e.start_time)
            #print e.name 
            if ct < now:
                continue
            sentence = e.description
            #sentence = ' '.join([word for word in sentence.split() if word not in cachedStopWords])

            index = int(e.event_id)
            #sentence = "%s : %s : %s : %s" % (attr.name, attr.suburb, attr.city, attr.state)
            #sentence = dmp.msg
            meta = self.fetch_meta(index)
            name = e.name
            loc = e.location
            lat = e.latitude
            lon = e.longitude
            ctime = e.start_time
            city = e.city
            utime = int(ctime.strftime("%s"))
            
            sentence_temp = "%s %s %s %s"%(sentence.lower(), name.lower(), loc.lower(), city.lower())
            #print 'Adding %s' % sentence
            self.addSentence(sentence, index)
            self.addMeta(index, name, ctime, lat, lon, loc, sentence, city, meta);
            self.addWordPrefix(sentence_temp, index, utime)

    def addSentence(self, sentence, hashes):
        """
        Add the complete sentence in the hashes
        """
        self.r._client.hset('task',hashes, sentence)

    def addMeta(self, hashes, name, ctime, lat, lon, loc, desc, city, meta):
        """
        Add the complete sentence in the hashes
        """
        self.r._client.hset(hashes, 'n', name)
        self.r._client.hset(hashes, 'c', ctime)
        self.r._client.hset(hashes, 'lt', lat)
        self.r._client.hset(hashes, 'ln', lon)
        self.r._client.hset(hashes, 'lc', loc)
        self.r._client.hset(hashes, 'd', desc)
        self.r._client.hset(hashes, 'cy', city)
        self.r._client.hset(hashes, 'mt', meta)

    def addWordPrefix(self, sentence, hashes, ctime):
        """
        Adding the prefixes in the sorted set
        """
        self.r._client.zadd('total', hashes, ctime)
        for word in sentence.split(' '):
            for index,letter in enumerate(word.strip()):
                # Deletermin the prefix
                if index < 3:
                    continue
                prefix = word[:index+1]
                # Add the prefix to the set along with the sentence hashes
                #print 'Adding task:%s' % prefix

                #print ('task:%s'%prefix, hashes, ctime)
                self.r._client.zadd('t:%s'%prefix, hashes, ctime)


a = EventsFiller()
a.setup()
