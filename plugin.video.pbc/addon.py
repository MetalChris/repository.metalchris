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

artbase = 'special://home/addons/plugin.video.pbc/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.pbc')
self = xbmcaddon.Addon(id='plugin.video.pbc')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.pbc")
#views = settings.getSetting(id="views")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

plugin = "Premier Boxing Champions (PBC)"

defaultimage = 'special://home/addons/plugin.video.pbc/icon.png'
defaultfanart = 'special://home/addons/plugin.video.pbc/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.pbc/icon.png'
baseurl = 'http://www.premierboxingchampions.com'

local_string = xbmcaddon.Addon(id='plugin.video.pbc').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


def index():
	addDir('Latest Videos', 'http://www.premierboxingchampions.com/boxing-videos', 630, defaultimage, defaultfanart)
	addDir('Past Fights', 'http://www.premierboxingchampions.com/past-boxing-fights', 632, defaultimage, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle)


#630
def latest(url):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	data = (re.compile('\\"featured_videos\\":(.+?)\\,\\"haymon_ooyala_v4_vars\\"').findall(str(page)))[0]
	jdata = json.loads(data)
	count = 0
	for videos in (jdata['videos']):
		count = count + 1
	for i in range(0,count):
		items = jdata['videos'][i]['videos']
		for item in items:
			#if 'Full Fight' in (item['tag']):
				title = (item['title'])#.replace('highlights','Highlights').replace('full fight','Full Fight')
				image = item['thumbnail']
				url = (image.rpartition('/')[-1]).split('.')[0]
				addDir(title, url, 640, image, image)
	xbmcplugin.endOfDirectory(addon_handle)


#632
def past_years(url):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	soup = BeautifulSoup(page,'html5lib').find_all('ul',{'class':'col-xs-offset-1 col-xs-22 col-sm-offset-0 col-sm-24 col-md-offset-2 col-md-20 fights-nav'})
	match = re.compile('href="(.+?)">(.+?)</').findall(str(soup))
	for url, year in match:
		url = baseurl + url
		addDir(year, url, 633, defaultimage, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle)



#633
def past_fights(url):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'row'})
	#xbmc.log('SOUP: ' + str(len(soup)))
	for item in soup[3:]:
		if not item.find('a',{'class':'bout-title'}) or not item.find('a',{'class':'view-video'}):
			continue
		title = item.find('a',{'class':'bout-title'}).text.strip().replace('\n', ' ').replace('\r', '').replace('  ','')# + ' Highlights'
		urls = item.find('ul',{'class':'past-fights__video_links list-unstyled list-inline pull-right-md'})
		for link in urls:
			url = re.compile('href="(.+?)"').findall(str(link))
			if len(url) > 0:
				#continue
				clip_type = link.find('a',{'class':'view-video'}).text.strip()
				url = str(baseurl + url[0])
				#xbmc.log('TYPE: ' + str(clip_type))
				#if 'full-fight' in url:
				title = title + ' - ' + clip_type
				if 'Full fight' in title:
					title = title.replace(' - Highlights','')
			else:
				continue
			addDir(title, url, 636, defaultimage, defaultfanart)
	if 'class="item-list"' in page:
		soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'item-list'})
		for next_page in soup:
			next_page = baseurl + next_page.find('a')['href']
		#xbmc.log('NEXT: ' + str(next_page))
		addDir('Load More Videos', next_page, 633, defaultimage, defaultfanart)
	xbmcplugin.setContent(addon_handle, content="videos")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def get_key(name,url,iconimage):
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'inline-video'})
	for key in soup:
		url = key.get('data-video')
	stream(name,url,iconimage)


#640
def stream(name,url,iconimage):
	key = url
	jurl = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/None/' + key + '?device=html5&domain=www.premierboxingchampions.com'
	#xbmc.log('JURL: ' + str(jurl))
	#'http://player.ooyala.com/player/all/' + key[0] + '_6000.m3u8'
	jgresponse = get_html(jurl)
	jgdata = json.loads(jgresponse)
	url = (jgdata["authorization_data"][key]["streams"][6]["url"]["data"]).decode('base64')
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
	xbmc.log("Generate PBC Main Menu")
	index()
elif mode==630:
	xbmc.log("PBC Latest")
	latest(url)
elif mode==632:
	xbmc.log("PBC Past Years")
	past_years(url)
elif mode==633:
	xbmc.log("PBC Past Fights")
	past_fights(url)
elif mode==636:
	xbmc.log("PBC Key")
	get_key(name,url,iconimage)
elif mode==640:
	xbmc.log("PBC Stream")
	stream(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
