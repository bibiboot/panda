from urllib2 import urlopen
import MySQLdb

def insert_data(dept,cname,prefix,code,insname,term,year,intro):
	pid=cname+"_"+prefix+"_"+code+"_"+insname+"_"+term+"_"+str(year)
	querystring="Insert into suggest_course  values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(pid,dept,cname,prefix,code,insname,term,year,intro)
	#print querystring
	#querytemp=querystring.replace("suggest_dump","suggest_temp")
	try:
		db=MySQLdb.connect(host="localhost",user="root",passwd="root",db="em")
	   	cur=db.cursor()
		a="printval"
		cur.execute(querystring)
		#cur.execute(querytemp)
        	cur.close()
       		db.commit()
        	db.close()
	except MySQLdb.Error,e:	  
		pass
	

def extracthelp_data(d,dept):
        prefix=d['CourseData']['prefix']
	code=d['CourseData']['number']
	cname=d['CourseData']['title']
	intro=d['CourseData']['description']
	term="fall"
	year=2014
	print prefix
	print code
	print cname
	print intro
	print dept
	print(type(d['CourseData']['SectionData']))
	if(isinstance(d['CourseData']['SectionData'],dict)):
		if(isinstance(d['CourseData']['SectionData']['instructor'],dict)):
			firstName=d['CourseData']['SectionData']['instructor']['first_name']
			insname=str(firstName)+" "+str(d['CourseData']['SectionData']['instructor']['last_name'])
			insert_data(dept,cname,prefix,code,insname,term,year,intro)
		else:
			for v in d['CourseData']['SectionData']['instructor']:
				insname=str(v['first_name'])+" "+str(v['last_name'])
				insert_data(dept,cname,prefix,code,insname,term,year,intro)
				
	else:
		for ins in d['CourseData']['SectionData']:
			if(isinstance(ins['instructor'],dict)):
				insname=str(ins['instructor']['first_name'])+" "+str(ins['instructor']['last_name'])
				insert_data(dept,cname,prefix,code,insname,term,year,intro)
			else:
				for b in ins['instructor']:
					insname=str(b['first_name'])+" "+str(b['last_name'])
					insert_data(dept,cname,prefix,code,insname,term,year,intro)
		
	#print intro
        #username=d['from']['name']
        #userid=d['from']['id']
        #gname= d['to']['data'][-1]['name']
	#if(d.has_key('message')):
	#	pmessage= d['message']
	#else:
	#	pmessage="" 
	#print pmessage
        #ctime=d['created_time']
	#utime=d['updated_time']
	#pmessage=pmessage.replace("(","")
	#pmessage=pmessage.replace(")","")
	#pmessage=pmessage.replace("'","")
       	#username=username.replace("'","")   
        #insert_data(pid,gname,gid,pmessage,username,userid,ctime,utime)
			             
def extract_data(dic):
	dept=dic['Dept_Info']['department']
        di=dic["OfferedCourses"]
	if(di.has_key('course')):
		if(isinstance(di['course'],list)):
			for d in di['course']:
				extracthelp_data(d,dept)
		else:
			extracthelp_data(di['course'],dept)
	

def get_data(url):
	print(url)
	html=urlopen(url)
	s=html.read()
	s=s.replace("\n","\\n")
	s=s.replace("false","False")
	s=s.replace("true","True")
	s=s.replace("null","")
	dic=eval(s)
	#print(type(dic))
	#print type(dic)
	extract_data(dic)


def get_parentdata(baseurl):
	print(baseurl)
	html=urlopen(baseurl)
	s=html.read()
	s=s.replace("\n","\\n")
	s=s.replace("false","False")
	s=s.replace("true","True")
	s=s.replace("null","")
	dic=eval(s)
	#de=dic['department']
	#print(type(de))
	codelist=[]
	for di in dic['department']:
		#print(type(di['department']))
		#print(len(di))
		if(di.has_key('department')):
			if(isinstance(di['department'],list)):
				for d in  di['department']:
					codelist.append(d['code'])
			else:
				codelist.append(di['department']['code'])
		
	for code in codelist:
		url="http://web-app.usc.edu/ws/soc/api/classes/"+code+"/20142"
		get_data(url)	
		
		
	
	


import pdb
baseurl="http://web-app.usc.edu/ws/soc/api/depts/20142"
get_parentdata(baseurl)
url="http://web-app.usc.edu/ws/soc/api/classes/csci/20142"
#get_data(url)






























































































