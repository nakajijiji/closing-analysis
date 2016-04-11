import sys,urllib2,json,codecs
from bs4 import BeautifulSoup

BASE = "http://profile.yahoo.co.jp/industry/"
COLUMN_MAP = { 0 : "code", 1 : "name", 2 : "detail"}


def fetch(url):
	html = ""
	results = []
	try: 
	  html = urllib2.urlopen(url)
	except urllib2.URLError, e:
	  return results
	soup = BeautifulSoup(html, "html.parser")
	trs = soup.select("table")[2].select("tr")
	first = True
	for tr in trs:
		if first:
			first = False
			continue
		result = {}
		for index, td in enumerate(tr.select("td")):
			if index == 3:
			  break
			key = COLUMN_MAP[index]
			result[key] = td.get_text()
		results.append(result)
	return results

def url(industry, index):
	return BASE + industry + "/" + industry + str(index) + ".html"

industry = sys.argv[1]

output = ""

if len(sys.argv) > 2:
	output = sys.argv[2]

index = 1

results = []
while(True):
	items = fetch(url(industry, index))
	if len(items) == 0:
		break
	results.extend(items)
	index = index + 1

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for r in results:
	print json.dumps(r, ensure_ascii=False)

