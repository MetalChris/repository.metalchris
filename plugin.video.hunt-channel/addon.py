#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import html5lib
import json
import datetime
from pytz import timezone

artbase = 'special://home/addons/plugin.video.hunt-channel/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.hunt-channel')
self = xbmcaddon.Addon(id='plugin.video.hunt-channel')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Hunt Channel"

defaultimage = 'special://home/addons/plugin.video.hunt-channel/icon.png'
defaultfanart = 'special://home/addons/plugin.video.hunt-channel/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.hunt-channel/icon.png'
baseurl = 'http://www.huntchannel.tv'
schedule = 'special://home/addons/plugin.video.hunt-channel/resources/media/schedule.json'

local_string = xbmcaddon.Addon(id='plugin.video.hunt-channel').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:51.0) Gecko/20100101 Firefox/51.0',
	'Referer': 'http://www.huntchannel.tv/shows/'
}

now = datetime.datetime.now(timezone('US/Eastern'))
now_minus_30 = now + datetime.timedelta(minutes = -30)
if now.hour >12:
	hour = now.hour - 12
elif now.hour < 1:
	hour = '12'
else:
	hour = now.hour
if now.minute < 29:
	minute = '00'
else:
	minute = '30'
showday = now.strftime("%A")
#xbmc.log(str(showday))
today = int(now.strftime("%w"))
if today <1:
	today = 7
#xbmc.log(str(today))
nowstring = str(hour) + ':' + minute + ' ' + now.strftime("%p")
#xbmc.log(str(nowstring))
program = 'No Info Currently Available'


def prog():
	html = get_html('http://www.huntchannel.tv/schedule')
	rows = BeautifulSoup(html,'html5lib').find_all('tr')
	match = 0
	for row in rows[1:45]:
		row_split = (str(row)).split('</td>')
		row_list = striphtml(str(row_split)).replace('\'','').replace('[','').replace(']','').split(',')
		if nowstring == row_list[0]:
			match = 1
			xbmc.log('==========================MATCH')
			program = str(row_list[today]).replace("\\","'")
			#xbmc.log(str(program))
			#xbmc.log(str(row_list))
			break

		elif match <1:
			program = 'No Info Currently Available'
	#xbmc.log(str(match))
	cats(program)


#10
def cats(program):
	addDir2('Live Stream' + ': ' + program,'http://www.huntchannel.tv/',12,defaultimage)
	addDir('On Demand','http://www.huntchannel.tv/shows/',100,defaultimage)
	xbmcplugin.endOfDirectory(addon_handle)


#12
def get_live(name,url,iconimage):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'style':'position: relative; padding-bottom: 10%; overflow: hidden;'})
	xbmc.log('SOUP Length: ' + str(len(soup)))
	i_url = str(re.compile('src="(.+?)"').findall(str(soup)))[2:-2].replace('html','js')
	xbmc.log('IFRAME: ' + str(i_url))
	html = get_html(i_url)
	source = re.compile('source0.src = (.+?);').findall(html)[0]
	m3u8 = str(re.compile("'[^']*'").findall(str(source)))[3:-3]
	xbmc.log('M3U8: ' + str(m3u8))
	listitem = xbmcgui.ListItem('Hunt Channel' + ' ' + name, thumbnailImage=defaulticon)
	listitem.setProperty('mimetype', 'video/x-mpegurl')
	#PLAY(name,m3u8)
	xbmc.Player().play( m3u8, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#21
def sc_videos(name,url):
	html = get_html(url)
	huntjson = re.compile('] = (.+?);\\n').findall(html)[0]
	hdata = json.loads(huntjson)
	total = hdata['total']
	xbmc.log('TOTAL: ' + str(total))
	if total > 25:
		total = 25
	for i in range(total):
		v_id = str(hdata['pages']['default']['1'][i])
		title = unicode(hdata['video_set'][v_id]['name']).encode('utf-8', errors='ignore')
		image = (hdata['video_set'][v_id]['thumbnail_small']).split('?')[0]
		url = 'https://player.vimeo.com/video/' + v_id
		add_directory(title,url,22,defaultfanart,image,plot='')
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#22
def sc_streams(name,url):
	html = get_html(url)
	width = re.compile('"width":(.+?),').findall(html)
	del width[-1]
	width = (map(int, width))
	##xbmc.log('WIDTH: ' + str(width))
	highest = max(width)
	##xbmc.log('HIGHEST: ' + str(highest))
	highest = width.index(max(width))
	##xbmc.log('HIGHEST: ' + str(highest))
	stream_link = re.compile('url":"(.+?)"').findall(html)
	##stream_json = re.compile('var a=(.+?);if').findall(html)[0]
	streams = []
	for stream in stream_link:
		if 'mp4' in stream:
			streams.append(stream)
			xbmc.log('STREAM: ' + str(stream))
	##xbmc.log('STREAMS: ' + str(len(streams)))
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( streams[highest], listitem )
	sys.exit()


#100
def more(url):
	count = 0
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'inner-entry'})
	xbmc.log('SOUP: ' + str(len(soup)))
	for title in soup:
		count = count + 1
		show = title.find('h1').text.encode('utf-8')
		url = title.find('a')['href']
		#image = title.find('img')['src']
		if title.find('img'):
			image = title.find('img')['src']
		else:
			image = defaultimage
		add_directory2(show,url,21,defaultfanart,image,plot='')
	if count > 99:
		next_page = 'http://www.huntchannel.tv/shows/page/2/'
		add_directory2('Next Page',next_page,100,defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log('### SETRESOLVEDURL ###')
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=xbmc.LOGDEBUG)
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(name,url,iconimage):
	xbmc.log(str(url))
	listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def hplay(name,url,iconimage):
	xbmc.log(str(url))
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def add_directory(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)# + "&thumbnail=" + urllib.quote_plus(thumbnail)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=100)
	return ok


def add_directory2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)# + "&thumbnail=" + urllib.quote_plus(thumbnail)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=100)
	return ok

def get_html(url):
	xbmc.log('URL: ' + str(url))
	req = urllib2.Request(url)
	#req.add_header('Host','content.jwplatform.com')
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0')

	try:
		response = urllib2.urlopen(req, timeout=30)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def get_iframe(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'player.vimeo.com')
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0')
	req.add_header('Referer', 'http://huntchannel.tv/')

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
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)# + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name,url,mode,iconimage, fanart=True, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)# + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',defaultfanart)
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
	prog()
elif mode == 4:
	xbmc.log("Play Video")
elif mode==10:
	xbmc.log('Hunt Channel Categories')
	cats(program)
elif mode==12:
	xbmc.log('Hunt Channel Live')
	get_live(name,url,iconimage)
elif mode==21:
	xbmc.log("Hunt Channel Videos")
	sc_videos(name,url)
elif mode==22:
	xbmc.log("Hunt Channel Videos")
	sc_streams(name,url)
elif mode==100:
	xbmc.log("Hunt Channel Shows")
	more(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
