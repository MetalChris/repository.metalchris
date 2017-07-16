#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, xbmcplugin, xbmcaddon, xbmcgui, re, sys
from bs4 import BeautifulSoup
import mechanize
import html5lib
import simplejson as json
#import Cookie
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

plugin = "Smithsonian Earth"

defaultimage = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
defaultfanart = 'special://home/addons/plugin.video.smithsonian-earth/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
baseurl = 'https://api.smithsonianearthtv.com:8443'

addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


#630
def cats():
	#page = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/categories/16617?5DJZN6FN').read()
	page = br.open('https://api.skychnl.net/channels/5DJZN6FN/responsives/categories/48456').read()
	cats = BeautifulSoup(page,'html5lib').find_all('option')
	for title in cats:
		url = baseurl + (title.get('value')).split('?')[0]
		mode = 633
		if len(url) < 50:
			continue
		if '48459' in url:
			url = url.split('categories')[0] + 'get_next_category_page?id=48459&index=0'
			mode = 635
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
			vid_key = title.find('div')['vid']
			url = 'https://api.skychnl.net' + (title.get('href'))# + 'token=' + str(cookie.value)
			title = title.find('h2').text.encode('utf-8').replace('&amp;','&').strip()
			addDir2(title, url, 634, defaultfanart, image, plot='')
	#xbmcplugin.setContent(addon_handle, content="videos")
	xbmcplugin.endOfDirectory(addon_handle)


#634
def series(name,url,iconimage):
	dlsn = settings.getSetting(id="status")
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	#for cookie in cookiejar:
		#print cookie.name, cookie.value, cookie.domain
	br.select_form(nr = 0)
	br['email'] = email
	br['password'] = password
	logged_in = br.submit()
	check = logged_in.read()
	if 'Log In' in check:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 5000, False)
		return
	else:
		if dlsn=='false':
			xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
	page = br.open(url).read()
	for cookie in cookiejar:
		xbmc.log('Cookie Name: ' + str(cookie.name))
		xbmc.log('Cookie Value: ' + str(cookie.value))
		xbmc.log('Cookie Domain: ' + str(cookie.domain))
	url = url.replace('https://api.skychnl.net', baseurl) + '&' + cookie.name + '=' + cookie.value
	xbmc.log('URL: ' + str(url))
	page = br.open(url).read()
	#soup = BeautifulSoup(page,'html5lib').find_all('a')
	scripts = BeautifulSoup(page,'html5lib').find_all('script',{'type':'text/javascript'})
	#for script in scripts:
		#print str(len(str(script)))
	jsob = re.compile('episodesArray      = (.+?);').findall(str(scripts[4]));i=0
	jdata = json.loads(jsob[0])
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
		q = settings.getSetting(id='quality')
		url = 'http://se-media.smithsonianchannel.com/5DJZN6FN/' + key[4] + '/hd/hls/v' + q + '_' + key[4] + '_clear/v' + q + '_' + key[4] + '_clear.m3u8'
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
		li.setProperty('fanart_image', defaultfanart)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Season": season, "Episode": ep, "Premiered": pubdate, "mpaa": rating})
		#li.setProperty('mimetype', 'video/mp4')
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
		xbmcplugin.setContent(addon_handle, 'episodes');i=i+1
	xbmcplugin.endOfDirectory(addon_handle)


#635
def single(url):
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
		purl = 'plugin://plugin.video.smithsonian-earth?mode=636&url=' + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(image)
		pubdate = jdata['page']['category']['videos'][i]['video']['pubdate']
		li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image);i=i+1
		li.setProperty('fanart_image', defaultfanart)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Premiered": pubdate, "mpaa": rating})
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#636
def stream(name,url):
	xbmc.log('URL: ' + str(url))
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	br.select_form(nr = 0)
	br['email'] = email
	br['password'] = password
	logged_in = br.submit()
	check = logged_in.read()
	dlsn = settings.getSetting(id="status")
	if 'Log In' in check:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 5000, False)
		return
	else:
		if dlsn=='false':
			xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
	page = br.open(str(url)).read()
	url = re.compile('html5_url":"(.+?)"').findall(page)
	xbmc.log('M3U8_URL: ' + str(url))
	urls = url[0].rpartition('/')
	keys = urls[-1].rpartition('.')
	q = settings.getSetting(id='quality')
	q_key = 'v' + q +'_' + keys[0]
	post_url = q_key + '/' + q_key + '.m3u8'
	stream = urls[0] + '/' + post_url
	play(name,stream,iconimage)
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
		liz.addContextMenuItems([('Plot Info', 'XBMC.RunPlugin(%s?mode=681&url=%s)' % (sys.argv[0], url))])
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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None:# or url == None or len(url) < 1:
	xbmc.log("Generate Smithsonian Earth Main Menu")
	cats()
elif mode==630:
	xbmc.log("Smithsonian Earth Categories")
	cats()
elif mode==633:
	xbmc.log("Smithsonian Earth Videos")
	videos(url)
elif mode==634:
	xbmc.log("Smithsonian Earth Series")
	series(name,url,iconimage)
elif mode==635:
	xbmc.log("Smithsonian Earth Single")
	single(url)
elif mode==636:
	xbmc.log("Smithsonian Earth Stream")
	stream(name,url)
elif mode==681:
	xbmc.log("Smithsonian Earth Plot Info")
	plot_info(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
