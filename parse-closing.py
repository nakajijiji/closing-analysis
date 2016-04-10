# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys,urllib2,json

BASE = "http://profile.yahoo.co.jp/"
INDEPENDENT = BASE + "independent/"
CONSOLIDATE = BASE + "consolidate/"
KEY_MAP = {u"　" : "term"}

def manipulate(index):
	return index % 4 

def parse(url):
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html, "html.parser")
	results = [{}, {}, {}]
	trs = soup.select("table.yjMt")[0].select("tr")
	first = True
	for tr in trs:
		tds = tr.select("td")
		key = ""
		for index, td in enumerate(tds):
		  # manipulation for broken html in yahoo website
			index = manipulate(index)	
			if index == 0:
				key = td.get_text()
				if key in KEY_MAP:
					key = KEY_MAP[key]
				continue
			results[index - 1][key] = td.get_text()
	return results

def filter(items):
	results = []
	for item in items:
		if item[u"決算期"] == '---':
			continue
		results.append(item)
	return results

def post_process(items, code):
	for item in items:
		item["code"] = code

code = sys.argv[1]

url = CONSOLIDATE + code
results = filter(parse(url))

if len(results) == 0:
	url = INDEPENDENT + code
	results = filter(parse(url))

post_process(results, code)

for r in results:
	print json.dumps(r, ensure_ascii=False)
