#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import html5lib

artbase = 'special://home/addons/plugin.video.hunt-channel/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.hunt-channel')
self = xbmcaddon.Addon(id='plugin.video.hunt-channel')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]
settings = xbmcaddon.Addon(id="plugin.video.hunt-channel")

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

plugin = "Hunt Channel"
name = "Hunt Channel"

defaultimage = 'special://home/addons/plugin.video.hunt-channel/icon.png'
defaultfanart = 'special://home/addons/plugin.video.hunt-channel/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.hunt-channel/icon.png'
iconimage = 'special://home/addons/plugin.video.hunt-channel/icon.png'
baseurl = 'http://www.huntchannel.tv'

local_string = xbmcaddon.Addon(id='plugin.video.hunt-channel').getLocalizedString
addon_handle = int(sys.argv[1])


#12
def get_live(name,baseurl,iconimage):
	html = get_html(baseurl)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'sqs-block-content'})
	xbmc.log('SOUP Length: ' + str(len(soup)),level=log_level)
	items = re.compile('src="(.+?)"').findall(str(soup))
	xbmc.log('ITEMS Length: ' + str(len(items)),level=log_level)
	for url in items:
		if 'zype' in url:
			m3u8 = 'plugin://plugin.video.hunt-channel?mode=99&url=' + urllib.quote_plus(url)
			li = xbmcgui.ListItem("Live Stream")
			li.setProperty('IsPlayable', 'true')
			li.setInfo(type="Video", infoLabels={"mediatype":"video","label":name,"title":name,"genre":"Sports"})
			li.setArt({'thumb':defaultimage,'fanart':defaultfanart})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=m3u8, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle)


#99
def PLAY(name,url,iconimage):
	html = get_html(url)
	source = re.compile("container.offsetHeight, '(.+?)'").findall(html)
	xbmc.log('SOURCE: ' + str(source),level=log_level)
	m3u8 = str(re.compile("'[^']*'").findall(str(source)))[3:-3]
	xbmc.log('M3U8: ' + str(m3u8),level=log_level)
	listitem = xbmcgui.ListItem(path = m3u8)
	xbmc.log(('### SETRESOLVEDURL ###'),level=log_level)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url),level=log_level)
	xbmcplugin.endOfDirectory(addon_handle)


def play(name,url,iconimage):
	xbmc.log(str(url),level=log_level)
	listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def get_html(url):
	xbmc.log('URL: ' + str(url),level=log_level)
	req = urllib2.Request(url)
	#req.add_header('Host','content.jwplatform.com')
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0')

	try:
		response = urllib2.urlopen(req, timeout=30)
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
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)# + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name,url,mode,iconimage, fanart=True, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)# + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',defaultfanart)
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
	mode = int(params["mode"])
except:
	pass

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log(("Generate Main Menu"),level=log_level)
	get_live(name,baseurl,iconimage)
elif mode == 4:
	xbmc.log(("Play Video"),level=log_level)
elif mode==10:
	xbmc.log(('Hunt Channel Categories'),level=log_level)
	cats()
elif mode==12:
	xbmc.log(('Hunt Channel Live'),level=log_level)
	get_live(name,baseurl,iconimage)
elif mode==99:
	xbmc.log(('Hunt Channel Play Stream'),level=log_level)
	PLAY(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
