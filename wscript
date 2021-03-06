# -*- coding: utf-8 -*-
# This is an example script
APPNAME = 'example-project'
VERSION = '0.0.1'
INDUSTRY = "50103"

srcdir = '.'
blddir = 'build'

def set_options(opt):
	return

def configure(conf):
	return

def build(bld):
	bld(source='industry-minkabu.py', target='industry', rule='python ${SRC} ' + INDUSTRY + ' > ${TGT}')
	bld(source='merge-closing.py closing.py industry', target='closing', rule='python ${SRC} > ${TGT}')
	bld(source='growth.py closing', target='closing-with-growth', rule='python ${SRC} > ${TGT}')
	bld(source='closing-with-growth', target='closing.csv', rule='(head -n1 ${SRC} | jq -r \'to_entries | [.[].key] | @csv\'; cat ${SRC} | jq -r \'select(."期"=="前期")|flatten|@csv\') > ${TGT}') 
	return

def shutdown(ctx):
	return
