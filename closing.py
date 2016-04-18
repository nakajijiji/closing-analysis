# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys,urllib2,json,codecs

BASE = "http://profile.yahoo.co.jp/"
INDEPENDENT = BASE + "independent/"
CONSOLIDATE = BASE + "consolidate/"
KEY_MAP = {u"　" : u"期"}
IGNORE_KEYS = [u"配当区分", u"発行済み株式総数", u"1株配当"]

def manipulate(index):
	return index % 4 

def normalize_key(text):
	if text.find(u"（") != -1:
		return text[:text.find(u"（")]
	return text

def normalize_value(text):
	if text.endswith(u'百万円'):
		text = text.replace(',', '')
		try:
			text = int(text.replace(u'百万円', '000000'))
		except:
			return None
	elif text.endswith(u'円'):
		try:
			text = float(text.replace(u'円', ''))
		except:
			return None
	elif text.endswith('%'):
		try:
			text = round(float(text.replace('%', '')) * 0.01, 4)
		except:
			return None
	return text

def parse(url):
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html, "html.parser")
	results = [{}, {}, {}]
	if len(soup.select("table.yjMt")) < 1:
		return results
	trs = soup.select("table.yjMt")[0].select("tr")
	first = True
	for tr in trs:
		tds = tr.select("td")
		key = ""
		for index, td in enumerate(tds):
		  # manipulation for broken html in yahoo website
			index = manipulate(index)	
			if index == 0:
				key = normalize_key(td.get_text())
				if key in IGNORE_KEYS:
					break
				elif key in KEY_MAP:
					key = KEY_MAP[key]
				continue
			results[index - 1][key] = normalize_value(td.get_text())
	return results

def filter(items):
	results = []
	for item in items:
		if not u"計算機" in item or item[u"決算期"] == '---':
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

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for r in results:
	print(json.dumps(r, sort_keys=True, ensure_ascii=False))
