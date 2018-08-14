#!/usr/bin/python3
import jinja2
import mistune
import re
import sys
import glob
import os
import time

TEMPLATES = """

<!DOCTYPE html>
<html>
<head>
	<title>{{title}}</title>
	<link rel="stylesheet" type="text/css" href="../static/css/bootstrap.min.css">
	<script type="text/javascript" src="../static/js/jquery.min.js"></script>
	<script type="text/javascript" src="../static/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="container">
		<div class="col-lg-12" style="padding-top: 5%">
			<h1 class="strong">{{title}}</h1>
			<p>Author: Vicky Vernando Dasta</p>
			<p>Build: {{generated_at}} </p>
			<hr>
			
			{{content}}

		</div>
	</div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
	<title>{{title}}</title>
	<link rel="stylesheet" type="text/css" href="../static/css/bootstrap.min.css">
	<script type="text/javascript" src="../static/js/jquery.min.js"></script>
	<script type="text/javascript" src="../static/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="container">
		<div class="col-lg-12" style="padding-top: 5%">
			<h1 class="strong">{{title}}</h1>
			<p>Author: Vicky Vernando Dasta</p>
			<p>Build: {{generated_at}} </p>
			<hr>
			
			{%for post in posts%}
			  <h3>{{post}}</h3>
			{%endfor%}}

		</div>
	</div>
</body>
</html>

"""

def print_error():
	print("""usage: 
   nuw.py init -> untuk membuat blogpost baru
   nuw.py build -> untuk membangun blogpost
   nuw.py publish -> publish blog
   nuw.py delete -> hapus semua kontent
   nuw.py clean -> hapus lock file
   """)



def judul_parser(judul):
	reg = r'\w+'
	reg = re.compile(reg)
	judul = '-'.join(reg.findall(judul))
	return judul + '.md'


def init():
	title = input('judul> ')
	parsed_title = judul_parser(title)
	
	with open(f'build/{parsed_title}'+'.lock', 'a+') as nuwlock:
		nuwlock.write(f'{title}')
		print('lockfile sudah dibuat...')

	with open(f"post/{parsed_title}", 'a+') as f:
		print(f'{parsed_title} sudah dibuat...')
		print('silahkan bikin blognya...')


def clean():
	lock_files = glob.glob('build/*.lock')
	for files in lock_files:
		print(f'removing {files}')
		os.system(f'rm {files}')
		print(f'{files} removed!')


def build():
	print('mencari berkas .lock ...')

	lock_files = glob.glob('build/*.lock')[0]
	print(f'kontent {lock_files} ditemukan...')
	target_name = lock_files.strip('.lock')
	target_post = target_name.split('/')[1]
	target_html = target_name.split('.')[0]+'.html'
	title = open(f'{lock_files}').read().strip('\n')

	print(f'menulis {target_post}')

	with open(f'{target_html}', 'w') as target_file:
		print('memecah konten...')
		parsed_content = mistune	.markdown(open(f'post/{target_post}').read())
		
		print('rendering content...')
		rendered_content = jinja2.Template(TEMPLATES).render(title=title, 
															 content=parsed_content, 
															 generated_at=time.asctime(time.localtime(time.time())))

		print(f'menulis konten {title}')
		target_file.write(rendered_content)
		print(f'{target_html} berhasil dibuat...')

def build_index():
	pass


def delete():
	post_files = glob.glob('post/*.md')
	build_files = glob.glob('build/*.html')

	prompt = input('apakah anda yakin?')
	if prompt in ['ya', 'yes', 'y', 'Y']:

		print('menghapus direktori post...')

		for berkas in post_files:
			print(f'menghapus post/{berkas}')
			os.system(f'rm {berkas}')
			print(f'{berkas} sudah dihapus...')

		print('menghapus direktori build...')	
		for berkas in build_files:
			print(f'menghapus post/{berkas}')
			os.system(f'rm {berkas}')
			print(f'{berkas} sudah dihapus...')




if __name__ == '__main__':
	args = None

	try:
		args = sys.argv[1]
	except:
		print_error()

	if args != None:
		if args == "init":
			init()

		elif args == "build":
			build()

		elif args == "clean":
			clean()

		elif args == "delete":
			delete()

		else:
			print_error()