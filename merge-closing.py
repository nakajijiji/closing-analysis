# -*- coding: utf-8 -*-
import subprocess,sys,codecs,json,io

script = sys.argv[1]
input = sys.argv[2]

with codecs.open(input, "r", "utf-8") as f:
	ds = []
	for l in f.readlines():
		item = json.loads(l.rstrip())
		code = item["code"]
		lines = subprocess.check_output(["python", script, str(code)]).split('\n')
		for l in lines[:len(lines) - 1]:
			d = dict(item.items() + json.loads(l).items())
			ds.append(d)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for d in ds:
	print json.dumps(d, ensure_ascii=False)
