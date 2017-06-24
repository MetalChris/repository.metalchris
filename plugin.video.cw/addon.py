#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)


import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys
import simplejson as json
from bs4 import BeautifulSoup
import html5lib


artbase = 'special://home/addons/plugin.video.cw/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.cw')
self = xbmcaddon.Addon(id='plugin.video.cw')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.cw")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "CW TV Network"

defaultimage = 'special://home/addons/plugin.video.cw/icon.png'
defaultfanart = 'special://home/addons/plugin.video.cw/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.cw/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.cw').getLocalizedString
addon_handle = int(sys.argv[1])
#p = settings.getSetting(id="parser")
#e = settings.getSetting(id="encoding")
confluence_views = [500,501,502,503,504,508,515]


#533
def sites():
		addDir('CW TV Network', 'http://www.cwtv.com/shows/', 534, defaultimage)
		addDir('CW Seed', 'http://www.cwseed.com/shows/', 535, artbase + 'seed.png', artbase + 'seed.jpg')
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


#534
def cw():
		addDir('Episodes', 'http://www.cwtv.com/shows/', 633, defaultimage)
		addDir('Clips', 'http://www.cwtv.com/shows/', 633, defaultimage)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


#535
def seed():
		addDir('Episodes', 'http://www.cwseed.com/shows/', 635, artbase + 'seed.png', artbase + 'seed.jpg')
		addDir('Clips', 'http://www.cwseed.com/shows/', 635, artbase + 'seed.png', artbase + 'seed.jpg')
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


#633
def shows(name,url):
	if name == 'Episodes':
		mode = 30
	else:
		mode = 31
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('a',{'class':'hublink'})
	for title in soup:
		name = striphtml(str(title)).strip()
		url = 'http://www.cwtv.com' + title.get('href')
		image = title.find('img')['src']
		add_directory2(name,url,mode,defaultfanart,image,plot='')#; i = i + 1
		xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#635
def seed_shows(name,url):
	if name == 'Episodes':
		mode = 30
	else:
		mode = 31
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('li',{'class':'showitem'})
	print len(soup)
	for title in soup:
		if title.find('div'):
			name = striphtml(str(title)).strip()
			url = 'http://www.cwseed.com' + (title.find('a')['href'])[:-1]
			image = title.find('img')['data-src']
			add_directory2(name,url,mode,artbase + 'seed.jpg',image,plot='')#; i = i + 1
			xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#30
def get_json(url):
	show = url.rpartition('/')[-1]
	url = 'http://www.cwtv.com/feed/mobileapp/videos?show=' + show + '&api_version=3'
	xbmc.log('JSON_URL: ' + str(url))
	response = urllib2.urlopen(url)
	jdata = json.load(response); i = 0
	count = len(jdata['videos'])
	for i in range(count):
		if jdata['videos'][i]['fullep'] != 1:
			continue
		title = jdata['videos'][i]['title']
		image = jdata['videos'][i]['large_thumbnail']
		ep = jdata['videos'][i]['episode']
		airdate = jdata['videos'][i]['airdate']
		description = jdata['videos'][i]['description_long']
		duration = jdata['videos'][i]['duration_secs']
		episode = jdata['videos'][i]['availability_asset_id'].rpartition('-')[-1]
		#title = title + ' - ' + episode
		url = 'https://www.cwtv.com/ioshlskeys/videos' + (image.split('thumbs')[-1]).split('_CWtv')[0] + '.m3u8'
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
		li.setProperty('fanart_image', image)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Episode": ep, "Premiered": airdate})
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
    	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
		#add_directory2(title,url,30,image,image,plot=''); i = i + 1
	xbmcplugin.endOfDirectory(addon_handle)



#31
def get_clips(url):
	show = url.rpartition('/')[-1]
	url = 'http://www.cwtv.com/feed/mobileapp/videos?show=' + show + '&api_version=3'
	response = urllib2.urlopen(url)
	jdata = json.load(response); i = 0
	count = len(jdata['videos'])
	for i in range(count):
		if jdata['videos'][i]['fullep'] != 0:
			continue
		title = jdata['videos'][i]['title']
		image = jdata['videos'][i]['large_thumbnail']
		ep = jdata['videos'][i]['episode']
		airdate = jdata['videos'][i]['airdate']
		description = jdata['videos'][i]['description_long']
		episode = jdata['videos'][i]['availability_asset_id'].rpartition('-')[-1]
		#title = title + ' - ' + episode
		url = 'https://www.cwtv.com/ioshlskeys/videos' + (image.split('thumbs')[-1]).split('_CWtv')[0] + '.m3u8'
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
		li.setProperty('fanart_image', image)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Episode": ep, "Premiered": airdate})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
    	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
		#add_directory2(title,url,30,image,image,plot=''); i = i + 1
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


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

def add_directory2(name,url,mode,fanart,thumbnail,plot,showcontext=False):
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
elif mode==533:
	print "CW TV Network Main Menu"
	sites()
elif mode==534:
	print "CW TV Network Menu"
	cw()
elif mode==535:
	print "CW Seed Menu"
	seed()
elif mode==633:
	print "CW TV Network Main Menu"
	shows(name,url)
elif mode==635:
	print "CW TV Network Seed Menu"
	seed_shows(name,url)
elif mode==30:
	print "CW TV Episodes JSON"
	get_json(url)
elif mode==31:
	print "CW TV Clips JSON"
	get_clips(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
