#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib


apiURL = 'http://www.omdbapi.com/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.fright-pix')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.fright-pix")
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]

defaultimage = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
defaultfanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
#defaultvideo = 'special://home/addons/plugin.video.fright-pix/icon.png'
#defaulticon = 'special://home/addons/plugin.video.fright-pix/icon.png'
fanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
icon = 'special://home/addons/plugin.video.fright-pix/icon.png'


def get_genres(url):
	html = get_html('http://www.frightpix.com/')
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'sub-menu'})
	match=re.compile('<a href="(.+?)">(.+?)</a>').findall(str(soup))
	xbmc.log(str(len(match)))
	for url,name in match:
		if not 'movies' in url:
			continue
		url = 'http://www.frightpix.com' + str(url)
		add_directory2(name, url, 10, fanart, icon, plot='')
		xbmcplugin.setContent(addon_handle, 'movies')
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)



def index(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('figure')
	plots = BeautifulSoup(html,'html5lib').find_all('div',{'class':'film-data-desc'})
	for item, plot in zip(soup, plots):
		title = item.find('img')['alt']
		url = 'http://www.frightpix.com' + item.find('a')['href']
		image = item.find('img')['src']
		plot =striphtml(str(plot)).strip()
		infoLabels = {'title':title,
					  'tvshowtitle':title,
					  'plot':plot}
		#i = i + 1
		#if i <= items:
		addDir2(title, url, 20, fanart, image, plot)
		#xbmcplugin.setInfo(type="Video", infoLabels=infoLabels)
		#xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=50)
		xbmcplugin.setContent(addon_handle, 'movies')
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def get_movie(name,url):
	html = get_html(url)
	#soup = BeautifulSoup(html,'html5lib').find_all('div',{'data-videosrc'})
	url = re.compile('data-videosrc="(.+?)"').findall(str(html))[0]
	xbmc.log('Stream: ' + str(url))
	listitem = xbmcgui.ListItem(name)
	xbmc.Player().play(url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:51.0) Gecko/20100101 Firefox/51.0')
	req.add_header('Host','www.frightpix.com')
	req.add_header('Referer','http://www.frightpix.com/')

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



def add_directory2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=10)
	return ok


def addDir2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=10)
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
	print "indexing Genres"
	get_genres(url)
elif mode == 10:
	print "indexing Videos"
	index(url)
elif mode == 2:
	print "indexing Replay by Sport"
	REPLAYBYSPORT(url)
elif mode == 4:
	print "Play Video"

elif mode == 20:
	print "Get FrightPix Movies"
	get_movie(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


