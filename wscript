# -*- coding: utf-8 -*-
# This is an example script
APPNAME = 'example-project'
VERSION = '0.0.1'
INDUSTRY = "insurer"

srcdir = '.'
blddir = 'build'

def set_options(opt):
	return

def configure(conf):
	return

def build(bld):
	bld(source='industry.py', target='industry', rule='python ${SRC} ' + INDUSTRY + ' > ${TGT}')
	bld(source='merge-closing.py closing.py industry', target='closing', rule='python ${SRC} > ${TGT}')
	bld(source='closing', target='closing.csv', rule='cat ${SRC} | jq -r \'select(.term == "前期") | [."code", ."name", ."売上高"] | @csv\' > ${TGT}') 
	return

def shutdown(ctx):
	return
