import urllib2
import random
import MySQLdb
import pprint
import pdb
from events.models import Event, Meta
from datetime import datetime

key="ne62f3m8swrsv2cvmf78rkx2"

def call(body):
    url = "http://api.opencalais.com/tag/rs/enrich"
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data=body)
    request.add_header('content-type', 'text/raw')
    request.add_header('accept', 'application/json')
    request.add_header('x-calais-licenseID', key)
    request.get_method = lambda: 'POST'
    url = opener.open(request)
    print url
    for line in url.readlines():
        result = eval(line)

    return result

def fetch():
    for e in Event.objects.all().order_by('start_time'):
        sentence = e.description
        name = e.name
        eventid = e.event_id
        d = Meta.objects.filter(eventid=str(eventid))
        if len(Meta.objects.filter(eventid=str(eventid))) is not 0:
            print "present"
            continue
        result = call(name+' '+sentence)
        #pprint.pprint(result)
        #print name+' '+sentence
        #break
        for key, value in result.items():
            if key == 'doc' or value.has_key('language'):
                continue
            insert(key, value, eventid)
            print key
            print '-------'

def insert(key, value, eventid):
   default = ''
   namer = shortnamer = tickerr = rid = default
   cid = key+'_'+str(eventid)
   eventid = eventid
   category = value.get('category', default)
   categoryName = value.get('categoryName', default)
   detection = value.get('detection', default)
   typeGroup = value.get('_typeGroup', default)
   typeG = value.get('_type', default)
   typeReference = value.get('_typeReference', default)
   score = value.get('score', default)
   classifierName = value.get('classifierName', default)
   url = value.get('url', default)
   name = value.get('name', default)
   nationality = value.get('nationality', default)
   resolutions = value.get('resolutions', default)
   resolutions_str = resolutions
   instances = value.get('instances', default)
   instances_str = instances
   if resolutions is not default:
       resolutions = resolutions[0]
       namer = resolutions.get('name', default)
       rid = resolutions.get('id', default)
       tickerr = resolutions.get('ticker', default)
       shortnamer = resolutions.get('shortname', default)

   if instances is default:
       instances = [{'suffix': default,
                     'prefix': default,
                     'detection': default,
                     'length': default,
                     'offset': default,
                     'exact' :  default }]
   else:
       pass
       #print instances
       #instances = eval(instances)
   

   for inst in instances:
       cid = cid+' '+str(random.randint(1,10))
       try:
           Meta.objects.create(cid=cid,
                           eventid=eventid,
                           category=category,
                           categoryName=categoryName,
                           detection=inst.get('detection', default),
                           typeGroup=typeGroup,
                           typeG=typeG,
                           typeReference=typeReference,
                           score=score,
                           classifierName=classifierName,
                           url=url,
                           name=name,
                           nationality=nationality,
                           resolutions=resolutions_str,
                           namer = namer,
                           tickerr = tickerr,
                           rid = rid, 
                           shortnamer = shortnamer,
                           instances=instances_str,
                           suffix=inst.get('suffix', default),
                           prefix=inst.get('prefix', default),
                           length=inst.get('length', default),
                           offset=inst.get('offset', default),
                           exact=inst.get('exact', default),
                           )
       except Exception as e:
           print "eception occured",e

fetch()
