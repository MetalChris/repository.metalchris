#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

#04.16.2020

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys
import simplejson as json
import mechanize
import html5lib

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')]

artbase = 'special://home/addons/plugin.video.space/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.space')
self = xbmcaddon.Addon(id='plugin.video.space')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.space")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

plugin = "Space.com"

defaultimage = 'special://home/addons/plugin.video.space/icon.png'
defaultfanart = 'special://home/addons/plugin.video.space/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.space/icon.png'
baseurl = 'http://www.space.com/'
next_pre = 'http://www.space.com/news/'

local_string = xbmcaddon.Addon(id='plugin.video.space').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


#630
def cats():
	br.set_handle_robots( False )
	response = br.open('https://videos.space.com/')
	page = response.get_data()
	playlists = re.compile('playlistId": "(.+?)"').findall(page)
	xbmc.log('PLAYLISTS: ' + str(playlists),level=log_level)
	for playlistId in range(len(playlists)):
		jurl = 'https://content.jwplatform.com/v2/playlists/' + str(playlists[playlistId])
		jgresponse = get_html(jurl)
		jgdata = json.loads(jgresponse)
		title = (jgdata['title']).encode('utf-8')
		image = defaultimage
		addDir(title, jurl, 633, image, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle)


#633
def videos(url):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	jsob = json.loads(page)
	total = len(jsob['playlist'])
	xbmc.log('TOTAL: ' + str(total),level=log_level)
	for title in range(total):
		name = (jsob['playlist'][title]['title']).encode('utf-8')
		jurl = (jsob['playlist'][title]['sources'][0]['file'])
		image = (jsob['playlist'][title]['image'])
		url = 'plugin://plugin.video.space?mode=99&url=' + urllib.quote_plus(jurl)
		li = xbmcgui.ListItem(name)
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="Video", infoLabels={"mediatype":"video","label":name,"title":name,"genre":"Space"})
		li.setArt({'thumb':image,'fanart':defaultfanart})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log(('### SETRESOLVEDURL ###'),level=log_level)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=log_level)
	xbmcplugin.endOfDirectory(addon_handle)


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

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
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok

params = get_params()
url = None
name = None
mode = None
cookie = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	plot = urllib.unquote_plus(params["plot"])
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
	xbmc.log(("Generate Space.com Main Menu"),level=log_level)
	cats()
elif mode==630:
	xbmc.log(("Space.com Categories"),level=log_level)
	cats()
elif mode==633:
	xbmc.log(("Space.com Videos"),level=log_level)
	videos(url)
elif mode==636:
	xbmc.log(("Space.com Stream"),level=log_level)
	play(name,url,iconimage)
elif mode == 99:
	xbmc.log("Play Video", level=log_level)
	PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
