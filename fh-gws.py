from requests_html import HTMLSession
session=HTMLSession() 
import sys 
from urllib.parse import urlparse
import sqlite3
from sqlite3 import Error
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

database=r'./DB/webscrape.db'
conn = create_connection(database)

def save_rendered_page(page_html): 
	#comback 
	pass



def log_done(line):
	
	with open('done_logfile.txt', 'a+') as f:
		f.write(line)
		f.write("\n")

def log_append(line):
	
	with open('append_logfile.txt', 'a+') as f:
		f.write(line)
		f.write("\n")

def import_form_db(page_forms, hostname, url, path):

	try:
		form_role=page_forms.attrs['role']
	except KeyError as e: 
		form_role=''
	try:
		form_id=page_forms.attrs['id']
	except KeyError as e: 
		form_id=''
	try:
		form_name=page_forms.attrs['name']
	except KeyError as e: 
		form_name=''
	form_other=[]
	for i in page_forms.attrs:
		#print('i',i)
		if i == 'role' or i == 'id' or i == 'name':
			continue
		form_other.append(i + '=' + str(page_forms.attrs[i]))
	form_other=', '.join(form_other)

	date_time = datetime.now().strftime("%B %d, %Y %I:%M%p")
	just_date=datetime.now().strftime("%Y-%m-%d")

	sql = '''insert into app_scrape_forms select '{0}', '{1}', '{2}', '{3}','{4}', '{5}', "{6}",'{7}', '{8}'; '''.format(  hostname, url, path, form_role, form_id, form_name, form_other, date_time, just_date	  )

	#continue
	#print(sql)
	cur = conn.cursor()
	cur.executescript(sql)
	conn.commit()

def get_forms(r_html, hostname, newurl,path):
	print('Importing forms for page: ' + path)
	page_forms=r_html.find('form')
	for i in page_forms:
		import_form_db(i, hostname, newurl, path)
		

def get_links(r_html): 
	links_set=r_html.links
	links_list=sorted(list(links_set))
	
	dlink_list=[]
	for link in links_list:
		lnk=link.split('?')[0]
		if lnk not in dlink_list:
			if lnk.startswith('/') == False: 
				continue
			dlink_list.append(lnk)
		else:
			continue
	
	return dlink_list

def get_rendered_page(url): 
	r=session.get(url, verify=False) 
	print("Retrieving Links for Page: " + url)
	#give page time to load
	r.html.render(sleep=5, timeout=60)
	html=r.html
	return html

def import_links_db(hostname, url, path, link):

	date_time = datetime.now().strftime("%B %d, %Y %I:%M%p")
	just_date=datetime.now().strftime("%Y-%m-%d")

	sql = '''insert into app_scrape_links select '{0}', '{1}', '{2}', '{3}','{4}', '{5}'; '''.format(  hostname, url,path,link,date_time,just_date	  )

	#continue
	#print(sql)
	cur = conn.cursor()
	cur.executescript(sql)
	conn.commit()

def loop_other_pages(hostname):
	masterlist=['/']
	
	donelist=[]
	newlist=[]
	for path in masterlist:	
		newurl=(hostname+path)
		page_html=get_rendered_page(newurl)
		get_forms(page_html, hostname, newurl,path)
		links_to_add=get_links(page_html)
		for nl in links_to_add:
			if len(masterlist)==1 and '/' in masterlist:
				import_links_db(hostname, newurl, path, nl)
			if nl not in masterlist:
				log_append('Appending ' + nl + ' to masterlist')
				masterlist.append(nl)
                
                ##comment below to not save to SQLITE db 
				import_links_db(hostname, newurl, path, nl)
		log_done('Done: ' + path)
		donelist.append(path)
	for i in sorted(masterlist):
		print(i)


def main(): 
	
	masterlist=[]

	try:
		oUrl=urlparse(sys.argv[1])	
	except IndexError:
		print('Usage: python3 <url>')
		sys.exit(1)
	
	if oUrl.scheme == '' or not oUrl.scheme: 
		url=urlparse('https://'+ oUrl.geturl())

	hostname=url.hostname

	loop_other_pages(url.geturl())
	select_all_from_table(url.geturl())
 	 

main()

