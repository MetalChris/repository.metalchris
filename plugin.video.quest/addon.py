#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib



artbase = 'special://home/addons/plugin.video.quest/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.quest')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.quest")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Quest TV"

defaultimage = 'special://home/addons/plugin.video.quest/icon.png'
defaultfanart = 'special://home/addons/plugin.video.quest/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.quest/icon.png'
pubId = '4401740954001'

local_string = xbmcaddon.Addon(id='plugin.video.quest').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


#10
def stream(name,url):
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit("Stop Video")


#53
def quest_shows():
	html = get_html('http://www.questtv.co.uk/video/')
	soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"dni-video-playlist-thumb-box"})
	xbmc.log('SOUP: ' + str(len(soup)))
	for title in soup:
		#if title.find('a'):
			#url = title.find('a')['href']
		#else:
			#continue
		image = title.find('img')['src']
		plot = title.find('p').text
		videoid = title.find('div')['data-videoid']
		stream = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + str(videoid) + '&pubId=4401740954001'
		title = title.find('h3').text.encode('utf-8')
		add_directory2(title, stream, 10, defaultfanart, image, plot=plot)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_sec(duration):
	l = duration.split(':')
	return int(l[0]) * 60 + int(l[1])


def play(url):
	print url
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=10)
		return ok

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def get_json(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'edge.api.brightcove.com')
	req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')
	req.add_header('Accept', 'application/json;pk=BCpkADawqM0dhxjC63Ux5MXyiMyIYB1S1bvk0iorISSaD1jFgWDyiv-JAcvE6XduNdDYxMdk_NTQWn91IQI9NLPkXd5UIw3cv49pcyJ5eW9QT0CWTrclSFHBHqSSyJ_9Ysgzc2v-Mw0wxNmZ')

	try:
		response = urllib2.urlopen(req)
		json = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		json = False
	return json




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
	quest_shows()
elif mode == 1:
	print "Indexing Videos"
	INDEX(url)
elif mode == 4:
	print "Play Video"
elif mode == 10:
	print "Get Quest Stream"
	stream(name,url)
elif mode == 53:
	print "Quest Shows"
	cfl_2016(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
