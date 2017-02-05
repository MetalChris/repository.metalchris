#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, os, platform, re, xbmcplugin, sys
import requests
from bs4 import BeautifulSoup
import simplejson as json
#import base64
## a.decode('base64') ##


artbase = 'special://home/addons/plugin.video.airspace/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.airspace')
self = xbmcaddon.Addon(id='plugin.video.airspace')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.airspace")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Smithsonian Air & Space"

defaultimage = 'special://home/addons/plugin.video.airspace/icon.png'
defaultfanart = 'special://home/addons/plugin.video.airspace/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.airspace/icon.png'
baseurl = 'http://www.airspacemag.com'

local_string = xbmcaddon.Addon(id='plugin.video.airspace').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#633
def index():
	response = get_html('http://www.airspacemag.com/videos/category/new-label/?no-ist')
	soup = BeautifulSoup(response,'html.parser')
	match = re.compile('value="(.+?)">(.+?)</option').findall(str(soup))
	for link, title in match[2:9]:
		title = title.encode('utf-8').replace('&amp;','&')
		if 'Channel' in title:
			mode = 635
		else:
			mode =636
		url = baseurl + link + '?no-ist'
		addDir2(title, url, mode, defaulticon, defaultfanart)
	views = settings.getSetting(id="views")
	if views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#635
def sc_videos(url):
	response = get_html(url)
	n = BeautifulSoup(response,'html.parser').find_all('a',{'class':'next pager'})
	if len(n) > 0:
		nextp = str(re.compile('href="(.+?)">').findall(str(n))[-1])
		nextpage = (url.rsplit('/',1))[0] + '/' + nextp
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class':'teaser-list'})
	items = BeautifulSoup(str(soup),'html.parser').find_all('a',{'class':'media-teaser '})
	for item in items:
		title = item.find('h5').text.strip()
		duration = title.split('   ')[-1]
		title = remove_non_ascii_1(title).split('   ')[0]
		image = item.find('img')['src']
		key = (re.compile('data-api_id="(.+?)"').findall(str(item))[-1])[:32]
		jurl = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/None/' + key + '?device=html5&domain=www.airspacemag.com'		
		description = item.find('span',{'class':'description hidden'}).text + ' ' + duration
		add_directory2(title,jurl,637,image,image,plot=description)
	if len(n) > 0:
		addDir2('Next Page', nextpage, 636, defaulticon, defaultfanart)
	#xbmc.log(str image)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	views = settings.getSetting(id="views")
	if views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def videos(url):
	response = get_html(url)
	next = BeautifulSoup(response,'html.parser').find_all('a',{'class':'next pager'})
	if len(next) > 0:
		nextp = str(re.compile('href="(.+?)">').findall(str(next))[-1])
		nextpage = (url.rsplit('/',1))[0] + '/' + nextp
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class':'teaser-list'})
	items = BeautifulSoup(str(soup),'html.parser').find_all('a',{'class':'media-teaser '})
	for item in items:
		title = item.find('h5').text.strip()
		duration = title.split('   ')[-1]
		title = remove_non_ascii_1(title).split('   ')[0]
		image = item.find('img')['src']
		key = (re.compile('data-api_id="(.+?)"').findall(str(item))[-1])[:32]
		jurl = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/None/' + key + '?device=html5&domain=www.airspacemag.com'		
		description = item.find('span',{'class':'description hidden'}).text + ' ' + duration
		add_directory2(title,jurl,638,image,image,plot=description)
	if len(next) > 0:
		addDir2('Next Page', nextpage, 636, defaulticon, defaultfanart)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	views = settings.getSetting(id="views")
	if views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#637
def sc_streams(url):
	key = re.compile('None/(.+?)\\?').findall(str(url))[-1]
	murl = 'http://player.ooyala.com/player/all/' + key + '.m3u8'
	r = requests.head(murl)
	#xbmc.log(str r.status_code)# == 404:
	if r.status_code == 200:
		play(murl)
	else:
		jgresponse = urllib2.urlopen(url)
		jgdata = json.load(jgresponse)
		url = (jgdata["authorization_data"][key]["streams"][3]["url"]["data"]).decode('base64')
		play(url)


#638
def streams(url):
	key = re.compile('None/(.+?)\\?').findall(str(url))[-1]; i = 0
	jgresponse = urllib2.urlopen(url)
	jgdata = json.load(jgresponse)
	for item in (jgdata["authorization_data"][key]):
		dtype = (jgdata["authorization_data"][key]["streams"][i]["delivery_type"])
		#xbmc.log(str(dtype))
		if 'hls' in dtype:
			url = ((jgdata["authorization_data"][key]["streams"][i]["url"]["data"]).decode('base64'))#.split('\\?')[0]
		#xbmc.log(str(url))
			play(url)
			break
		elif 'mp4' in dtype:
			bitrate = ((jgdata["authorization_data"][key]["streams"][i]["video_bitrate"]))
		#xbmc.log(str(bitrate))
			if bitrate >= 1200:
				url = ((jgdata["authorization_data"][key]["streams"][i]["url"]["data"]).decode('base64'))#.split('\\?')[0]
				#xbmc.log(str(url))
				play(url)
				break
		i = i + 1



def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
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

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'www.airspacemag.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	req.add_header('Referer', 'http://www.airspacemag.com/videos/')
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


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
	mode = int(params["mode"])
except:
	pass

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Smithsonian Air & Space Main Menu")
	index()
elif mode == 4:
	xbmc.log("Play Video")
elif mode==633:
	xbmc.log("Smithsonian Air & Space")
	index()
elif mode==635:
	xbmc.log("Smithsonian Air & Space Videos")
	sc_videos(url)
elif mode==636:
	xbmc.log("Smithsonian Air & Space Videos")
	videos(url)
elif mode==637:
	xbmc.log("Smithsonian Air & Space Streams")
	sc_streams(url)
elif mode==638:
	xbmc.log("Smithsonian Air & Space Streams")
	streams(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
