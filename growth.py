# -*- coding: utf-8 -*-ZZ
# inputとして、code, 期順にソートされた1行1jsonの決算データを前提とします

import sys,json,codecs

SALES_KEY = u"売上高"
RETURN_KEY = u"経常利益"
SALES_TWO = u"2期前売上高"
RETURN_TWO = u"2期前経常利益"
SALES_THREE = u"3期前売上高"
RETURN_THREE = u"3期前経常利益"

def create_ifnotexists(key, item):
	if not key in item:
		item[key] = None

input = sys.argv[1]

results = []

with codecs.open(input, "r", "utf-8") as f:
	current_code = None
	current_result = None
	for l in f.readlines():
		item = json.loads(l.rstrip())
		if not current_code == item["code"]:
			current_code = item["code"]
			current_result = item
			results.append(current_result)
		if item[u"期"] == u"2期前":
			current_result[SALES_TWO] = item[SALES_KEY]
			current_result[RETURN_TWO] = item[RETURN_KEY]
		elif item[u"期"] == u"3期前":
			current_result[SALES_THREE] = item[SALES_KEY]
			current_result[RETURN_THREE] = item[RETURN_KEY]
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for result in results:
	create_ifnotexists(SALES_TWO, result)
	create_ifnotexists(RETURN_TWO, result)
	create_ifnotexists(SALES_THREE, result)
	create_ifnotexists(RETURN_THREE, result)
	print json.dumps(result, sort_keys=True, ensure_ascii=False)

