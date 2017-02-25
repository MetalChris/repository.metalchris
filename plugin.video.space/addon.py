#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys
from bs4 import BeautifulSoup
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
#settings = xbmcaddon.Addon(id="plugin.video.space")
#views = settings.getSetting(id="views")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

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
	response = br.open('http://www.space.com/news?type=video')
	page = response.get_data()
	soup = BeautifulSoup(page,'html5lib').find_all('ul',{'id':'filter-categories'})
	cats = BeautifulSoup(str(soup),'html5lib').find_all('li')
	for item in cats:
		title = item.find('a').text.encode('utf-8').replace('&amp;','&').strip()
		url = baseurl + 'news?type=video&section=' + item.find('a')['data-slug']
		if 'all-sections' in url:
			url = baseurl + 'news?type=video'
		addDir(title, url, 633, defaulticon, defaultfanart)
	#if views != 'false':
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#633
def videos(url):
	next_url = url.split('?')
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	soup = BeautifulSoup(page,'html5lib').find_all('li',{'class':'search-item line pure-g'})
	for item in soup:
		title = item.find('h2').text.encode('utf-8').replace('&amp;','&').strip()
		url = baseurl + item.find('a')['href']
		image = item.find('img')['src']
		plot = item.find('p',{'class':'mod-copy'}).text.strip()
		infoLabels = {"Title": name,"plot": plot}
		addDir2(title, url, 636, image, defaultfanart)
	if 'class="next"' in page:
		count = int((re.compile('rel="next" href="(.+?)"').findall(page)[0])[-1:])
		next_page = next_pre + str(count) + '?' + next_url[1]
		addDir('Load More Videos', next_page, 633, defaultimage, defaultfanart)
	#if views != 'false':
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[0])+")")
	xbmcplugin.setContent(addon_handle, content="videos")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def stream(name,url,iconimage):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	key = re.compile('video_id":"(.+?)"').findall(str(page))
	jurl = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/None/' + key[0] + '?device=html5&domain=www.spacemag.com'
	#'http://player.ooyala.com/player/all/' + key[0] + '_6000.m3u8'
	jgresponse = get_html(jurl)
	jgdata = json.loads(jgresponse)
	url = (jgdata["authorization_data"][key[0]]["streams"][3]["url"]["data"]).decode('base64')
	play(name,url,iconimage)
	xbmcplugin.endOfDirectory(addon_handle)



def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(name,url,iconimage):
	item = xbmcgui.ListItem(name, path=url, thumbnailImage=iconimage)
	xbmc.Player().play( url, item )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'player.ooyala.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	#req.add_header('Referer', 'http://www.space.com/news?type=video')
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


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=True):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Space.com Main Menu")
	cats()
elif mode==630:
	xbmc.log("Space.com Categories")
	cats()
elif mode==633:
	xbmc.log("Space.com Videos")
	videos(url)
elif mode==636:
	xbmc.log("Space.com Stream")
	stream(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
