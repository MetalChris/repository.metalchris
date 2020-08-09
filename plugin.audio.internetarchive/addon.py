#!/usr/bin/python
#
#
# Constructed by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
from bs4 import BeautifulSoup
#import lxml.html
#import socket
from ssl import SSLError

settings = xbmcaddon.Addon(id="plugin.audio.internetarchive")
artbase = 'special://home/addons/plugin.audio.internetarchive/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.audio.internetarchive')
translation = selfAddon.getLocalizedString
local_string = xbmcaddon.Addon(id='plugin.audio.internetarchive').getLocalizedString
download = settings.getSetting(id="download")
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.audio.internetarchive")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
baseurl = 'https://archive.org/'
audiourl = 'https://archive.org/details/audio'

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

plugin = "Internet Archive [Audio]"

defaultimage = 'special://home/addons/plugin.audio.internetarchive/icon.png'
defaultfanart = 'special://home/addons/plugin.audio.internetarchive/fanart.jpg'
defaulticon = 'special://home/addons/plugin.audio.internetarchive/icon.png'

local_string = xbmcaddon.Addon(id='plugin.audio.internetarchive').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#confluence_views = [500,501,502,503,504,508,515]
#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#60
def ia_categories():
		data = urllib2.urlopen(audiourl).read()
		add_directory2('Search', baseurl, 65, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		soup = BeautifulSoup(data,'html.parser')
		for item in soup.find_all(attrs={'class': 'collection-title C C2'}):
			for link in item.find_all('a'):
				l = link.get('href')
				title = link.get('title')
				url = l
				if len(url) <5:
					continue
				if str(url)[0] == '/':
					url = 'https://archive.org' + url
				if title not in link:
					title = link.text
					if len(title) < 1:
						continue
					if ('All Audio' in title) or ('Just' in title):
						# Find a better way #
						title = (title.split(" ", 1))[-1]
					link = str(link)
					#title = re.compile('>(.+?)</a>').findall(link)[0]
					if 'img' in title:
						continue
					if '</span> ' in title:
						title = re.compile('</span> (.+?)</').findall(link)[0]
					if 'All Audio' in title:
						mode = 61
					elif title == 'Live Music Archive':
						mode = 64
					else:
						mode = 62
				url = url + '&page=1'
				title = title.strip()
				xbmc.log('TITLE: ' + str(title),level=log_level)
				#xbmc.log('IA URL= ' + str(url),level=log_level)
				add_directory2(title,url, mode,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.setContent(pluginhandle, 'episodes')


#61
def ia_sub_cat(url):
		url = url.replace('?&page=1','')
		#xbmc.log('IA Audio Sub_Cat URL= ' + str(url),level=log_level)
		data = urllib2.urlopen(url).read()
		soup = BeautifulSoup(data,'html.parser')
		for item in soup.find_all(attrs={'class': 'collection-title'}):
			for link in item.find_all('a'):
				l = link.get('href')
				url = 'https://archive.org' + l + '?&page=1'
				if len(url) <25:
					continue
				link = str(link)
				title = re.sub('\s+',' ',link)
				title = re.compile('<div>(.+)</div>').findall(title)[0]
				title = title.replace('&amp;','&')
				if title == 'Television Archive':
					mode = 61
				else:
					mode = 62
				add_directory2(title,url, mode, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.setContent(pluginhandle, 'episodes')


#62
def ia_sub2_audio(name,url):
		page = (url)[-1]
		#xbmc.log('page= ' + str(page),level=log_level)
		thisurl = url[:-7]
		#xbmc.log('thisurl= ' + str(thisurl),level=log_level)
		req = urllib2.Request(url)
		try: data = urllib2.urlopen(req, timeout = 5)
		except urllib2.HTTPError , e:
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)    #not catch
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		except urllib2.URLError , e:
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		#except socket.timeout , e:
			#xbmc.log('Error Type= ' + str(type(e)),level=log_level)
			#xbmc.log('Error Args= ' + str(e.args),level=log_level)
			#line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			#xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			#return
		try: soup = BeautifulSoup(data,'html.parser').find_all('div',{'class': 'item-ttl'})
		except SSLError:
			e = sys.exc_info()[1]
			xbmc.log('ERROR: ' + str(e),level=log_level)
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)    #not catch
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		xbmc.log(('SOUP:' + str(len(soup))),level=log_level)
		for item in soup:
			l = item.find('a')['href']
			purl = 'https://archive.org' + l
			title = item.find('a')['title'].encode('ascii','ignore')
			url = purl
			add_directory2(title,url, 63, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		page = str(int(page) + 1)
		#thisurl = thisurl.replace('?','')
		url = thisurl + '&page=' + page
		xbmc.log('IA Next Page URL= ' + str(url),level=log_level)
		add_next('Next Page', url, 62,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#63
def ia_audio_files(url):
	html = get_html(url)
	tracks = re.compile('"title":"(.+?)",').findall(html);	i = 0
	for track in tracks:
		title = str(track.split('.')[-1])
		try:song = re.compile('"file":"(.+?)mp3').findall(html)[i]
		except IndexError:
			pass
		duration = re.compile('duration(.+?)sources').findall(html)[i]
		duration = duration[2:-2]
		i = i + 1
		tracknumber = int(i)
		url = 'https://archive.org' + str(song) + 'mp3'
		infoLabels = {'title':title, 'duration':duration, 'tracknumber':tracknumber}
		li = xbmcgui.ListItem(title, iconImage=artbase + 'ia.png', thumbnailImage=artbase + 'ia.png')
		li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
		#li.setProperty(Playcount)
		li.setInfo(type = 'music', infoLabels = infoLabels)
		li.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url))])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
		xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#64
def ia_live_audio(name,url):
		page = (url)[-1]
		#xbmc.log('page= ' + str(page),level=log_level)
		thisurl = url[:-7]
		#xbmc.log('thisurl= ' + str(thisurl),level=log_level)
		req = urllib2.Request(url)
		try: data = urllib2.urlopen(req, timeout = 5)
		except urllib2.HTTPError , e:
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)    #not catch
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		except urllib2.URLError , e:
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		#except socket.timeout , e:
			#xbmc.log('Error Type= ' + str(type(e)),level=log_level)
			#xbmc.log('Error Args= ' + str(e.args),level=log_level)
			#line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			#xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			#return
		try: soup = BeautifulSoup(data,'html.parser').find_all('div',{'class': 'collection-title'})
		except SSLError:
			e = sys.exc_info()[1]
			xbmc.log('ERROR: ' + str(e),level=log_level)
			xbmc.log('Error Type= ' + str(type(e)),level=log_level)    #not catch
			xbmc.log('Error Args= ' + str(e.args),level=log_level)
			line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
			#dialog = xbmcgui.Dialog()
			xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
			return
		xbmc.log(('SOUP:' + str(len(soup))),level=log_level)
		for item in soup:
			l = item.find('a')['href']
			purl = 'https://archive.org' + l
			title = item.find('a').text.encode('ascii','ignore').strip()
			url = purl + '&page=1'
			add_directory2(title,url, 62, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		page = str(int(page) + 1)
		#thisurl = thisurl.replace('?','')
		url = thisurl + '&page=' + page
		xbmc.log('IA Next Page URL= ' + str(url),level=log_level)
		add_next('Next Page', url, 64,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
		xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#81
def lineage(url):
		html = get_html(url)
		xbmc.log('Lineage URL: ' + str(url),level=log_level)
		soup = BeautifulSoup(html,'html.parser').find_all('dl',{'class': 'metadata-definition'})
		#xbmc.log('SOUP: ' + str(soup),level=log_level)
		for item in soup:
			match = item.find('dt')
			if 'Lineage' in match:
				xbmc.log('Lineage Found: ' + str(match),level=log_level)
				lineage = item.find('dd').text
				xbmc.log('Lineage dd: ' + str(lineage),level=log_level)
		#lineage = str(re.compile('Lineage</dt>\n<dd class="">"(.+?)"</').findall(str(html)))[2:-2]
		#xbmc.log('Lineage: ' + str(lineage),level=log_level)
		#lineage = lineage.replace('&gt;','>').replace('&amp;','&')
				if len(lineage) < 5:
					lineage = 'Not Available'
				xbmcgui.Dialog().ok('Lineage', lineage)


#82
def desc(url):
		html = get_html(url)
		desc = str(re.compile('<meta property="og:description" content="(.+?)"/>').findall(html))[2:-2].replace('\\xc2\\xa0',' ').replace('\\xe2\\x80\\x99','\'').replace('\\xe2\\x80\\x98','')
		xbmcgui.Dialog().ok('Description', desc)


def play(name,url):
    url = url.replace(' ','%20')
    xbmc.log(url,level=log_level)
    listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
    xbmc.Player().play( url, listitem )
    sys.exit()
    xbmcplugin.endOfDirectory(addon_handle)


def ia_search():
		keyb = xbmc.Keyboard('', 'Search')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			xbmc.log('search= ' + search,level=log_level)
			url = 'https://archive.org/search.php?query=%28' + search + '%29%20AND%20mediatype%3A%28audio%29&page=1'
			#url = 'https://archive.org/search.php?query=' + search + '&and[]=mediatype%3A%22audio%22&page=1'
			ia_sub2_audio(name,url)
			#ia_search_audio(url)
		else:
			ia_categories()


def ia_search_audio(url):
		page = (url)[-1]
		#xbmc.log('page= ' + str(page),level=log_level)
		thisurl = url[:-7]
		#xbmc.log('thisurl= ' + str(thisurl),level=log_level)
		data = urllib2.urlopen(url).read()
		soup = BeautifulSoup(data,'html.parser')
		for item in soup.find_all(attrs={'class': 'item-ttl C C2'}):
			for link in item.find_all('a'):
				l = link.get('href')
				purl = 'https://archive.org' + l
				title = link.get('title')
				html = get_html(purl)
				match=re.compile('<meta property="og:video" content="(.+?)"/>').findall(html)
				clipstream = re.compile('TV.clipstream_clips  = (.+?);').findall(html)
				if str(clipstream) == '[]':
					url = str(match)[2:-2]
					if len(url) <25:
						continue
					li = xbmcgui.ListItem(title, iconImage= artbase + 'ia.png', thumbnailImage= artbase + 'ia.png')
					li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
					xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
				else:
					url = str(clipstream)[3:-3]
					url = url.replace('"','')
					try: add_directory2(title,url,63,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
					except KeyError:
						continue
		page = str(int(page) + 1)
		thisurl = thisurl.replace('?','')
		url = thisurl + '&page=' + page
		xbmc.log('IA Next Page URL= ' + str(url),level=log_level)
		add_next('Next Page', url, 66,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')

		xbmcplugin.endOfDirectory(addon_handle)


#80
def downloader(url):
		xbmc.log(('DOWNLOAD'),level=log_level)
		path = addon.getSetting('download')
		if path == "":
			xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
					%(translation(30000), translation(30010), defaulticon))
			addon.openSettings()
			path = addon.getSetting('download')
		if path == "":
			return
		xbmcgui.Dialog().notification('IA [Audio]', 'Getting Download URL.', xbmcgui.NOTIFICATION_INFO, 5000)
		file_name = url.split('/')[-1]
		dlsn = settings.getSetting(id="status")
		bsize = settings.getSetting(id="bsize")
		#xbmc.log('bfr Size= ' + str(bsize),level=log_level)
		ret = xbmcgui.Dialog().yesno("Internet Archive [Audio]", 'Download Selected File?', str(file_name))
		if ret == False:
			return #ia_sub2_video
		else:
			xbmcgui.Dialog().notification('IA [Audio]', 'Download Started.', xbmcgui.NOTIFICATION_INFO, 5000)
		xbmc.log('URL: ' + str(url),level=log_level)
		xbmc.log('Filename: ' + str(file_name),level=log_level)
		xbmc.log('Download Location: ' + str(download),level=log_level)
		u = urllib2.urlopen(url)
		f = open(download+file_name, 'wb')
		meta = u.info()
		file_size = float(meta.getheaders("Content-Length")[0])
		file_sizeMB = float(file_size/(1024*1024))
		xbmc.log("Downloading: %s %s MB" % (file_name, "%.2f" % file_sizeMB),level=log_level)
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
				xbmcgui.Dialog().notification('IA [Audio] Download in Progress', str(status) + ' of ' + ("%.2f" % float(file_sizeMB)) + ' MB', xbmcgui.NOTIFICATION_INFO, 2500, False)
			else:
				break
		f.close()
		xbmcgui.Dialog().notification('IA [Audio]', 'Download Completed.', xbmcgui.NOTIFICATION_INFO, 5000)
		xbmc.log('Download Completed',level=log_level)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
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
        liz.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url)),('Lineage', 'XBMC.RunPlugin(%s?mode=81&url=%s)' % (sys.argv[0], url)),('Description', 'XBMC.RunPlugin(%s?mode=82&url=%s)' % (sys.argv[0], url))])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=70)
        return ok


def add_next(name,url,mode,fanart,thumbnail,plot):
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

def addDir(name, url, mode, iconimage, fanart=False, infoLabels=True):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="music", infoLabels={ "Title": name,
												} )
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="music", infoLabels={ "Title": name,
												} )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok


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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu",level=log_level)
	ia_categories()
elif mode == 1:
	xbmc.log("Indexing Audio",level=log_level)
	index(url)
elif mode == 4:
	xbmc.log("Play Audio",level=log_level)
elif mode == 6:
	xbmc.log("Get Episodes",level=log_level)
	get_episodes(url)
elif mode == 60:
	xbmc.log("Get IA Audio Categories",level=log_level)
	ia_video(url)
elif mode == 61:
	xbmc.log("Get IA Audio Sub Categories",level=log_level)
	ia_sub_cat(url)
elif mode == 62:
	xbmc.log("Get IA Audio Sub2 Categories",level=log_level)
	ia_sub2_audio(name,url)
elif mode == 63:
	xbmc.log("Get Audio Files",level=log_level)
	ia_audio_files(url)
elif mode == 64:
	xbmc.log("Get IA Audio Live Categories",level=log_level)
	ia_live_audio(name,url)
elif mode == 65:
	xbmc.log("IA Search",level=log_level)
	ia_search()
elif mode == 66:
	xbmc.log("IA Search Audio",level=log_level)
	ia_search_audio(url)
elif mode == 80:
   xbmc.log("IA Download File",level=log_level)
   downloader(url)
elif mode == 81:
   xbmc.log("IA Lineage",level=log_level)
   lineage(url)
elif mode == 82:
   xbmc.log("IA Description",level=log_level)
   desc(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
