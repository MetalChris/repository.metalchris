#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys
from bs4 import BeautifulSoup
import simplejson as json
import mechanize
import html5lib

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')]

artbase = 'special://home/addons/plugin.video.smithsonian-earth/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.smithsonian-earth')
self = xbmcaddon.Addon(id='plugin.video.smithsonian-earth')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.smithsonian-earth")
email = settings.getSetting(id="username")
password = settings.getSetting(id="password")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

plugin = "Smithsonian Earth"

defaultimage = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
defaultfanart = 'special://home/addons/plugin.video.smithsonian-earth/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.smithsonian-earth/icon.png'
baseurl = 'https://api.smithsonianearthtv.com:8443'
next_pre = 'http://www.space.com/news/'

local_string = xbmcaddon.Addon(id='plugin.video.smithsonian-earth').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


def login():
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	br.select_form(nr = 0)
	br['email'] = 'slingtv@the-antinet.net'
	br['password'] = '1drowssap2017'
	logged_in = br.submit()
	check = logged_in.read()
	soup = BeautifulSoup(check,'html5lib').find_all('title')
	xbmc.log('CHECK: ' + str(soup))
	if 'Log In' in check:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 5000, False)
		return
	else:
		xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 5000, False)
		cats()


#630
def cats():
	page = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/categories/16617?5DJZN6FN').read()
	cats = BeautifulSoup(page,'html5lib').find_all('option')
	xbmc.log('CATS: ' + str(len(cats)))
	xbmc.log('CAT0: ' + str(cats[0]))
	for title in cats:
		url = baseurl + (title.get('value')).split('?')[0]
		if len(url) < 50:
			continue
		title = title.text
		addDir(title, url, 633, defaulticon, defaultfanart)
	xbmcplugin.endOfDirectory(addon_handle)


#633
def videos(url):
	page = br.open(url).read()
	soup = BeautifulSoup(page,'html5lib').find_all('a')
	xbmc.log('SOUP: ' + str(len(soup)))
	xbmc.log('SOUP: ' + str(soup[0]))
	for title in soup:
		if title.find(class_="video-thumb"):
			image = 'http:' + (re.compile('image:url\\((.+?)\\)').findall(str(title)))[0]
			url = baseurl + (title.get('href'))
			title = title.find('h2').text.encode('utf-8').replace('&amp;','&').strip()
			addDir2(title, url, 636, image, defaultfanart)
	xbmcplugin.setContent(addon_handle, content="videos")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def stream(name,url,iconimage):
	sign_in = br.open('https://api.smithsonianearthtv.com:8443/channels/5DJZN6FN/responsives/login')
	br.select_form(nr = 0)
	br['email'] = email
	br['password'] = password
	logged_in = br.submit()
	check = logged_in.read()
	soup = BeautifulSoup(check,'html5lib').find_all('title')
	xbmc.log('CHECK: ' + str(soup))
	if 'Log In' in check:
		xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 5000, False)
		return
	else:
		xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
	page = br.open(url).read()
	xbmc.log('LAST URL: ' + str(br.geturl()))
	soup = BeautifulSoup(page,'html5lib').find_all('script',{'type':'text/javascript'})
	xbmc.log('SOUP: ' + str(len(soup)))
	url = re.compile('html5_url":"(.+?)"').findall(page)[0]
	xbmc.log('URL: ' + str(url))
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


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'player.ooyala.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	#req.add_header('Referer', 'http://www.space.com/news?type=video')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

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


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=True):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok


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

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Smithsonian Earth Main Menu")
	cats()
elif mode==630:
	xbmc.log("Smithsonian Earth Categories")
	cats()
elif mode==633:
	xbmc.log("Smithsonian Earth Videos")
	videos(url)
elif mode==636:
	xbmc.log("Smithsonian Earth Stream")
	stream(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
