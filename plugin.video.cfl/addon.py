#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib
import simplejson as json

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


def cfl(url):
		addDir('Latest', 'http://www.cfl.ca/videos/latest-news/', 53, artbase + 'cfl.jpg')
		addDir('Game Previews', 'http://www.cfl.ca/videos/game-previews/', 53, artbase + 'cfl.jpg')
		addDir('2016 Game Recaps', 'http://www.cfl.ca/videos/2016-game-recaps/', 53, artbase + 'cfl.jpg')
		addDir('Analysis', 'http://www.cfl.ca/videos/analysis/', 53, artbase + 'cfl.jpg')
		addDir('Highlights', 'http://www.cfl.ca/videos/highlights/', 53, artbase + 'cfl.jpg')
		addDir('Kegsize Plays of the Week', 'http://www.cfl.ca/videos/kegsize-plays-of-the-week/', 53, artbase + 'cfl.jpg')
		addDir('103rd Grey Cup', 'http://www.cfl.ca/videos/gc103/', 53, artbase + 'cfl.jpg')
		addDir('2015 Game Recaps', 'http://www.cfl.ca/videos/recaps/', 53, artbase + 'cfl.jpg')

		xbmcplugin.endOfDirectory(int(sys.argv[1]))

#10
def stream(url):
	html = get_html(url)
	videoId = re.compile('iframe-(.+?)"').findall(html)
	print videoId[0]
	data = get_json('https://edge.api.brightcove.com/playback/v1/accounts/4401740954001/videos/' + str(videoId[0]))
	jgdata = json.loads(data)
	stream = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + str(videoId[0]) + '&pubId=4401740954001'
	description = jgdata['description']
	title = jgdata['name']
	image = jgdata['poster']
	print title
	print description
	print image
	print stream
	listitem = xbmcgui.ListItem(title, thumbnailImage=image)
	xbmc.Player().play( stream, listitem )
	sys.exit("Stop Video")


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
		keys = image.split('_')
		key = (keys[-1].split('-'))[0]
		if len(key) != 13:
			continue
		stream = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + key + '&pubId=4401740954001'
		#duration = striphtml(str(item.find('span', {'class':'time-bar'})))
		#duration = int(get_sec(duration))
		#print duration
		#title.addStreamInfo('video', { 'duration': duration })
		add_directory2(title, stream, 99, image, image, plot='')
	xbmcplugin.setContent(pluginhandle, 'episodes')


def get_sec(duration):
	l = duration.split(':')
	return int(l[0]) * 60 + int(l[1])


def play(name,url):
	print url
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit("Stop Video")
	#item = xbmcgui.ListItem(path=url)
	#item.setProperty('IsPlayable', 'true')
	#return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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

xbmcplugin.endOfDirectory(int(sys.argv[1]))
