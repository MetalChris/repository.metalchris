#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
import requests
from bs4 import BeautifulSoup
import html5lib

headers= {'Host':'player.vimeo.com',
'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
'Referer':'https://www.edge.org/videos'}

artbase = 'special://home/addons/plugin.video.edge/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.edge')
self = xbmcaddon.Addon(id='plugin.video.edge')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.edge")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Edge.org"

defaultimage = 'special://home/addons/plugin.video.edge/icon.png'
defaultfanart = 'special://home/addons/plugin.video.edge/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.edge/icon.png'
baseurl = 'https://www.edge.org/videos'

local_string = xbmcaddon.Addon(id='plugin.video.edge').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#10
def cats(url):
	#response = get_html(baseurl)
	response = requests.get(baseurl)
	print response
	xbmc.log('RESPONSE: ' + str(response))
	page = response.content
	soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'views-field views-field-name'})
	for item in soup:
		title = item.find('a').string.encode('utf-8').title()
		url = 'http://www.edge.org' + item.find('a')['href']
		add_directory2(title,url,20,defaultfanart,defaultimage,plot='')
	add_directory2('Browse by Year',url,11,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)

#11
def years(url):
	page = requests.get(url)
	response = page.content
	soup = BeautifulSoup(response,'html5lib').find_all('div',{'id':'block-accordion-blocks-videos-browse-by-year-2'})
	match = re.compile('href="(.+?)">(.+?)</').findall(str(soup))
	for url, year in match:
		url = 'http://www.edge.org' + url
		add_directory2(year,url,20,defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	lasttitle = ''
	page = requests.get(url)
	response = page.content
	soup = BeautifulSoup(response,'html5lib').find_all('h2',{'class':'views-field views-field-title margin-top-zero'}); i = 0
	#members = striphtml(str(members))
	#print members
	for item in soup:
		title = item.find('span',{'class':'field-content'}).string.encode('utf-8')
		if title == lasttitle:
			continue
		#title = striphtml(members[i]) + ': ' + title
		url = 'http://www.edge.org' + item.find('a')['href']
		print 'EDGE URL: ' + str(url)
		lasttitle = title
		add_directory2(title,url,30,defaultfanart,defaultimage,plot=''); i = i + 1
	try:nxt = 'http://www.edge.org' + re.compile('next page" href="(.+?)"').findall(response)[-1]
	except IndexError:
		return
	#print next
	add_directory2('Next Page',nxt,20,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	Q = int(QUALITY)
	print type(Q)
	page = requests.get(url)
	print page
	response = page.content
	soup = BeautifulSoup(response,'html5lib').find_all('iframe')
	print 'len(iframe): ' + str(len(soup))
	if len(soup) > 1:
		multi(name, soup)
		sys.exit()
	url = re.compile('src="(.+?)"').findall(str(soup))[0]
	#print iframe
	iframe(name, url)


#40
def multi(name, soup):
	print name
	titles = re.compile('title="(.+?)"').findall(str(soup))
	iframes = re.compile('src="(.+?)"').findall(str(soup))
	items = zip(titles, iframes)
	for item in items:
		title = item[0]
		iframe = item[1]
		#print title, iframe
		add_directory2(title,iframe,50,defaultfanart,defaultimage,plot='')#; i = i + 1
	xbmcplugin.endOfDirectory(addon_handle)


#50
def iframe(name, url):
	iframe = url
	if iframe.find('?')!=-1:
		iframe = 'https:' + iframe.split('?', 1)[0]
		iframe = iframe.replace('https:https:','https:')
	print 'EDGE iframe: ' + str(iframe)
	if iframe.find('https:')!=0:
		iframe = 'https:' + iframe
	#request = urllib2.Request(iframe)
	#request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0')
	#request.add_header('Referer', url)
	#page = urllib2.urlopen(request).read()
	page = requests.get(iframe, headers=headers)
	response = page.content
	url = re.compile('"url":"(.+?)","origin"').findall(str(response))[-1].replace('json?base64_init=1','m3u8')
	print url
	if url.find(',')!=-1:
		url = url.split(',', 1)[0]
		#print url
		url = url + '/playlist.m3u8?p=6'
	listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
	#play(url)
	xbmc.Player().play( url, listitem )
	sys.exit()
	if 'mp4' in url:
		listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
		listitem.setProperty('IsPlayable', 'true')
		#play(url)
		xbmc.Player().play( url, listitem )
		sys.exit()
		xbmcplugin.endOfDirectory(addon_handle)
	m3u8 = get_html(url)
	base = url.rsplit('/',2)[0]
	streams = re.compile('RESOLUTION=(.+?)\\n(.+?)\\n').findall(m3u8)
	#print streams
	for stream in streams:
		bitrate = (stream[0]).split('x')[0]
		#print bitrate + ' ' + str(stream[1])
		qkey = bitrate + ' ' + str(stream[1])
		if '1280' in bitrate and QUALITY == '1':
		#print 'HD= ' + str(qkey.split('..')[-1])
			url = base + str(qkey.split('..')[-1])
			print url
		if '960' in bitrate and QUALITY == '0':
		#print 'MD= ' + str(qkey.split('..')[-1])
			url = base + str(qkey.split('..')[-1])
			print url
		if '640' in bitrate and QUALITY == '0':
		#print 'SD= ' + str(qkey.split('..')[-1])
			url = base + str(qkey.split('..')[-1])
			print url
	listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
	listitem.setProperty('IsPlayable', 'true')
	#play(url)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	print url
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	item.setProperty('IsFolder', 'false')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), succeeded=True, listitem=item)


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

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host','www.edge.org')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

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
	cats(url)
elif mode == 4:
	print "Play Video"
elif mode==11:
	print "Edge Years"
	years(url)
elif mode==20:
	print "Edge Videos"
	videos(url)
elif mode==30:
	print "Edge Streams"
	streams(name,url)
elif mode==40:
	print "Edge Multi Streams"
	multi(name,soup)
elif mode==50:
	print "Edge Iframe"
	iframe(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
