#!/usr/bin/python
#
#
# Constructed by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
import urlparse
import httplib


settings = xbmcaddon.Addon(id="plugin.video.internetarchive")
artbase = 'special://home/addons/plugin.video.internetarchive/resources/media/'
selfAddon = xbmcaddon.Addon(id='plugin.video.internetarchive')
translation = selfAddon.getLocalizedString
local_string = xbmcaddon.Addon(id='plugin.video.internetarchive').getLocalizedString
dsort = settings.getSetting(id="dsort")
ssort = settings.getSetting(id="ssort")
download = settings.getSetting(id="download")
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.internetarchive")
addon = xbmcaddon.Addon(id="plugin.video.internetarchive")
addonname = addon.getAddonInfo('name')
baseurl = 'https://archive.org/'

plugin = "Internet Archive [Video]"

defaultimage = 'special://home/addons/plugin.video.internetarchive/icon.png'
defaultfanart = 'special://home/addons/plugin.video.internetarchive/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.internetarchive/icon.png'

addon_handle = int(sys.argv[1])
#int(sys.argv[1])
confluence_views = [551,500,501,502,503,504,508,515]
#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[4])+")")

#60
def ia_categories():
		mode = 62
		try:data = urllib2.urlopen(baseurl).read()
		except urllib2.HTTPError , e:
			print 'Error Type= ' + str(type(e))    #not catch
			print 'Error Args= ' + str(e.args)
			line1 = 'The addon ' + str(e.args).partition("'")[-1].rpartition("'")[0] + '.'
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		except urllib2.URLError , e:
			print 'Error Type= ' + str(type(e))
			print 'Error Args= ' + str(e.args)
			line1 = 'The addon ' + str(e.args).partition("'")[-1].rpartition("'")[0] + '.'
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		add_directory2('Search', baseurl, 65, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		soup = BeautifulSoup(data,'html.parser')
		for item in soup.find_all(attrs={'class': 'row toprow fivecolumns movies'}):
			for link in item.find_all('a'):
				l = link.get('href')
				title = link.get('title')
				#print 'Title= ' + str(title)
				if title == 'TV NSA Clip Library':
					mode = 64
					url = l + '&page=1'
				if title == 'Occupy Wall Street':
					mode = 62
					url = l + '&page=1'
				else:
					url = l
				if len(url) <5:
					continue
				if str(url)[0] == '/':
					url = 'https://archive.org' + url
				if title not in link:
					title = link.text
					if len(title) < 1:
						continue
					link = str(link)
					#title = re.compile('>(.+?)</a>').findall(link)[0]
					print 'TITLE: ' + str(title)
					if 'img' in title:
						continue
					if '</span> ' in title:
						title = re.compile('</span> (.+?)</').findall(link)[0]
					if 'Understanding' in title:
						add_directory2(title,'https://archive.org/details/911', 70,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
						continue
					if ('All Video' in title) or ('Just' in title):
						# Find a better way #
						title = (title.split(" ", 1))[-1]
						#
						mode = 61
					if title == 'TV News':
						mode = 62
						url = 'https://archive.org/details/tvnews'
					if 'Just' in title:
						mode = 62
				url = url +'&page=1' #'?&sort='+default+
				#print 'IA URL= ' + str(url)
				add_directory2(title,url, mode,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#61
def ia_sub_cat(url):
		url = url.split("?")[0]
		#print 'ia sub cat url= ' + str(url)
		data = urllib2.urlopen(url).read()
		soup = BeautifulSoup(data,'html.parser')
		for item in soup.find_all(attrs={'class': 'collection-title'}):
			for link in item.find_all('a'):
				l = link.get('href')
				url = 'http://archive.org' + l +'&page=1'# '?&sort='+default+
				if len(url) <25:
					continue
				link = str(link)
				title = re.sub('\s+',' ',link)
				title = re.compile('<div>(.+)</div>').findall(title)[0]
				title = title.replace('&amp;','&')
				if 'Television Archive' in title:
					mode = 61
				if 'Movies' in title:
					mode = 61
				if 'Feature' in title:
					mode = 61
				else:
					mode = 62

				add_directory2(title,url, mode, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#62
def ia_sub2_video(url):
		page = (url)[-1]
		#print 'page= ' + str(page)
		thisurl = url.split("?")[0]
		#print 'thisurl= ' + str(thisurl)
		req = urllib2.Request(url)
		try: data = urllib2.urlopen(req, timeout = 10)
		except urllib2.HTTPError , e:
			print 'Error Type= ' + str(type(e))    #not catch
			print 'Error Args= ' + str(e.args)
			print 'Error Code0= ' + str(e.code)
			line1 = str(e.code)#.partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		except urllib2.URLError , e:
			print 'Error Type= ' + str(type(e))
			print 'Error Args= ' + str(e.args)
			line1 = str(e.args)#.partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		#hidden = BeautifulSoup(data,'html.parser').find_all('div', 'details-ia')
		#xbmc.log('HIDDEN: ' + str(hidden))
		#xbmc.log('HIDDEN: ' + str(len(hidden)))
		try: soup = BeautifulSoup(data,'html.parser')
		except:
			print 'Error Type= '# + str(type(e))    #not catch
			print 'Error Args= '# + str(e.args)
			line1 = 'Time Out'#str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		#if soup.find('div',{'class':'details-ia'}):
			#xbmc.log('MATCH')
		for item in soup.find_all(attrs={"class":"item-ia"}):#('div',{'class':'item-ttl'}):
			if item.find('div',{'class':'item-ttl'}):
				#xbmc.log('MATCH')
			#for item in items.find('div',{'class':'C234'})[0]:
				for link in item.find_all('a'):
					purl = 'https://archive.org' + link.get('href')
					title = link.get('title')#.encode('ascii','ignore')
					if title == None:
						continue
					title = title.encode('ascii','ignore')
					image = 'https://archive.org' + link.find('img')['source']
						#plot = plots.find('div',{'class':'C234'})
				try: add_directory3(title, purl, 67, defaultfanart, image, plot='')
				except KeyError:
					continue
		page = int(page) + 1
		thisurl = thisurl.rpartition('&')[0]
		url = thisurl +'&page=' + str(page)# '?&sort='+default+'&page=' + str(page)
		print 'IA Next Page URL= ' + str(url)
		add_directory2('Next Page', url, 62,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#67
def get_links(name,url):
		html = get_html(url)
		match = re.compile('<meta property="og:video" content="(.+?)"').findall(html)
		xbmc.log('MATCH: ' + str(match))
		if str(match) == '[]':
			xbmc.log('NOTHING TO PLAY')
			xbmcgui.Dialog().notification('IA [Video]', 'No Playable File on Archive.org', xbmcgui.NOTIFICATION_INFO, 5000)
			sys.exit()
		plot = str(re.compile('<meta property="og:description" content="(.+?)"').findall(html))[2:-2]
		plot = plot.replace('\\xc2\\xa0',' ').replace('\\xe2\\x80\\x99','\'').replace('\\xe2\\x80\\x98','')
		#image = str(re.compile('<meta property="og:image" content="(.+?)"/>').findall(html))[2:-2]
		#infoLabels = {'title':name, 'plot':plot}
		clipstream = re.compile('TV.clipstream_clips  = (.+?);').findall(html)
		xbmc.log('CLIPSTREAM: ' + str(len(clipstream)))
		if str(clipstream) == '[]':
			url = str(match)[2:-2]
			play(name,url)
		else:
			xbmc.log('CLIPSTREAM: ' + str(len(clipstream)))
			xbmc.log('URL: ' + str(url))
			ia_clipstream(url)

#63
def ia_clipstream(url):
		xbmc.log('CLIPSTREAM URL:' + str(url))
		html = get_html(url)
		clipstream = re.compile('TV.clipstream_clips  = (.+?);').findall(html)
		xbmc.log('CLIPSTREAM: ' + str(len(clipstream)))
		data = str(clipstream)[3:-3]
		data = data.replace('"','')
		data = data.split(',')
		xbmc.log('DATA: ' + str(len(data)))
		for item in data:
			title = item
			url = (item.split('\\?'))[0]
			add_directory3(title,url,999,defaultfanart,defaultimage,plot='')
		xbmcplugin.endOfDirectory(addon_handle)

#80
def downloader(url):
		xbmc.log('DOWNLOAD')
		path = addon.getSetting('download')
		if path == "":
			xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
					%(translation(30000), translation(30010), defaulticon))
			addon.openSettings()
			path = addon.getSetting('download')
		if path == "":
			return
		html = get_html(url)
		xbmcgui.Dialog().notification('IA [Video]', 'Getting Download URL.', xbmcgui.NOTIFICATION_INFO, 5000)
		match = re.compile('<meta property="og:video" content="(.+?)"/>').findall(html)
		xbmc.log('MATCH: ' + str(match[0]))
		url = resolve_http_redirect(match[0])
		xbmc.log('FINAL URL: ' + str(url))
		file_name = url.split('/')[-1]
		dlsn = settings.getSetting(id="status")
		bsize = settings.getSetting(id="bsize")
		#print 'bfr Size= ' + str(bsize)
		ret = xbmcgui.Dialog().yesno("Internet Archive [Video]", 'Download Selected File?', str(file_name))
		if ret == False:
			return ia_sub2_video
		else:
			xbmcgui.Dialog().notification('IA [Video]', 'Download Started.', xbmcgui.NOTIFICATION_INFO, 3000)
		print 'URL: ' + str(url)
		print 'Filename: ' + str(file_name)
		print 'Download Location: ' + str(download)
		u = urllib2.urlopen(url)
		f = open(download+file_name, 'wb')
		meta = u.info()
		file_size = float(meta.getheaders("Content-Length")[0])
		file_sizeMB = float(file_size/(1024*1024))
		print "Downloading: %s %s MB" % (file_name, "%.2f" % file_sizeMB)
		file_size_dl = 0
		block_sz = int(bsize)
		while True:
			bfr = u.read(block_sz)
			if not bfr:
				break
			file_size_dl += float(len(bfr))
			file_size_dlMB = float(file_size_dl/(1024*1024))
			f.write(bfr)
			status = "%.2f  [%3.2f%%]" % (file_size_dlMB, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			if dlsn!='false':
				xbmcgui.Dialog().notification('IA [Video] Download in Progress', str(status) + ' of ' + ("%.2f" % float(file_sizeMB)) + ' MB', xbmcgui.NOTIFICATION_INFO, 2500, False)
			else:
				break
		f.close()
		xbmcgui.Dialog().notification('IA [Video]', 'Download Completed.', xbmcgui.NOTIFICATION_INFO, 5000)
		print 'Download Completed'


def sanitize(data):
	output = ''
	for i in data:
		for current in i:
			if ((current >= '\x20') and (current <= '\xD7FF')) or ((current >= '\xE000') and (current <= '\xFFFD')) or ((current >= '\x10000') and (current <= '\x10FFFF')):
			   output = output + current
	return output


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)

#>>> striphtml('<a href="foo.com" class="bar">I Want This <b>text!</b></a>')
#'I Want This text!'

#73
def ia_911_streams(url):
		html = get_html(url)
		images = re.compile('src="(.+?)"/>').findall(html)
		i = 0
		for image in images:
			if i % 2==0:
				seconds = ':00'
			else:
				seconds = ':30'
			urlkey = image.rsplit('/',1)[-1].rpartition("_")[0]
			network = str(urlkey[:3])
			start = str(image.rpartition("_")[-1])[2:-4]
			end = str(int(start) + 30)
			url = 'https://ia802203.us.archive.org/28/items/' + urlkey + '/' + urlkey + '.mp4?start=' + start + '&end=' + end + '&ignore=x.mp4'
			image = 'https:' + str(image)
			title = network + ' - ' + re.compile('title="(.+?)"').findall(html)[i].replace('am', seconds + 'am').replace('pm', seconds + 'pm')
			i = i + 1
			li = xbmcgui.ListItem(title, iconImage =  image, thumbnailImage =  image)
			li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
			xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url, listitem=li, totalItems=15)
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#70
def ia_u911(url):
		html = get_html(url)
		days = re.compile('<span class="day">(.+?)</span><br />\\n    <a href="(.+?)">(.+?)</a>').findall(html)
		for day,url,date in days[1:]:
			title = day + ', ' + date
			url = 'https://archive.org' + str(url)
			add_directory2(title,url,71,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		u911 = re.compile('<td class="c1">(.+?)</tr>').findall(html)
		i = 0
		for title in u911:
			title = striphtml(title)
			title = "[" + "m ] ".join(title.split("m", 1))
			url = re.compile('"file":"(.+?)"').findall(html)[i]
			url = 'https://archive.org' + url.replace('\\','')
			i = i + 1
			li = xbmcgui.ListItem(title, iconImage =  artbase + 'internetarchive.jpg', thumbnailImage =  artbase + 'internetarchive.jpg')
			li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
			xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url, listitem=li, totalItems=15)
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#71
def ia_u911_day(url):
		html = get_html(url)
		#datecode = url.rsplit('/', 1)[-1]
		soup = BeautifulSoup(html,'html.parser')
		nets = soup.find_all(attrs={'id': 'gridL'})
		location = re.compile('<i>(.+?)</i>').findall(str(nets))
		i = 0
		networks = re.compile('url\\((.+?)\\)').findall(html)
		for network in networks:
			title = network.partition("_")[-1].rpartition(".jpg")[0] + ' - ' + str(location[i])
			image = 'https://archive.org' + str(network)

			i = i + 1
			add_directory2(title,url,72,  artbase + 'internetarchive.jpg', image,plot='')
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#72
def ia_u911_day_net(name,url):
		html = get_html(url)
		datecode = url.rsplit('/', 1)[-1]
		divid = name.split('-',1)[0].strip() + '_' + datecode
		#print 'divid= ' + str(divid)
		soup = BeautifulSoup(html,'html.parser')
		for ndiv in soup.find_all(attrs={'id': divid}):
			for link in ndiv.find_all('a'):
				l = link.get('href')
				url = 'https://archive.org' + l + '&hi1=0&raw=1'
				title = link.get('title')
				add_directory2(title,url,73,  artbase + 'internetarchive.jpg', artbase + 'internetarchive.jpg',plot='')
		#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

#64
def ia_nsa(url):
		data = get_html(url)
		page = (url)[-1]
		match = re.compile('<video src="(.+?)"').findall(data)
		for link in match:
			url = 'https://archive.org' + link
			title = url

			li = xbmcgui.ListItem(title, iconImage=artbase + 'ia.png', thumbnailImage=artbase + 'ia.png')
			li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
			xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url, listitem=li, totalItems=70)
		page = str(int(page) + 1)
		url = 'https://archive.org/details/nsa?page=' + page
		print 'IA NSA Next Page URL= ' + str(url)
		add_directory2('Next Page', url, 64,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

#65
def ia_search():
		keyb = xbmc.Keyboard('', 'Search')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			print 'search= ' + search
			#https://archive.org/search.php?query=%28commodore%29%20AND%20mediatype%3A%28movies%29
			url = 'https://archive.org/search.php?query=%28' + search + '%29%20AND%20mediatype%3A%28movies%29&page=1'
			#url = 'https://archive.org/search.php?query=' + search + '&and[]=mediatype%3A%22movies%22&page=1'
			ia_search_video(url)
		else:
			ia_categories()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

#66
def ia_search_video(url):
		page = (url)[-1]
		#print 'page= ' + str(page)
		thisurl = url[:-7]
		#print 'thisurl= ' + str(thisurl)
		data = urllib2.urlopen(url).read()
		soup = BeautifulSoup(data,'html.parser')
		#print 'SOUP= ' + str(soup)
		for item in soup.find_all(attrs={'class': 'item-ttl'}):
			#for link in item.find_all('a'):
				l = item.find('a')['href']
				purl = 'https://archive.org' + l
				title = (item.find('a')['title'])
				if len(title) < 1:
				   continue
				image = 'https://archive.org' + item.find('img')['source']
				try: add_directory3(title, purl, 67, defaultfanart, image, plot='')
				except KeyError:
					continue
		page = str(int(page) + 1)
		#thisurl = thisurl.replace('?&sort='+sval+'','')
		url = thisurl + '&page=' + page
		print 'IA Next Page URL= ' + str(url)
		add_directory2('Next Page', url, 66,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


def play(name,url):
	url = url.replace(' ','%20')
	print url
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def plot_info(url):
		html = get_html(url)
		plot = str(re.compile('<meta property="og:description" content="(.+?)"').findall(html))[2:-2]
		xbmcgui.Dialog().ok('Plot Info', plot)


def add_directory3(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		#commands = []
		#commands.append ----- THIS WORKS! -----
		liz.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url)),('Description', 'XBMC.RunPlugin(%s?mode=81&url=%s)' % (sys.argv[0], url))])
		#liz.addContextMenuItems([('Plot Info', 'XBMC.RunPlugin(%s?mode=81&url=%s)' % (sys.argv[0], url))])
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=70)
		return ok


def add_directory2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=70)
		return ok


def add_directory(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=70)
		return ok

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params) - 1] == '/'):
			params = params[0:len(params) - 2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]

	return param


def resolve_http_redirect(url, depth=0):
    if depth > 10:
        raise Exception("Redirected "+depth+" times, giving up.")
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if headers.has_key('location') and headers['location'] != url:
        return resolve_http_redirect(headers['location'], depth+1)
    else:
        return url


def unescape(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()




params = get_params()
url = None
name = None
mode = None
cookie = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
	print "Generate Main Menu"
	ia_categories()
elif mode == 1:
	print "Indexing Videos"
	index(url)
elif mode == 4:
	print "Play Video"
elif mode == 6:
	print "Get Episodes"
	get_episodes(url)
elif mode == 60:
	print "Get IA Video Categories"
	ia_video(url)
elif mode == 61:
	print "Get IA Video Sub Categories"
	ia_sub_cat(url)
elif mode == 62:
	print "Get IA Video Sub2 Categories"
	ia_sub2_video(url)
elif mode == 63:
	print "Get IA Clipstream"
	ia_clipstream(url)
elif mode == 64:
	print "Get IA NSA"
	ia_nsa(url)
elif mode == 65:
	print "IA Search"
	ia_search()
elif mode == 66:
	print "IA Search Video"
	ia_search_video(url)
elif mode == 67:
	print "IA Get Links"
	get_links(name,url)
elif mode == 70:
	print "IA Understanding 9/11"
	ia_u911(url)
elif mode == 71:
	print "IA 9/11 Day"
	ia_u911_day(url)
elif mode == 72:
	print "IA 9/11 Day Net"
	ia_u911_day_net(name,url)
elif mode == 73:
   print "IA 911 Streams"
   ia_911_streams(url)
elif mode == 80:
   print "IA Download File"
   downloader(url)
elif mode == 81:
   print "IA Plot Info"
   plot_info(url)
elif mode==999:
	print "IA Play URL"
	play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
