#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests
import urlparse
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
import html5lib


addon = xbmcaddon.Addon('plugin.audio.internet-radio')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
artbase = 'special://home/addons/plugin.audio.internet-radio/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.audio.internet-radio')
self = xbmcaddon.Addon(id='plugin.audio.internet-radio')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.audio.internet-radio")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]
favorites = os.path.join(profile, 'favorites')
if os.path.exists(favorites)==True:
	FAV = open(favorites).read()
else: FAV = []

plugin = "Internet Radio"

defaultimage = 'special://home/addons/plugin.audio.internet-radio/icon.png'
defaultfanart = 'special://home/addons/plugin.audio.internet-radio/fanart.jpg'
defaulticon = 'special://home/addons/plugin.audio.internet-radio/icon.png'
baseurl = 'http://www.internet-radio.com'

local_string = xbmcaddon.Addon(id='plugin.audio.internet-radio').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,511,512,513,515]


#20
def genres():
	add_directory2('Search',baseurl,50,defaultfanart,defaultimage,plot='')
	if os.path.exists(favorites) == True:
		addDir('Favorites','url',4,os.path.join(home, 'resources', defaultimage),defaultfanart,'','','','')
	response = get_html(baseurl)
	soup = BeautifulSoup(response,'html5lib').find_all('a',{'style':'margin: 4px;'})
	for item in soup:
		title = (re.compile('>(.+?)</a').findall(str(item))[-1]).title().replace('0S','0\'s')
		url = baseurl + str(re.compile('href="(.+?)"').findall(str(item))[-1])
		add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#30
def stations(name,url):
	print url
	page = get_html(url)
	#response = br.open(url)
	#page = response.get_data()
	try: next = baseurl + str(re.compile('next"><a href="(.+?)"').findall(page)[-1])
	except IndexError:
		next = ''
		pass
	soup = BeautifulSoup(page,'html5lib').find_all('small',{'class':'hidden-xs'})
	#print soup[1]
	#stations = [tuple(soup[i:i+3]) for i in range(0, len(soup), 3)]
	#print stations[0]
	print len(soup)
	for station in soup:
		try: title = (re.compile('title=(.+?)&').findall(str(station))[-1]).split(' - ')[0]
		except IndexError:
			continue
		#try: track = re.compile('b>(.+?)</b').findall(str(track))[-1]
		#except IndexError:
			#continue
		#title = title + ' - ' + track
		mount = baseurl + str(re.compile('open\\(\'(.+?)\',').findall(str(station))[-1]).split('&')[0]
		add_directory(title,mount,40,defaultfanart,defaultimage,plot='')
	if len(next) > 1:
		add_directory2('Next Page',next,30,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#40
def streams(name,url):
	print url
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	r = requests.get(url, headers=headers)
	print r.status_code
	html = get_html(url)
	try: url = re.compile('mp3: "(.+?)"').findall(str(html))[-1]
	except IndexError:
		url = re.compile('m4a: "(.+?)"').findall(str(html))[-1]
	thumbnail = defaultimage
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)

#50
def search():
		keyb = xbmc.Keyboard('', 'Search')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText().replace(' ','+')
			print 'search= ' + search
		url = baseurl + '/search/?radio=' + search
		stations(name,url)

def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host','www.internet-radio.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError as (e):
		print (e)
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


def add_directory(name,url,mode,fanart,thumbnail,plot,showcontext=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
		return ok


def add_directory2(name,url,mode,fanart,thumbnail,plot,showcontext=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok


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
		genres()
elif mode == 4:
		print "Play Video"
elif mode==20:
		print "Internet Radio"
		genres()
elif mode==30:
		print "Stations"
		stations(name,url)
elif mode==40:
		print "Internet Radio Streams"
		streams(name,url)
elif mode==50:
		print "Internet Radio Search"
		search()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
