# This is an example script
APPNAME = 'example-project'
VERSION = '0.0.1'

srcdir = '.'
blddir = 'build'

def set_options(opt):
	return

def configure(conf):
	return

def build(bld):
	bld(source='parse-closing.py', target='closing', rule='python ${SRC} 4591 ${TGT}')
	return

def shutdown(ctx):
	return
