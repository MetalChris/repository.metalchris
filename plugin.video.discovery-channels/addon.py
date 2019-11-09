#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

#11092019

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, platform, re, sys, os
import requests
import json
import mechanize
import cookielib

artbase = 'special://home/addons/plugin.video.discovery-channels/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.discovery-channels')
translation = selfAddon.getLocalizedString
settings = xbmcaddon.Addon(id="plugin.video.discovery-channels")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
__resource__   = xbmc.translatePath( os.path.join( _addon_path, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

from uas import *

CookieJar = cookielib.LWPCookieJar(os.path.join(addon_path_profile, 'cookies.lwp'))
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', ua)]

plugin = "Discovery Channels"

defaultimage = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaulticon = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaultfanart = 'special://home/addons/plugin.video.discovery-channels/fanart.jpg'

local_string = xbmcaddon.Addon(id='plugin.video.discovery-channels').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,503,504,515]
force_views = settings.getSetting(id="force_views")

first = settings.getSetting(id='first')
if first != 'true':
	addon.openSettings(label="Channels")
	addon.setSetting(id='first',value='true')

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

def channels():
	xbmc.log(str(platform.system()),level=log_level)
	xbmc.log(str(platform.release()),level=log_level)
	dsc = settings.getSetting(id="dsc")
	if dsc!='false':
		addDir2('Discovery Channel', 'https://go.discovery.com', 25, artbase + 'discovery.png')
	ap = settings.getSetting(id="ap")
	if ap!='false':
		addDir2('Animal Planet', 'https://www.animalplanet.com', 25, artbase + 'animalplanet.jpg')
	sci = settings.getSetting(id="sci")
	if sci!='false':
		addDir2('Discovery Science', 'https://www.sciencechannel.com', 25, artbase + 'sciencechannel.png')
	idsc = settings.getSetting(id="idsc")
	if idsc!='false':
		addDir2('Investigation Discovery', 'https://www.investigationdiscovery.com', 25, artbase + 'investigationdiscovery.jpg')
	dahn = settings.getSetting(id="dahn")
	if dahn!='false':
		addDir2('American Heroes', 'https://www.ahctv.com/', 25, artbase + 'ahctv.jpg')
	motor = settings.getSetting(id="motor")
	#if motor!='false':
		#addDir2('Motor Trend', 'https://watch.motortrend.com', 25, artbase + 'motortrend.png')
	diy = settings.getSetting(id="diy")
	if diy!='false':
		addDir2('DIY Network', 'https://watch.diynetwork.com/', 30, artbase + 'diynetwork.png')
	dest = settings.getSetting(id="dest")
	if dest!='false':
		addDir2('Destination America', 'https://www.destinationamerica.com/', 25, artbase + 'destinationamerica.jpg')
	dscl = settings.getSetting(id="dscl")
	if dscl!='false':
		addDir2('Discovery Life', 'https://www.discoverylife.com', 25, artbase + 'discoverylife.jpg')
	hgtv = settings.getSetting(id="hgtv")
	if hgtv!='false':
		addDir2('HGTV', 'https://watch.hgtv.com/', 30, artbase + 'hgtv.png')
	food = settings.getSetting(id="food")
	if food!='false':
		addDir2('Food Network', 'https://watch.foodnetwork.com/', 30, artbase + 'foodnetwork.png')
	trvl = settings.getSetting(id="trvl")
	if trvl!='false':
		addDir2('Travel Channel', 'https://watch.travelchannel.com/', 30, artbase + 'travelchannel.png')
	cook = settings.getSetting(id="cook")
	if cook!='false':
		addDir2('Cooking Channel', 'https://watch.cookingchanneltv.com/', 30, artbase + 'cookingchanneltv.png')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#25
def dsc_menu_new(url):
	site = 'https://www.' + (iconimage.rsplit('/', 1)[-1]).split('.')[0] + '.com'
	if ('motortrend' in site) or ('diy' in site) or ('hgtv' in site) or ('food' in site) or ('travel' in site) or ('cook' in site):
		site = site.replace('www','watch')
	xbmc.log('SITE: ' + str(site),level=log_level)
	br.set_handle_robots( False )
	br.set_cookiejar(CookieJar)
	response = br.open(url)
	for cookie in CookieJar:
		#xbmc.log('COOKIE: ' + str(cookie),level=log_level)
		CookieJar.set_cookie(cookie)
	CookieJar.save(ignore_discard=True)
	page = response.get_data()
	#dscjson = re.compile('window.__reactTransmitPacket = (.+?);</script>').findall(page)[0]
	dscjson = re.compile('type="application/json">(.+?)</script>').findall(page)[0]
	xbmc.log('DSCJSON: ' + str(len(dscjson)),level=log_level)
	data = json.loads(dscjson)
	total = len(data['layout']['contentBlocks']);i=0
	xbmc.log('CONTENTBLOCKS: ' + str(total),level=log_level)
	xbmc.log('DSCJSON: ' + str(len(dscjson)),level=log_level)
	for contentBlock in range(total):
		if 'unlocked' in (data['layout']['contentBlocks'][i]['contentLocationTag']):
			xbmc.log('UNLOCKED: ' + str(i),level=log_level)
			value = i
		else:
			i=i+1
	total = len(data['layout']['contentBlocks'][value]['content']['items']);i=0
	xbmc.log('EPISODES: ' + str(total),level=log_level)
	for title in range(total):
		title = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['name'])
		title = unicode(title).encode('utf-8')
		show = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['show']['slug'])
		slug = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['slug'])
		show_name = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['show']['name'])
		url = site + '/tv-shows/' + show + '/full-episodes/' + slug
		image = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['image']['links'][0]['href']).replace('{width}','700')#.replace('{height}','260')
		#test_link(image)
		description = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['description']['standard'])
		runtime = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['duration'])
		duration = GetInHMS(runtime)
		plot = '[I]' + show_name + ':  [/I]' + description
		add_directory3(title, url, 50, artbase + 'fanart2.jpg', image, site, plot=plot + ' (' + duration.replace('00:','') + ') ')# + expiry)
		xbmcplugin.setContent(addon_handle, 'episodes')
		i = i + 1
	#if not 'tlc.com' in site:
		#addDir('Find More Episodes From ' + name, url, 80, iconimage, artbase + 'fanart2.jpg')
		#addDir(name +' Video Clips Sorted by Show', site, 533, iconimage, artbase + 'fanart2.jpg')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)

#30
def diy_menu_new(url):
	site = 'https://www.' + (iconimage.rsplit('/', 1)[-1]).split('.')[0] + '.com'
	if ('motortrend' in site) or ('diy' in site) or ('hgtv' in site) or ('food' in site) or ('travel' in site) or ('cook' in site):
		site = site.replace('www','watch')
	xbmc.log('SITE: ' + str(site),level=log_level)
	br.set_handle_robots( False )
	br.set_cookiejar(CookieJar)
	response = br.open(url)
	for cookie in CookieJar:
		#xbmc.log('COOKIE: ' + str(cookie),level=log_level)
		CookieJar.set_cookie(cookie)
	CookieJar.save(ignore_discard=True)
	page = response.get_data()
	dscjson = re.compile('type="application/json">(.+?)</script>').findall(page)[0]
	xbmc.log('DSCJSON: ' + str(len(dscjson)),level=log_level)
	data = json.loads(dscjson)
	total = len(data['layout']['contentBlocks']);i=0
	xbmc.log('CONTENTBLOCKS: ' + str(total),level=log_level)
	xbmc.log('DSCJSON: ' + str(len(dscjson)),level=log_level)
	for contentBlock in range(total):
		if 'Stream for Free' in (data['layout']['contentBlocks'][i]['label']['line1']) or 'Free Episodes' in (data['layout']['contentBlocks'][i]['label']['line1']):
			xbmc.log('UNLOCKED: ' + str(i),level=log_level)
			value = i
		else:
			i=i+1
	total = len(data['layout']['contentBlocks'][value]['content']['items']);i=0
	xbmc.log('EPISODES: ' + str(total),level=log_level)
	for title in range(total):
		title = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['name'])
		title = unicode(title).encode('utf-8')
		show = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['show']['slug'])
		slug = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['slug'])
		show_name = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['show']['name'])
		url = site + '/tv-shows/' + show + '/full-episodes/' + slug
		image = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['image']['links'][0]['href']).replace('{width}','700')#.replace('{height}','260')
		#test_link(image)
		description = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['description']['standard'])
		runtime = (data['layout']['contentBlocks'][value]['content']['items'][i]['item']['duration'])
		duration = GetInHMS(runtime)
		plot = '[I]' + show_name + ':  [/I]' + description
		add_directory3(title, url, 50, artbase + 'fanart2.jpg', image, site, plot=plot + ' (' + duration.replace('00:','') + ') ')# + expiry)
		xbmcplugin.setContent(addon_handle, 'episodes')
		i = i + 1
	#if not 'tlc.com' in site:
		#addDir('Find More Episodes From ' + name, url, 80, iconimage, artbase + 'fanart2.jpg')
		#addDir(name +' Video Clips Sorted by Show', site, 533, iconimage, artbase + 'fanart2.jpg')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#50
def get_clips_new(name,url,site):
	for cookie in CookieJar:
		xbmc.log('COOKIE LENGTH: ' + str(len(str(cookie))),level=log_level)
		#CookieJar.set_cookie(cookie)
		##if cookie.name == "eosAn":# and not cookie.is_expired():
			##auth = 'Bearer ' +  re.compile('%2522%253A%2522(.+?)%2522%252C%2522').findall(str(cookie.value))[0]
			##xbmc.log('AUTH: ' + str(auth),level=log_level)
	#site = url.split('/')[2]
	xbmc.log('SITE: ' + str(site),level=log_level)
	br.set_handle_robots( False )
	br.addheaders = [('Host', 'api.discovery.com')]
	br.addheaders = [('User-Agent', ua)]
	br.addheaders = [('Referer', site)]
	#br.addheaders = [('authorization', auth)]
	br.set_cookiejar(CookieJar)
	response = br.open(url)
	request = br.request
	xbmc.log('HEADERS: ' + str(request.header_items()),level=log_level)
	for cookie in CookieJar:
		xbmc.log('COOKIE LENGTH: ' + str(len(str(cookie))),level=log_level)
		#if len(str(cookie)) < 500:
			#xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
			#xbmc.log('NO COOKIE NO STREAM',level=log_level)
			#sys.exit()
		CookieJar.set_cookie(cookie)
		if cookie.name == "eosAn":# and not cookie.is_expired():
			auth = 'Bearer ' +  re.compile('%2522%253A%2522(.+?)%2522%252C%2522').findall(str(cookie.value))[0]
			#xbmc.log('AUTH: ' + str(auth),level=log_level)
			browser = mechanize.Browser()
			browser.addheaders = [('Host', 'api.discovery.com')]
			browser.addheaders = [('User-Agent', ua)]
			browser.addheaders = [('Referer', url)]
			browser.addheaders = [('Authorization', auth)]
			browser.set_handle_robots( False )
			#CookieJar.save(ignore_discard=True)
			response = browser.open(url)
			request = browser.request
			xbmc.log('HEADERS: ' + str(request.header_items()),level=log_level)
			page = response.get_data()
			video_id = re.compile('platform=desktop&video_id=(.+?)&networks').findall(str(page))[0]
			xbmc.log('VIDEO_ID: ' + str(video_id),level=log_level)
			video_url = 'http://api.discovery.com/v1/streaming/video/' + video_id + '?platform=desktop'
			xbmc.log('VIDEO_URL: ' + str(video_url),level=log_level)
			#test_link(video_url)
			try:response = browser.open(video_url)
			except mechanize.HTTPError as e:
				xbmc.log('ERROR: ' + str(e.code),level=log_level)
				if e.code != '200':
					xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
					xbmc.log('403 - CURRENTLY UNAVAILABLE',level=log_level)
				sys.exit()
			xbmc.log('RESPONSE: ' + str(response.code),level=log_level)
			try:jsob = json.load(response)
			except ValueError:
				xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
				xbmc.log('JSON CURRENTLY UNAVAILABLE',level=log_level)
				sys.exit()
			stream = jsob['streamUrl']
			xbmc.log('STREAM: ' + str(stream),level=log_level)
			play_episode(stream)
	xbmcplugin.endOfDirectory(addon_handle)


def test_link(url):
	request = requests.head(url)
	if request.status_code == 200:
		xbmc.log('CODE: ' + str(request.status_code),level=log_level)
		xbmc.log('TEXT: ' + str(request.text),level=log_level)
		xbmc.log('HEADERS: ' + str(request.headers),level=log_level)
		xbmc.log('Link Works',level=log_level)
		xbmc.log('IMAGE: ' + str(url),level=log_level)
		return url
	else:
		xbmc.log('Link Broken',level=log_level)
		xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
		xbmc.log('LINK CURRENTLY UNAVAILABLE',level=log_level)
		sys.exit()


#550
def get_clips(name,url):
	r = requests.get(url)
	video_id = re.compile('platform=desktop&video_id=(.+?)&networks').findall(str(r.content))[0]
	xbmc.log('VIDEO_ID: ' + str(video_id),level=log_level)
	video_url = 'http://api.discovery.com/v1/streaming/video/' + video_id + '?platform=desktop'
	opener = urllib2.build_opener()
	xbmc.log('COOKIES LENGTH: ' + str(len(r.cookies)),level=log_level)
	if len(str(r.cookies)) < 1:
		xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
		xbmc.log('CURRENTLY UNAVAILABLE',level=log_level)
		return
	auth = 'Bearer ' + re.compile('%2522%253A%2522(.+?)%2522%252C%2522').findall(str(r.cookies))[0]
	opener.addheaders.append(('Host', 'api.discovery.com'))
	opener.addheaders.append(('User-Agent', ua))
	opener.addheaders.append(('Referer', url))
	opener.addheaders.append(('Authorization', auth))
	f = opener.open(video_url)
	page = f.read()
	jsob = json.loads(page)
	stream = jsob['streamUrl']
	xbmc.log('STREAM: ' + str(stream),level=log_level)
	PLAY(name,stream)
	xbmcplugin.endOfDirectory(addon_handle)


def GetInHMS(seconds):
	hours = seconds / 3600
	seconds -= 3600*hours
	minutes = seconds / 60
	seconds -= 60*minutes
	ti = "%02d:%02d:%02d" % (hours, minutes, seconds)
	ti = str(ti)
	return ti


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


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	listitem.setInfo(type="Video", infoLabels={"Title": name})
	listitem.setProperty('IsPlayable', 'true')
	#xbmc.Player().play( url + '&m3u8=yes', listitem )
	xbmc.Player().play( url, listitem )
	while xbmc.Player().isPlaying():
		continue
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#999
def play(url):
	xbmc.log('URL: ' + str(url),level=log_level)
	#item = xbmcgui.ListItem(path=url + '&m3u8=yes')
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


#999
def play_episode(url):
	xbmc.log('URL: ' + str(url),level=log_level)
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
	return ok


def add_directory3(name,url,mode,fanart,thumbnail,site,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&site="+urllib.quote_plus(site)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	liz.setProperty('IsPlayable', 'true')
	#commands = []
	#commands.append ----- THIS WORKS! -----
	#liz.addContextMenuItems([('Find More Like This', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url))])
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
	return ok


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

def addDir(name, url, mode, iconimage, fanart=True, infoLabels=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image', artbase + 'fanart2.jpg')
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image', artbase + 'fanart5.jpg')
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
site = None

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
try:
	site = urllib.unquote_plus(params["site"])
except:
	pass

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("Discovery Channels",level=log_level)
	channels()
elif mode==80:
	xbmc.log("Find More",level=log_level)
	find_more(url)
elif mode==25:
	xbmc.log("DSC Menu",level=log_level)
	dsc_menu_new(url)
elif mode==30:
	xbmc.log("DIY Menu",level=log_level)
	diy_menu_new(url)
elif mode==31:
	xbmc.log("Discovery Shows",level=log_level)
	discovery_shows_new(name,url)
elif mode==50:
	xbmc.log("Discovery Episodes",level=log_level)
	get_clips_new(name,url,site)
elif mode == 99:
	xbmc.log("PLAY Video",level=log_level)
	PLAY(name,url)
elif mode==998:
	xbmc.log("Get JSON",level=log_level)
	dsc_json(name,url)
elif mode==999:
	xbmc.log("Play Video",level=log_level)
	play(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
