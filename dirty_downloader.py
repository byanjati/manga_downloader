import urllib2
import urllib
import bs4
import errno
import os

def require_dir(path):
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise

def search_comic(manga_title,links):
	list_comic = []
	for i in links:
		if manga_title in i['href']:		
			list_comic.append(i['href'])

	return list_comic[0]

def inspect_url(url):
	resp = urllib2.urlopen(url)
	html_resp = resp.read()

	return html_resp

def inspect_img(resp):
	inspector = bs4.BeautifulSoup(resp)
	imgs = inspector.select('.page img')

	return imgs[0]

def inspect_next_url(resp):
	inspector = bs4.BeautifulSoup(resp)
	next_url = inspector.select('.next a')

	return next_url[0]

def download_comic(manga_title,mangasource):
	if mangasource is "mangastream":
		directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), manga_title)
		require_dir(directory)

		html = inspect_url("http://mangastream.com/")
		soup = bs4.BeautifulSoup(html)
		links = soup.select('.new-list a[href]')

		resp = inspect_url(search_comic(manga_title,links))

		try:
			i = 100
			while(inspect_img(resp)['src'] is not None):
				filename = os.path.join(directory, manga_title + ' ' + str(i)+".png")
				urllib.urlretrieve(inspect_img(resp)['src'],filename)
				i += 1
				resp = inspect_url(inspect_next_url(resp)['href'])
		except IndexError:
			print "finished"

download_comic('one_piece','mangastream')