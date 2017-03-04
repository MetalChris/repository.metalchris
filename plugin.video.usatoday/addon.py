#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
import requests
from bs4 import BeautifulSoup
import html5lib
import simplejson as json

artbase = 'special://home/addons/plugin.video.usatoday/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.usatoday')
self = xbmcaddon.Addon(id='plugin.video.usatoday')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "USA Today"

artbase = 'special://home/addons/plugin.video.usatoday/resources/media/'
defaultimage = 'special://home/addons/plugin.video.usatoday/icon.png'
defaultfanart = 'special://home/addons/plugin.video.usatoday/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.usatoday/icon.png'
baseurl = 'http://www.usatoday.com/media/latest/videos/news/'
brightcove = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='

local_string = xbmcaddon.Addon(id='plugin.video.usatoday').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]



def cats():
	html = get_html(baseurl)
	soup = BeautifulSoup(html,'html5lib').find_all('ul',{'class':'site-nav-more-dropdown-list site-nav-more-dropdown-list-1col'})
	#titles  = re.compile('">(.+?)</a>').findall(str(soup))
	links  = re.compile('href="(.+?)"').findall(str(soup))
	for link in links[0:6]:
		title = link.replace('/','').title()
		url = baseurl.replace('/news/', str(link))
		image = artbase + title.lower() + '.jpg'
		add_directory2(title,url,3,defaultfanart,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#3
def sub_cats(name, url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('li',{'class':'sub active media-sidenav-item'})
	titles  = re.compile('">(.+?)</a>').findall(str(soup))
	links  = re.compile('href="(.+?)"').findall(str(soup))
	for title, link in zip(titles, links)[1:]:
		title = striphtml(str(title))
		image = artbase + name.lower() + '.jpg'
		url = ('http://www.usatoday.com' + link).replace('latest', 'latest/videos')
		add_directory2(title,url,6,defaultfanart,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#6
def videos(url):
	html = get_html(url)
	titles  = re.compile('capt">(.+?)</figcaption').findall(str(html))
	images  = re.compile('data-large-src="(.+?)"').findall(str(html))
	for title, image in zip(titles, images):
		title = title.replace("&#39;","'")
		image = 'http://' + (image.split('/http/')[-1])
		key = (image.split('_')[-1]).split('-')[0]
		xbmc.log('KEY: ' + str(key))
		if key.isdigit():
			url = brightcove + key
			add_directory2(title,url,99,image,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


#99
def play(name,url):
	print url
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
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

def get_html(url):
	req = urllib2.Request(url)
	req = urllib2.Request(url)
	req.add_header('Host', 'www.usatoday.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	req.add_header('Referer', baseurl)

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
	print "USA Today Main Menu"
	cats()
elif mode==3:
	print 'USA Today Sub Menu'
	sub_cats(name,url)
elif mode == 4:
	print "Play Video"
elif mode==6:
	print 'USA Today Videos'
	videos(url)
elif mode==99:
	print 'Play USA Today Videos'
	play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
