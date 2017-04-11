#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys
import simplejson as json
#import base64
## a.decode('base64') ##


artbase = 'special://home/addons/plugin.video.bigcatrescue/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.bigcatrescue')
self = xbmcaddon.Addon(id='plugin.video.bigcatrescue')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.bigcatrescue")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Big Cat Rescue"

defaultimage = 'special://home/addons/plugin.video.bigcatrescue/icon.png'
defaultfanart = 'special://home/addons/plugin.video.bigcatrescue/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.bigcatrescue/icon.png'
baseurl = 'http://vimeo.com'
duration = ''

local_string = xbmcaddon.Addon(id='plugin.video.bigcatrescue').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])

def index():
	url = 'https://vimeo.com/search/sort:latest?q=Big+Cat+Rescue&page=1'
	bcr_videos(url)


#635
def bcr_videos(url):
	response = get_html(url); i = 0
	page = int(str(url)[-1])
	xbmc.log('PAGE: ' + str(page))
	json_data = re.compile('\\"data\\":(.+?),\\"search_id\\"').findall(str(response))[-1]
	jdata = json.loads(json_data)
	for item in jdata:
		title = (jdata[i]['clip']['name']).encode('utf-8')
		#url = 'https://player.vimeo.com/video/' + (jdata[i]['clip']['link']).split('/')[-1]
		url = 'https://vimeo.com/' + (jdata[i]['clip']['link']).split('/')[-1]
		image = (jdata[i]['clip']['pictures']['sizes'][0]['link'])#[:-6]
		duration = (jdata[i]['clip']['duration'])
		description = ''
		add_directory2(title,url,638,image,image,plot=description); i = i + 1
		xbmcplugin.setContent(pluginhandle, 'episodes')
		#views = settings.getSetting(id="views")
		#if views != 'false':
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	print duration
	page = page + 1;next_page = baseurl + '/search/sort:latest?q=Big+Cat+Rescue&page=' + str(page)
	add_directory('Next Page',next_page,635,defaultfanart,defaultimage,plot=description)
	xbmcplugin.endOfDirectory(addon_handle)

#638
def streams(url):
	html = get_html(url)
	url = re.compile('"GET","(.+?)"').findall(str(html))[-1]
	jresponse = urllib2.urlopen(url)
	jdata = json.load(jresponse)
	stream = (jdata['request']['files']['progressive'][0]['url'])
	play(stream)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def remove_non_ascii_1(text):
	return ''.join(i for i in text if ord(i)<128)


def add_directory(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	liz.addStreamInfo('video', { 'duration': (duration) })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
	return ok


def add_directory2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
											"plot": plot} )
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	liz.addStreamInfo('video', { 'duration': (duration) })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
	return ok

def get_html(url):
	req = urllib2.Request(url)
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
	print "Generate Big Cat Rescue Main Menu"
	index()
elif mode == 4:
	print "Play Video"
elif mode==633:
	print "Big Cat Rescue"
	index()
elif mode==635:
	print "Big Cat Rescue Videos"
	bcr_videos(url)
elif mode==636:
	print "Big Cat Rescue Videos"
	videos(url)
elif mode==637:
	print "Big Cat Rescue Videos"
	sc_streams(url)
elif mode==638:
	print "Big Cat Rescue Videos"
	streams(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
