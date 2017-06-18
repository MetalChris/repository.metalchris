#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
import simplejson as json

artbase = 'special://home/addons/plugin.video.bigstar-movies/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.bigstar-movies')
self = xbmcaddon.Addon(id='plugin.video.bigstar-movies')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.bigstar-movies")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
m_views = [50,51,500,501,508,504,503,515]
t_views = [50,51,500,504,503,515]

plugin = "BigStar Movies & TV"

defaultimage = 'special://home/addons/plugin.video.bigstar-movies/icon.png'
defaultfanart = 'special://home/addons/plugin.video.bigstar-movies/fanart.jpg'
fanart = 'special://home/addons/plugin.video.bigstar-movies/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.bigstar-movies/icon.png'

local_string = xbmcaddon.Addon(id='plugin.video.bigstar-movies').getLocalizedString
addon_handle = int(sys.argv[1])
views = settings.getSetting(id="enable_views")
xbmc.log('VIEWS: ' + str(views))
if views == 'false':
	m_view = 0
	t_view = 0
else:
	m_view = settings.getSetting(id="movies_view")
	t_view = settings.getSetting(id="tv_shows_view")
xbmc.log('T_VIEW: ' + str(t_view))
xbmc.log('M_VIEW: ' + str(m_view))


def CATEGORIES():
	addDir('Recently Added', 'http://www.bigstar.tv/mobile/movies/genre/recently-added/page/1/limit/60/os/web/device', 139,
		   defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#140
def bigstar_genres(url):
	add_directory2('Search','http://www.bigstar.tv/mobile/movies/q/', 144, defaultfanart ,defaultimage,plot='')
	response = urllib2.urlopen('http://www.bigstar.tv/mobile/genres/os/web/device/undefined')
	jgdata = json.load(response)
	for item in jgdata["items"]:
		title = item["name"]
		genre = item["url"]
		url = 'http://www.bigstar.tv/mobile/movies/genre/' + str(genre) + '/page/1/limit/30/os/web/device'
		if 'TV Episodes' in title:
			mode = 142
		else:
			mode = 141
		add_directory2(title,url,mode, defaultfanart ,defaultimage,plot='')
	xbmcplugin.setContent(addon_handle, 'episodes')
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#141
def bigstar_movies(url):
	print 'URL= ' + str(url)
	page = re.compile('page/(.+?)/limit').findall(url)[0]
	page = int(page) + 1
	response = urllib2.urlopen(url)
	jgdata = json.load(response)
	for item in jgdata["films"]:
		film_id = item["id"]
		item_page = 'http://www.bigstar.tv/mobile/stream/film/' + str(film_id) + '/ads/1/type/0/version/2/mobileStreams/1/hls/1/os/web/device/75d6a6c6349cfecb9420d6119c51e1ec/lan/default'
		title = item["title"]
		image = item["cover_large"]
		fanart = item["imageUrl1"]
		desc = item["desc"]
		tv = str(item["hasEpisodes"])
		if 'True' in tv:
			continue
		add_directory(title, item_page, 150, fanart , image, plot=desc)
		xbmcplugin.setContent(addon_handle, 'movies')
	next_page = url.rsplit('/', 6)[0]
	next_page = str(next_page) + '/' + str(page) + '/limit/30/os/web/device'
	add_directory2('Next Page>>', next_page, 141, defaultfanart, artbase + 'big-star.png',plot='')
	#if views != 'false':
	xbmc.executebuiltin("Container.SetViewMode("+str(m_views[int(m_view)])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#150
def get_stream(url):
	response = urllib2.urlopen(url)
	jgdata = json.load(response)
	stream = jgdata["items"]["film"]["hls"]
	play(stream)


#142
def bigstar_tv(url):
	add_directory2('Search','http://www.bigstar.tv/mobile/movies/q/', 145, defaultfanart ,defaultimage,plot='')
	print 'URL= ' + str(url)
	page = re.compile('page/(.+?)/limit').findall(url)[0]
	page = int(page) + 1
	next_page = url.rsplit('/', 6)[0]
	next_page = str(next_page) + '/' + str(page) + '/limit/30/os/web/device'
	response = urllib2.urlopen(url)
	jgdata = json.load(response)
	for item in jgdata["films"]:
		title = item["title"]
		image = item["cover_large"]
		fanart = item["imageUrl1"]
		desc = item["desc"]
		plot = desc
		show = item["id"]
		url = 'http://www.bigstar.tv/mobile/movies/boxset/' + str(show) + '/os/web/device'
		add_directory2(title, url,143, fanart, image, plot)
		xbmcplugin.setContent(addon_handle, 'episodes')
	add_directory2('Next Page>>', next_page, 142, defaultfanart , artbase + 'big-star.png',plot='')
	#if views != 'false':
	xbmc.executebuiltin("Container.SetViewMode("+str(t_views[int(t_view)])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#143
def bigstar_episodes(url):
	print 'Episode URL= ' + str(url)
	response = urllib2.urlopen(url)
	jgdata = json.load(response)
	for item in jgdata["films"]:
		film_id = item["id"]
		item_page = 'http://www.bigstar.tv/mobile/stream/film/' + str(film_id) + '/ads/1/type/0/version/2/mobileStreams/1/hls/1/os/web/device/75d6a6c6349cfecb9420d6119c51e1ec/lan/default'
		title = item["title"]
		#image = item["cover_large"]
		fanart = item["imageUrl1"]
		desc = item["desc"]
		add_directory(title, item_page, 150, fanart , fanart, plot=desc)
		xbmcplugin.setContent(addon_handle, 'episodes')
	#if views != 'false':
	xbmc.executebuiltin("Container.SetViewMode("+str(t_views[int(t_view)])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#144
def bigstar_search(url):
	keyb = xbmc.Keyboard('', 'Search')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		print 'search= ' + search
		url = url + search
		print url
		response = urllib2.urlopen(url)
		jgdata = json.load(response)
	for item in jgdata["films"]:
		film_id = item["id"]
		item_page = 'http://www.bigstar.tv/mobile/stream/film/' + str(film_id) + '/ads/1/type/0/version/2/mobileStreams/1/hls/1/os/web/device/75d6a6c6349cfecb9420d6119c51e1ec/lan/default'
		title = item["title"]
		image = item["cover_large"]
		fanart = item["imageUrl1"]
		desc = item["desc"]
		tv = str(item["hasEpisodes"])
		print 'TV= ' + str(tv)
		if 'True' in tv:
			continue
		add_directory(title, item_page, 150, fanart , image, plot=desc)
		xbmcplugin.setContent(addon_handle, 'movies')
	#if views != 'false':
	xbmc.executebuiltin("Container.SetViewMode("+str(m_views[int(m_view)])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#145
def bigstar_tvsearch(url):
	keyb = xbmc.Keyboard('', 'Search')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		print 'search= ' + search
		url = url + search
		print url
		response = urllib2.urlopen(url)
		jgdata = json.load(response)
	for item in jgdata["films"]:
		title = item["title"]
		image = item["cover_large"]
		desc = item["desc"]
		tv = str(item["hasEpisodes"])
		print 'TV= ' + str(tv)
		if 'False' in tv:
			continue
		plot = desc
		show = item["id"]
		url = 'http://www.bigstar.tv/mobile/movies/boxset/' + str(show) + '/os/web/device'
		add_directory2(title, url,143, defaultfanart, image, plot)
		xbmcplugin.setContent(addon_handle, 'episodes')
	#if views != 'false':
	xbmc.executebuiltin("Container.SetViewMode("+str(t_views[int(t_view)])+")")
	xbmcplugin.endOfDirectory(addon_handle)


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

def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def add_directory(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
	return ok

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

	try:
		response = urllib2.urlopen(req, timeout=60)
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
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
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

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
	print "Generate Main Menu"
	bigstar_genres(url)
elif mode == 1:
	print "Indexing Videos"
	INDEX(url)
elif mode == 4:
	print "Play Video"
elif mode==140:
	print "BigStar Genres"
	bigstar_genres(url)
elif mode==141:
	print "BigStar Movies"
	bigstar_movies(url)
elif mode==142:
	print "BigStar TV"
	bigstar_tv(url)
elif mode==143:
	print "BigStar Episodes"
	bigstar_episodes(url)
elif mode == 144:
	print "BigStar Search"
	bigstar_search(url)
elif mode == 145:
	print "BigStar TV Search"
	bigstar_tvsearch(url)
elif mode == 150:
	print "BigStar Get Stream"
	get_stream(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
