#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib

artbase = 'special://home/addons/plugin.video.msl/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.msl')
self = xbmcaddon.Addon(id='plugin.video.msl')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.msl")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Mars Science Laboratory"

defaultimage = 'special://home/addons/plugin.video.msl/icon.png'
defaultfanart = 'special://home/addons/plugin.video.msl/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.msl/icon.png'
baseurl = 'http://mars.jpl.nasa.gov/multimedia'

local_string = xbmcaddon.Addon(id='plugin.video.msl').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


def cats():
	addDir('All Videos', baseurl + '/videos/?searchTerm=All', 636, defaultimage)
	addDir('Rovers', baseurl, 631, defaultimage)
	addDir('Orbiters', baseurl, 632, defaultimage)

def rovers():
	addDir('Curiosity', baseurl + '/videos/?searchTerm=Mission:MSL', 636, defaultimage)
	addDir('Opportunity', baseurl + '/videos/?searchTerm=Mission:MERB', 636, defaultimage)
	addDir('Spirit', baseurl + '/videos/?searchTerm=Mission:MERA', 636, defaultimage)

def orbiters():
	addDir('MAVEN', baseurl + '/videos/?searchTerm=Mission:MAVEN', 636, defaultimage)
	addDir('Mars Reconaissance Orbiter', baseurl + '/videos/?searchTerm=Mission:MRO', 636, defaultimage)
	addDir('2001 Mars Odyssey', baseurl + '/videos/?searchTerm=Mission:Odyssey', 636, defaultimage)


#636
def msl_videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('li')
	QUALITY = settings.getSetting(id="quality")
	if QUALITY !='0':
		mode = 637
	else:
		mode = 640
	for item in soup[30:]:
		title = item.find('h2').text.encode('utf-8')
		image = 'http://mars.nasa.gov' + re.compile('url\\((.+?)\\)').findall(str(item))[-1] # 'http://mars.nasa.gov' + item.find('img')['src']
		#xbmc.log(str(image))
		url = (baseurl + item.find('a')['href']).replace('..','')#image.replace('.jpg','-1280.mp4')
		description = item.find('div',{'class':'listTextLabel'}).text.encode('utf-8')
		add_directory2(title, url, mode, image, image, plot=description)
		xbmcplugin.setContent(pluginhandle, 'episodes')
		views = settings.getSetting(id="views")
	if views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#637
def source(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('div',{'class':'flowplayer is-splash'})
	url = 'http://mars.nasa.gov' + re.compile('src="(.+?)"').findall(str(soup))[-1]
	title = re.compile('">(.+?)<span').findall(str(soup))[-1]
	image = 'http://mars.nasa.gov' + re.compile("url\\(\\'(.+?)\\'\\)").findall(str(soup))[-1]
	listitem = xbmcgui.ListItem(name, thumbnailImage=image)
	xbmc.Player().play(url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#640
def files(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('li')
	elements = [];links = []
	for item in soup[30:]:
		title = item.find('a').text.strip().encode('utf-8')
		url = item.find('a')['href']
		if 'pdf' in title:
			continue
		elements.append(title)
		links.append(url.encode('utf-8'))
	dialog = xbmcgui.Dialog()
	ret = xbmcgui.Dialog().select('Select Quality',elements)
	xbmc.log(str(ret))
	url = 'http://mars.nasa.gov' + links[ret]
	image = url.split('-')[0] + '.jpg'
	listitem = xbmcgui.ListItem(name, thumbnailImage=image)
	xbmc.Player().play(url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


#638
def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo(type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok

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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu")
	cats()
elif mode == 4:
	xbmc.log("Play Video")
elif mode==631:
	xbmc.log("Mars Rovers")
	rovers()
elif mode==632:
	xbmc.log("Mars Orbiters")
	orbiters()
elif mode==634:
	xbmc.log("Mars Science Laboratory Categories")
	cats()
elif mode==636:
	xbmc.log("Mars Science Laboratory Videos")
	msl_videos(url)
elif mode==637:
	xbmc.log("Mars Science Laboratory Sources")
	source(url)
elif mode==638:
	xbmc.log("Play Video")
	play(url)
elif mode==640:
	xbmc.log("Mars Science Laboratory Files")
	files(name, url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
