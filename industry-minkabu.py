# -*- coding: utf-8 -*-
import sys,urllib2,json,codecs
from bs4 import BeautifulSoup

BASE = "http://minkabu.jp/stock/nomurasitemap/"
COLUMN_MAP = { 0 : "code", 1 : u"名称"}

def manipulate(item):
# consistency with yahoo page
	item[u"詳細"] = None

def fetch(url):
	html = ""
	results = []
	try: 
	  html = urllib2.urlopen(url)
	except urllib2.URLError, e:
	  return results
	soup = BeautifulSoup(html, "html.parser")
	if len(soup.select("#contents table")) < 2:
		return results

	trs = soup.select("#contents table")[1].select("tr")
	first = True
	for tr in trs:
		if first:
			first = False
			continue
		result = {}
		for index, td in enumerate(tr.select("td")):
			if index == 2:
			  break
			key = COLUMN_MAP[index]
			result[key] = td.get_text()
		manipulate(result)
		results.append(result)
	return results

def url(industry, index):
	return BASE + id + "?page=" + str(index)

id = sys.argv[1]

index = 1

results = []
while(True):
	items = fetch(url(id, index))
	if len(items) == 0:
		break
	results.extend(items)
	index = index + 1

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for r in results:
	print json.dumps(r, ensure_ascii=False)

