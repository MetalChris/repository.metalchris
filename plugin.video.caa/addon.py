#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, calendar, re, sys, os
#from bs4 import BeautifulSoup
#import HTMLParser
import simplejson as json
#import html5lib
#from urllib import urlopen
#import requests
from datetime import date, datetime, timedelta as td
import time
#import mechanize
#import cookielib

today = time.strftime("%m-%d-%Y")

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
#CookieJar = cookielib.LWPCookieJar(os.path.join(addon_path_profile, 'cookies.lwp'))
#br = mechanize.Browser()
#br.set_cookiejar(CookieJar)
#br.set_handle_robots(False)
#br.set_handle_equiv(False)
#br.addheaders = [('Host', 'www.campusinsiders.com')]
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0')]

selfAddon = xbmcaddon.Addon(id='plugin.video.caa')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.caa/icon.png'
defaultfanart = 'special://home/addons/plugin.video.caa/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.caa/icon.png'
defaulticon = 'special://home/addons/plugin.video.caa/icon.png'

addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]


def CATEGORIES():
	addDir('CAA.TV Live', 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + today +'&clientID=47302&broadcastType=live&token=&school=&_=%5Bobject+Object%5D', 5, defaultimage)
	#addDir('CAA.TV Schedule', 'https://watchstadium.com/schedule/', 10, defaultimage)
	addDir('CAA.TV On Demand', 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + today +'&clientID=47302&broadcastType=vod&token=&school=&_=%5Bobject+Object%5D', 7, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#5
def LIVE(name,url):
	response = get_html(url)
	data = json.loads(response)#; i = 0
	total = len(data['events'])
	#xbmc.log('TOTAL: ' + str(total))
	for i in range(total):
		#xbmc.log('HAS VIDEO: ' + str(hasVideo))
		title = data['events'][i]['mobileTitle']
		timeString = data['events'][i]['timeString']
		event = data['events'][i]['type']
		isLive = data['events'][i]['isLive']
		if isLive == True:
			title = '[LIVE] ' + title + ' (' + event + ')'
		else:
			title = '[' + timeString +'] ' + title + ' (' + event + ')'
		eventID = data['events'][i]['eventID']
		clientID = data['events'][i]['clientID']
		hasVideo = data['events'][i]['hasVideo']
		if hasVideo != True:
			continue
		url = 'https://neo-client.stretchinternet.com/streamservice.portal?clientID=' + str(clientID) + '&userID=-1&broadcastType=live&method=getStream&eventID=' + str(eventID) + '&streamType=video'
		addDir2(title, url, 20, defaultimage, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#6
def VOD(name,url):
	response = get_html(url)
	data = json.loads(response)#; i = 0
	total = len(data['events'])
	#xbmc.log('TOTAL: ' + str(total))
	for i in range(total):
		hasVideo = data['events'][i]['hasVideo']
		if hasVideo != True:
			continue
		#xbmc.log('HAS VIDEO: ' + str(hasVideo))
		title = data['events'][i]['mobileTitle']
		#xbmc.log('TITLE: ' + str(title))
		timeString = data['events'][i]['timeString']
		event = data['events'][i]['type']
		title = title + ' (' + event + ')'
		eventID = data['events'][i]['eventID']
		clientID = data['events'][i]['clientID']
		url = 'https://neo-client.stretchinternet.com/streamservice.portal?clientID=' + str(clientID) + '&userID=-1&broadcastType=vod&method=getStream&eventID=' + str(eventID) + '&streamType=video'
		addDir2(title, url, 10, defaultimage, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#7
def ON_DEMAND():
	current = datetime.utcnow() - td(hours=5)
	for i in range(0,11):
		aday = str(current - td(days=i)).split(' ')[0]
		#xbmc.log('ADAY: ' + str(aday))
		s = aday.replace('-','')
		#xbmc.log('S: ' + str(s))
		title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
		urlday = title.strftime("%m-%d-%Y")
		#xbmc.log('UDAY: ' + str(urlday))
		#day = title.strftime ("%Y-%m-%d")
		title = title.strftime("%B %d, %Y")
		title = str(title.replace(' 0', ' '))
		url = 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + urlday +'&clientID=47302&broadcastType=vod&token=&school=&_=%5Bobject+Object%5D'
		addDir(title,url,6, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#10
def VOD_JSON(name,url):
	response = get_html(url)
	data = json.loads(response)
	mountPointServiceUrl = data['mountPointServiceUrl']
	#xbmc.log('MPU: ' + str(mountPointServiceUrl))
	mP = get_html(mountPointServiceUrl)
	#mP = mountPointServiceUrl.split('/')
	#xbmc.log('MP: ' + str(mP))
	streamHDURL = data['streamURL']
	streams = streamHDURL.split('#')
	#xbmc.log('STREAMS: ' + str(streams))
	stream = streams[0] + mP#[2] + streams[-1]
	xbmc.log('STREAM: ' + str(stream))
	#stream = 'rtmp://' + lB[2] +
	#stream = re.sub("\#[^#]*", lB[2], streamHDURL)
	PLAY(name, stream)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#20
def GET_PAGE(name,url):
	response = get_html(url)
	data = json.loads(response)
	loadBalancerUrl = data['loadBalancerUrl']
	lB = loadBalancerUrl.split('/')
	#xbmc.log('LB: ' + str(lB))
	streamHDURL = data['streamURL']
	streams = streamHDURL.split('#')
	#xbmc.log('STREAMS: ' + str(streams))
	stream = streams[0] + lB[2] + streams[-1] + ' live=true'
	xbmc.log('STREAM: ' + str(stream))
	#stream = 'rtmp://' + lB[2] +
	#stream = re.sub("\#[^#]*", lB[2], streamHDURL)
	PLAY(name, stream)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	listitem.setInfo(type="Video", infoLabels={"Title": name})
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def sanitize(data):
	output = ''
	for i in data:
		for current in i:
			if ((current >= '\x20') and (current <= '\xD7FF')) or ((current >= '\xE000') and (current <= '\xFFFD')) or ((current >= '\x10000') and (current <= '\x10FFFF')):
			   output = output + current
	return output



def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0')

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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("CAA.TV Menu")
	CATEGORIES()
elif mode == 5:
	xbmc.log("CAA.TV Live")
	LIVE(name,url)
elif mode == 6:
	xbmc.log("CAA.TV Live")
	VOD(name,url)
elif mode == 7:
	xbmc.log("CAA.TV On Demand")
	ON_DEMAND()
elif mode == 10:
	xbmc.log("CAA.TV Get Stream")
	VOD_JSON(name,url)
elif mode == 20:
	xbmc.log("CAA.TV Get Stream")
	GET_PAGE(name,url)
elif mode == 99:
	xbmc.log("Play Video")
	PLAY(name,url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))