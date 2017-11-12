#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, sys, os
import json
from datetime import datetime, timedelta as td
import time
import socket

today = time.strftime("%m-%d-%Y")

addon_id = 'plugin.video.caa'
selfAddon = xbmcaddon.Addon(id=addon_id)
translation = selfAddon.getLocalizedString
#addon_version = selfAddon.getAddonInfo('version')
#settings = xbmcaddon.Addon(id=addon_id)

schools = ['charleston', 'delaware', 'drexel', 'elon', 'hofstra', 'madison', 'mary', 'northeastern','towson', 'uncw']

defaultimage = 'special://home/addons/plugin.video.caa/icon.png'
defaultfanart = 'special://home/addons/plugin.video.caa/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.caa/icon.png'
artbase = 'special://home/addons/plugin.video.caa/resources/media/'

plugin = 'CAA TV'

addon_handle = int(sys.argv[1])


def CATEGORIES():
	addDir('CAA.TV Live', 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + today +'&clientID=47302&broadcastType=live&token=&school=&_=%5Bobject+Object%5D', 15, defaultimage)
	addDir('CAA.TV On Demand', 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + today +'&clientID=47302&broadcastType=vod&token=&school=&_=%5Bobject+Object%5D', 7, defaultimage)
	xbmcplugin.endOfDirectory(addon_handle)


#5
def LIVE(name,url):
	response = get_html(url)
	data = json.loads(response)
	total = len(data['events'])
	for i in range(total):
		sport = data['events'][i]['type']
		if name != sport:
			continue
		title = data['events'][i]['mobileTitle']
		timeString = data['events'][i]['timeString']
		event = data['events'][i]['type']
		title = '[' + timeString +'] ' + title + ' (' + event + ')'
		eventID = data['events'][i]['eventID']
		clientID = data['events'][i]['clientID']
		m_type = 'video'
		hasVideo = data['events'][i]['hasVideo']
		if hasVideo != True:
			title = title + ' * ' + translation(30002) + ' *'
			m_type = 'audio'
		img_key = (data['events'][i]['customText']).split(' ')[-1].lower()
		if img_key in schools:
			image = os.path.join(artbase,img_key + '.png')
		else:
			image = defaultimage
		jurl = 'https://neo-client.stretchinternet.com/streamservice.portal?clientID=' + str(clientID) + '&userID=-1&broadcastType=live&method=getStream&eventID=' + str(eventID) + '&streamType=' + str(m_type)
		url = 'plugin://plugin.video.caa?mode=20&url=' + urllib.quote_plus(jurl)
		li = xbmcgui.ListItem(title)
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"Sports"})
		li.setArt({'thumb':image,'fanart':defaultfanart})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#15
def GET_SPORTS(name,url):
	if 'Live' in name:
		mode = 5
	else:
		mode = 6
	sports = []
	response = get_html(url)
	data = json.loads(response)
	total = len(data['events'])
	for i in range(total):
		sport = data['events'][i]['type']
		if not sport in sports:
			sports.append(sport)
	for sport in sorted(sports):
		addDir(sport, url, mode, defaultimage, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#6
def VOD(name,url):
	response = get_html(url)
	data = json.loads(response)
	total = len(data['events'])
	xbmc.log('TOTAL: ' + str(total), level=xbmc.LOGDEBUG)
	for i in range(total):
		sport = data['events'][i]['type']
		if name != sport:
			continue
		title = data['events'][i]['mobileTitle']
		event = data['events'][i]['type']
		title = title + ' (' + event + ')'
		m_type = 'video'
		hasVideo = data['events'][i]['hasVideo']
		if hasVideo != True:
			title = title + ' * ' + translation(30002) + ' *'
			m_type = 'audio'
		eventID = data['events'][i]['eventID']
		clientID = data['events'][i]['clientID']
		img_key = (data['events'][i]['customText']).split(' ')[-1].lower()
		if img_key in schools:
			image = os.path.join(artbase,img_key + '.png')
		else:
			image = defaultimage
		jurl = 'https://neo-client.stretchinternet.com/streamservice.portal?clientID=' + str(clientID) + '&userID=-1&broadcastType=vod&method=getStream&eventID=' + str(eventID) + '&streamType=' + str(m_type)
		url = 'plugin://plugin.video.caa?mode=10&url=' + urllib.quote_plus(jurl)
		li = xbmcgui.ListItem(title)
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"Sports"})
		li.setArt({'thumb':image,'fanart':defaultfanart})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#7
def ON_DEMAND():
	current = datetime.utcnow() - td(hours=5)
	for i in range(0,11):
		aday = str(current - td(days=i)).split(' ')[0]
		s = aday.replace('-','')
		title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
		urlday = title.strftime("%m-%d-%Y")
		title = title.strftime("%B %d, %Y")
		title = str(title.replace(' 0', ' '))
		url = 'https://neo-client.stretchinternet.com/portal-ws/getEvents.json?dateFilter=' + urlday +'&clientID=47302&broadcastType=vod&token=&school=&_=%5Bobject+Object%5D'
		addDir(title,url,15, defaultimage)
	xbmcplugin.endOfDirectory(addon_handle)


#10
def VOD_JSON(url):
	xbmc.log('VURL: ' + str(url), level=xbmc.LOGDEBUG)
	response = get_html(url)
	data = json.loads(response)
	u_Reason = data['unauthorizedReason']
	if len(u_Reason) > 1:
		xbmcgui.Dialog().notification(plugin, u_Reason, defaultimage, 10000, False)
		xbmc.log('* UNAUTHORIZED *')
		return
	mountPointServiceUrl = data['mountPointServiceUrl']
	mP = get_html(mountPointServiceUrl)
	streamHDURL = data['streamURL']
	streams = streamHDURL.split('#')
	stream = streams[0] + mP
	xbmc.log('STREAM: ' + str(stream), level=xbmc.LOGDEBUG)
	PLAY(name, stream)


#20
def GET_STREAM(url):
	urls = []
	xbmc.log('URL: ' + str(url), level=xbmc.LOGDEBUG)
	response = get_html(url)
	data = json.loads(response)
	u_Reason = data['unauthorizedReason']
	if len(u_Reason) > 1:
		xbmcgui.Dialog().notification(plugin, u_Reason, defaultimage, 10000, False)
		xbmc.log('* UNAUTHORIZED *')
		return
	loadBalancerUrl = data['loadBalancerUrl']
	lB = loadBalancerUrl.split('/')
	streamHDURL = data['streamURL']
	streams = streamHDURL.split('#')
	parts = streams[-1].split('/')
	stream1 = 'https://d15xyumcalkui.cloudfront.net/' + parts[1] + '/_definst_/' + parts[2] + '/playlist.m3u8'# live=true'
	urls.append(stream1)
	stream2 = streams[0] + lB[2] + streams[2]
	urls.append(stream2)
	xbmc.log('STREAMS: ' + str(urls), level=xbmc.LOGDEBUG)
	stream = TEST_STREAMS(urls)
	PLAY(name, stream)


def TEST_STREAMS(url):
	req = urllib2.Request(url[0])
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0')
	try:response = urllib2.urlopen(req, timeout=10)
	except urllib2.HTTPError:
		xbmc.log('* HTTP Error *')
		stream = url[1]
		return stream
	#except socket.timeout:
		#xbmc.log('TIMEOUT', level=xbmc.LOGDEBUG)
		#stream = url[1]
		#return stream
	except socket.error:
		xbmc.log('* SOCKET ERROR *')
		stream = url[1]
		return stream
	stream = url[0]
	return stream


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log('### SETRESOLVEDURL ###')
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=xbmc.LOGDEBUG)
	xbmcplugin.endOfDirectory(addon_handle)



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


def addDir(name,url,mode,iconimage, fanart=False, infoLabels=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	#ok=True
	liz=xbmcgui.ListItem(name)
	liz.setInfo(type="Video", infoLabels={"mediatype":"video","label":name,"title":name,"genre":"Sports"})
	#liz.setProperty('IsPlayable', 'true')
	#liz.setInfo( type="Video", infoLabels={ "Title": name } )
	if not fanart:
		fanart=defaultfanart
	#liz.setProperty('fanart_image',fanart)
	liz.setArt({'thumb':defaulticon,'fanart':defaultfanart})
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
	VOD_JSON(url)
elif mode == 15:
	xbmc.log("CAA TV Sports")
	GET_SPORTS(name,url)
elif mode == 20:
	xbmc.log("CAA.TV Get Stream")
	GET_STREAM(url)
elif mode == 99:
	xbmc.log("Play Video")
	PLAY(name,url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))