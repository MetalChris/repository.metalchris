#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup


artbase = 'special://home/addons/plugin.video.gmm/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.gmm')
self = xbmcaddon.Addon(id='plugin.video.gmm')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.gmm")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "GMM - Graspop Metal Meeting"

defaultimage = 'special://home/addons/plugin.video.gmm/icon.png'
defaultfanart = 'special://home/addons/plugin.video.gmm/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.gmm/icon.png'
baseurl = 'http://vod.graspop.be/?language=en'

local_string = xbmcaddon.Addon(id='plugin.video.gmm').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#20
def sites():
		addDir('Concert', baseurl, 30, defaultimage)
		addDir('Reportage', baseurl, 30, defaultimage)
		addDir('Interview', baseurl, 30, defaultimage)
		addDir('Showcase', baseurl, 30, defaultimage)
		addDir('Highlights', baseurl, 30, defaultimage)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


#30
def cat(name,url):
	key = name.lower()
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('li',{'class':'stream__list__item __' + key})
	for item in soup:
		title = item.find('strong').text.strip().split('   ')[0].encode('utf-8')
		url = 'http://vod.graspop.be/' + item.find('a')['href']
		image = item.find('img')['src']
		add_directory2(title,url,40,defaultfanart,image,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#40
def streams(name,url):
	response = get_html(url)
	m3u8 = re.compile('hls: \'(.+?)\'').findall(str(response))[-1].replace('https','http')
	thumbnail = defaultimage
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
	xbmc.Player().play( m3u8, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

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
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok



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

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
	print "Generate Main Menu"
	sites()
elif mode == 4:
	print "Play Video"
elif mode==20:
	print "GMM"
	sites()
elif mode==30:
	print "GMM Categories"
	cat(name,url)
elif mode==40:
	print "GMM Streams"
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
