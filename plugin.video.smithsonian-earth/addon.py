#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, xbmcplugin, xbmcaddon, xbmcgui, re, sys
from bs4 import BeautifulSoup
import mechanize
import html5lib
import json
import cookielib
cookiejar = cookielib.LWPCookieJar()

br = mechanize.Browser()
br.set_cookiejar(cookiejar)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')]

artbase = 'special://home/addons/plugin.video.smithsonian-earth/resources/media/'
selfAddon = xbmcaddon.Addon(id='plugin.video.smithsonian-earth')
translation = selfAddon.getLocalizedString
local_string = xbmcaddon.Addon(id='plugin.video.smithsonian-earth').getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.smithsonian-earth")
email = settings.getSetting(id="username")
password = settings.getSetting(id="password")
addon = xbmcaddon.Addon(id="plugin.video.smithsonian-earth")
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,503,504,515]
force_views = settings.getSetting(id="force_views")

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

plugin = "Smithsonian Earth"

defaultimage = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
defaultfanart = 'special://home/addons/plugin.video.smithsonian-earth/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
baseurl = 'https://api.smithsonianearthtv.com:8443'

addon_handle = int(sys.argv[1])


#630
def cats():
	page = br.open('https://api.skychnl.net/channels/5DJZN6FN/responsives/categories/48456').read()
	cats = BeautifulSoup(page,'html5lib').find_all('option')
	for title in cats:
		url = baseurl + (title.get('value')).split('?')[0]
		mode = 633
		if len(url) < 50:
			continue
		if '48459' in url:
			url = url.split('categories')[0] + 'get_next_category_page?id=48459&index=0'
			mode = 636
		title = title.text
		addDir(title, url, mode, defaulticon, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle)


#633
def videos(url):
	page = br.open(url).read()
	soup = BeautifulSoup(page,'html5lib').find_all('a')
	for title in soup:
		if title.find(class_="video-thumb"):
			image = 'http:' + (re.compile('image:url\\((.+?)\\)').findall(str(title)))[0]#.replace('.jpg','.background.atv4.jpg')
			url = 'https://api.skychnl.net' + (title.get('href'))# + 'token=' + str(cookie.value)
			title = title.find('h2').text.encode('utf-8').replace('&amp;','&').strip()
			#xbmc.log('TITLE: ' +str(title), level=log_level)
			addDir2(title, url, 634, defaultfanart, image, plot='')
	#xbmcplugin.setContent(addon_handle, content="videos")
	xbmcplugin.endOfDirectory(addon_handle)


#634
def series(name,url,iconimage):
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	#for cookie in cookiejar:
		#print cookie.name, cookie.value, cookie.domain
	br.select_form(nr = 0)
	br['email'] = email
	br['password'] = password
	logged_in = br.submit()
	check = logged_in.read()
	device_id = re.compile(" device_id = '(.+?)'").findall(str(check))
	xbmc.log('DEVICE_ID: ' + str(device_id),level=log_level)
	dlsn = settings.getSetting(id="status")
	if email in check:
		if dlsn=='false':
			xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
	else:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 50000, False)
		return
	page = br.open(url).read()
	for cookie in cookiejar:
		xbmc.log('Cookie Name: ' + str(cookie.name), level=log_level)
		xbmc.log('Cookie Value: ' + str(cookie.value), level=log_level)
		xbmc.log('Cookie Domain: ' + str(cookie.domain), level=log_level)
	url = url.replace('https://api.skychnl.net', baseurl) + '&' + cookie.name + '=' + cookie.value
	xbmc.log('URL: ' + str(url), level=log_level)
	page = br.open(url).read()
	scripts = BeautifulSoup(page,'html5lib').find_all('script',{'type':'text/javascript'});i=0
	for script in scripts:
		i = i + 1
		if 'episodesArray' in str(script):
			xbmc.log('### SEASON ###', level=log_level)
			count = int(i - 1)
			xbmc.log('COUNT: ' + str(i), level=log_level)
			if len(str(scripts[count])) > 5000:
				jsob = re.compile('episodesArray      = (.+?);').findall(str(scripts[count]))
			else:
				xbmc.log('### SINGLE ###', level=log_level)
				count = int(i - 1)
				xbmc.log('COUNT: ' + str(i), level=log_level)
				jsob = re.compile('new SCVideo\((.+?)\)').findall(str(scripts[count]))
				image = BeautifulSoup(page,'html5lib').find('div',{'class':'thumb'})
				iconimage = 'https:' + image.find('img')['src']
				single(jsob,iconimage)
				return
	jdata = json.loads(jsob[0]);i=0
	for title in jdata:
		title = jdata[i]['title']
		image = jdata[i]['thumbnail']#.replace('.jpg','.spot.16_9.jpg')
		description = jdata[i]['description']
		duration = jdata[i]['duration']
		rating = jdata[i]['rating']
		ep = jdata[i]['episode_number']
		season = jdata[i]['season_number']
		pubdate = jdata[i]['pubdate']
		m3u8_url = jdata[i]['vtt'][0]['m3u8_url']
		#subs_url = jdata[i]['vtt'][0]['url']
		key = m3u8_url.split('/')
		url = 'https://se-media.smithsonianchannel.com/5DJZN6FN/' + key[4] + '/hd/hls/' + key[4] + '_clear.m3u8'
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
		#li.setSubtitles(subs_url)
		li.setProperty('fanart_image', defaultfanart)
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Season": season, "Episode": ep, "Premiered": pubdate, "mpaa": rating})
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10, isFolder=False)
		xbmcplugin.setContent(addon_handle, 'episodes');i=i+1
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#635
def single(jsob,iconimage):
	jdata = json.loads(jsob[0])#;i=0
	for title in jdata:
		title = jdata['title']
		description = jdata['description']
		duration = jdata['duration']
		rating = jdata['rating']
		pubdate = jdata['pubdate']
		url = jdata['html5_url']
		play(title,url,iconimage)


#636
def nature(url):
	page = br.open(url).read()
	jdata = json.loads(page);i=0
	for title in jdata['page']['category']['videos']:
		title = jdata['page']['category']['videos'][i]['video']['title']
		image = jdata['page']['category']['videos'][i]['video']['thumbnail']#.replace('.jpg','.spot.16_9.jpg')
		description = jdata['page']['category']['videos'][i]['video']['description']
		duration = jdata['page']['category']['videos'][i]['video']['duration']
		rating = jdata['page']['category']['videos'][i]['video']['rating']
		video_id = jdata['page']['category']['videos'][i]['video']['id']
		url = 'https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/' + str(video_id) + '?index=0&locale=en'
		purl = 'plugin://plugin.video.smithsonian-earth?mode=637&url=' + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(image)
		pubdate = jdata['page']['category']['videos'][i]['video']['pubdate']
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image);i=i+1
		li.setProperty('fanart_image', defaultfanart)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Premiered": pubdate, "mpaa": rating})
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#637
def stream(name,url):
	xbmc.log('URL: ' + str(url))
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	br.select_form(nr = 0)
	br['email'] = email
	br['password'] = password
	logged_in = br.submit()
	check = logged_in.read()
	device_id = re.compile(" device_id = '(.+?)'").findall(str(check))
	xbmc.log('DEVICE_ID: ' + str(device_id),level=log_level)
	dlsn = settings.getSetting(id="status")
	if email in check:
		if dlsn=='false':
			xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
	else:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 50000, False)
		return
	page = br.open(str(url)).read()
	url = re.compile('html5_url":"(.+?)"').findall(page)[0]
	xbmc.log('M3U8_URL: ' + str(url),level=log_level)
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


#99
def PLAY(url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log('### SETRESOLVEDURL ###', level=log_level)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=log_level)
	xbmcplugin.endOfDirectory(addon_handle)


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


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


def addDir2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		#commands = []
		#commands.append ----- THIS WORKS! -----
		#liz.addContextMenuItems([('Description', 'XBMC.RunScript(special://home/addons/plugin.video.smithsonian-earth/plot.py)')])
		#liz.addContextMenuItems([('Description', 'XBMC.RunPlugin(%s?mode=681&url=%s)' % (sys.argv[0], url))])
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=70)
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
	plot = urllib.unquote_plus(params["plot"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

xbmc.log("Mode: " + str(mode), level=log_level)
xbmc.log("URL: " + str(url), level=log_level)
xbmc.log("Name: " + str(name), level=log_level)

if mode == None:# or url == None or len(url) < 1:
	xbmc.log(("Generate Smithsonian Earth Main Menu"), level=log_level)
	cats()
elif mode==630:
	xbmc.log(("Smithsonian Earth Categories"), level=log_level)
	cats()
elif mode==633:
	xbmc.log(("Smithsonian Earth Videos"), level=log_level)
	videos(url)
elif mode==634:
	xbmc.log(("Smithsonian Earth Series"), level=log_level)
	series(name,url,iconimage)
elif mode==635:
	xbmc.log(("Smithsonian Earth Single"), level=log_level)
	single(url)
elif mode==636:
	xbmc.log(("Smithsonian Nature Scenes"), level=log_level)
	nature(url)
elif mode==637:
	xbmc.log(("Smithsonian Nature Scenes Stream"), level=log_level)
	stream(name,url)
elif mode==681:
	xbmc.log(("Smithsonian Earth Plot Info"), level=log_level)
	plot_info(url)
elif mode==99:
	xbmc.log(("Play Smithsonian Earth Video"), level=log_level)
	PLAY(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
