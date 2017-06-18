#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import simplejson as json


artbase = 'special://home/addons/plugin.video.lifechurch/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.lifechurch')
self = xbmcaddon.Addon(id='plugin.video.lifechurch')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.lifechurch")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Life.Church"

#https://lifechurch-tv.churchonline.org/api/v1/events/current

defaultimage = 'special://home/addons/plugin.video.lifechurch/icon.png'
defaultfanart = 'special://home/addons/plugin.video.lifechurch/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.lifechurch/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.lifechurch').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#632
def podcast():
	html = get_html('http://feedpress.me/lifechurchipod')
	soup = BeautifulSoup(html,'html.parser').find_all('item')
	items = sorted(soup, reverse=True)
	for item in items:
		title = item.find('title').string.encode('utf-8')
		url = item.find('enclosure')['url']
		duration = item.find('itunes:duration').string.encode('utf-8')
		li = xbmcgui.ListItem(title, iconImage= defaulticon, thumbnailImage= defaultimage)
		li.setProperty('mimetype', 'video/mp4')
		li.setProperty('fanart_image',  defaultfanart)
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=50)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#631
def live():
	response = get_html('https://lifechurch-tv.churchonline.org/api/v1/events/current')
	jdata = json.loads(response)
	live_key = (jdata['response']['item']['isLive'])
	print live_key
	if str(live_key) != 'False':
		stream = 'https://churchonline-streaming.life.church/fastly/ngrp:lifechurch_adaptive/playlist.m3u8'
		listitem = xbmcgui.ListItem(plugin + ' ' + name, thumbnailImage=defaulticon)
		listitem.setProperty('mimetype', 'video/x-mpegurl')
		xbmc.Player().play( stream, listitem )
		sys.exit()
	else:
		line1 = "No Live Broadcast Available"
		line2 = "M-F: Every 90 Minutes Starting 7 AM CT"
		line3 = "5:30 PM Sat Thru 10 PM Sun"
		xbmcgui.Dialog().ok(plugin, line1, line2, line3)
		#xbmcgui.Dialog().notification(plugin, 'No Live Broadcast Available.', defaultimage, 5000, False)
		sys.exit()
		print 'No Live Broadcast Available'
		return
		xbmcplugin.endOfDirectory(addon_handle)


#633
def shows():
	add_directory2('Live', 'https://lifechurch-tv.churchonline.org/api/v1/events/current', 631, defaultfanart, defaultimage, plot='')
	add_directory2('PodCast', 'http://feedpress.me/lifechurchipod', 632, defaultfanart, defaultimage, plot='')
	html = get_html('https://www.life.church/watch/messages/')
	soup = BeautifulSoup(html,'html.parser').find_all("div",{"class":"card messages-card"})
	for show in soup:
		title = show.find('div',{'class':'card-description'}).text.encode('utf-8').strip()
		url = 'http://life.church' + str(show.find('a')['href'])
		iconimage = show.find('img')['src']
		add_directory2(title, url, 636, iconimage, iconimage, plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#634
def episodes(url):
	base = url.rpartition('/')[0]
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser')
	for show in soup.find_all("li",{"class":"grid-item md"}):
		title = striphtml(str(show.find('h5')))
		key = show.find('a')['href']
		url = base + key + '/feed/mp4-large'
		thumbnail = 'http://videos.revision3.com/revision3/images/shows' + key + key + '_web_avatar.jpg'
		add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
	add_directory2('Archives', url, 635, defaultfanart, defaultimage, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#635
def archives(url):
	response = get_html('http://www.life.church/watch/archive/')
	soup = BeautifulSoup(response,'html.parser')
	for item in soup.find_all("div",{"class":"grid-items grid-three"})[1:]:
		group = item.find_all('div',{'class':'watch-item grid-item'})
		for item in group:
			title = (item.find('h6')).string.encode('utf-8')
			image = str(item.find('img')['data-retina'])
			url = 'http://life.church' + str(item.find('a')['href'])
			add_directory2(title, url, 636, defaultfanart, image, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#636
def lifechurch_videos(url, iconimage):
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class':'messages-card'})
	print len(soup)
	for item in soup:
		if item.find('a',{'class':'messages-watch-now'}):
			continue
		title = item.find('img')['alt']
		image = item.find('img')['src']
		url = 'https://www.life.church' + item.find('a')['href']
		#print title
		add_directory(title, url, 637, defaultfanart, image, plot='')
		xbmcplugin.setContent(pluginhandle, 'episodes')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#637
def get_stream(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class':'small-12 large-10 large-offset-1 column'})
	for stream in soup:
		url = stream.find('div')['data-stream-url']
		xbmc.log('STREAM: ' + str(url))
		play(url)
	xbmcplugin.endOfDirectory(addon_handle)


def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def get_redirected_url(url):
	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
	request = opener.open(url)
	#print 'Redirect' + str(request.url)
	#playthis = request.url
	#play(playthis)
	return request.url


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def add_directory2(name,url,mode,fanart,iconimage,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok


def add_directory(name,url,mode,fanart,iconimage,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0')

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
	shows()
elif mode == 4:
	print "Play Video"
elif mode==631:
	print "Life Church Live"
	live()
elif mode==632:
	print "Life Church PodCast"
	podcast()
elif mode==633:
	print "Life Church Shows"
	shows()
elif mode==634:
	print "Life Church Episodes"
	episodes(url)
elif mode==635:
	print "Life Church Archive"
	archives(url)
elif mode==636:
	print "Life Church Videos"
	lifechurch_videos(url, iconimage)
elif mode==637:
	print "Life Church Get Stream"
	get_stream(url)
elif mode==638:
	print "Animalist Most Watched"
	most_watched(name,url)
elif mode==639:
	print "Animalist More Shows"
	more_shows(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
