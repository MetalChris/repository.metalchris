#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import html5lib

artbase = 'special://home/addons/plugin.video.cfl/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.cfl')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.cfl")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "CFL Video"

defaultimage = 'special://home/addons/plugin.video.cfl/icon.png'
defaultfanart = 'special://home/addons/plugin.video.cfl/resources/media/FBCL-20120713121328.jpg'
defaulticon = 'special://home/addons/plugin.video.cfl/icon.png'
fanart = 'special://home/addons/plugin.video.cfl/media/FBCL-20120713121328.jpg'
cflfanart = 'special://home/addons/plugin.video.cfl/resources/media/FBCL-20120713121328.jpg'
pubId = '4401740954001'

local_string = xbmcaddon.Addon(id='plugin.video.cfl').getLocalizedString
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]
baseurl = 'http://www.cfl.ca/videos'


def cfl(baseurl):
	html = get_html('http://www.cfl.ca/videos')
	soup = BeautifulSoup(html,'html5lib').find_all("ul",{"id":"dropdown-filter-featured"})[0]
	for anchor in soup.find_all('a'):
		title = anchor.text
		url = 'http://www.cfl.ca/videos/' + anchor.get('href')
		addDir(title, url, 53, artbase + 'cfl.jpg')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#53
def cfl_2016(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"video-items-section"})[0]
	for item in soup.find_all("div",{"class":"landing-video-cell"}):
		h2 = item.find('h2')
		title = striphtml(str(h2.find('a')))
		url = h2.find('a')['href']
		image = item.find("div",{"class":"card-image"})
		image = ((re.compile('(\'(.+?)\')').findall(str(image))[0])[0]).replace("'","")
		url = 'plugin://plugin.video.cfl?mode=55&url=' + urllib.quote_plus(url)
		li = xbmcgui.ListItem(title)
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"Sports"})
		li.setArt({'thumb':image,'fanart':defaultfanart})
		xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(pluginhandle, cacheToDisc=True)


#55
def get_stream(url):
	xbmc.log('URL: ' + str(url))
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("iframe",{"class":"brightcove-iframe"})[0]
	xbmc.log('SOUP: ' + str(soup))
	key = re.compile('videoId=(.+?)&amp;').findall(str(soup))[0]
	xbmc.log('KEY: '  + str(key))
	stream = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + key + '&pubId=4401740954001'
	xbmc.log('STREAM: ' + str(stream))
	PLAY(stream)
	xbmcplugin.endOfDirectory(pluginhandle, cacheToDisc=True)


#99
def PLAY(url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log('### SETRESOLVEDURL ###')
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=xbmc.LOGDEBUG)
	xbmcplugin.endOfDirectory(pluginhandle)


def get_sec(duration):
	l = duration.split(':')
	return int(l[0]) * 60 + int(l[1])


def play(name,url):
	print url
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit("Stop Video")


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
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

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host','www.cfl.ca')
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
	cfl(url)
elif mode == 1:
	print "Indexing Videos"
	INDEX(url)
elif mode == 99:
	play(name,url)
	print "Play Video"
elif mode == 10:
	print "Get CFL Stream"
	stream(url)
elif mode == 53:
	print "CFL 2016"
	cfl_2016(url)
elif mode == 55:
	print "CFL Get Stream"
	get_stream(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
