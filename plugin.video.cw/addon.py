#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)


import urllib, xbmcplugin, xbmcaddon, xbmcgui, re, sys, os
import simplejson as json
import mechanize

artbase = 'special://home/addons/plugin.video.cw/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.cw')
self = xbmcaddon.Addon(id='plugin.video.cw')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.cw")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]
__resource__   = xbmc.translatePath( os.path.join( _addon_path, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

from uas import *

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('Host', 'www.cwtv.com')]
br.addheaders = [('User-agent', ua)]
xbmc.log('USER AGENT: ' + str(ua))

plugin = "CW TV Network"

defaultimage = 'special://home/addons/plugin.video.cw/icon.png'
defaultfanart = 'special://home/addons/plugin.video.cw/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.cw/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.cw').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,503,504,515]
force_views = settings.getSetting(id="force_views")


#533
def sites():
	addDir('CW TV Network', 'http://www.cwtv.com/shows/', 633, defaultimage)
	addDir('CW Seed', 'http://www.cwseed.com/shows/', 633, artbase + 'seed.png', artbase + 'seed.jpg')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#633
def shows(name,url):
	br.open('http://www.cwtv.com/')
	response = br.open('http://www.cwtv.com/feed/mobileapp/shows?api_version=3')
	xbmc.log('RESPONSE: ' + str(response.code))
	page = response.get_data()
	jdata = json.loads(page)
	count = jdata['count']
	xbmc.log('COUNT: ' + str(count))
	for i in range(count):
		if 'Network' in name:
			if (jdata['items'][i]['airtime'] == 'STREAM NOW') or (jdata['items'][i]['airtime'] == '') or (jdata['items'][i]['airtime'] == 'COMING SOON') or (jdata['items'][i]['schedule'] == 'coming-soon'):
				continue
		elif 'Seed' in name:
			if (jdata['items'][i]['show_type'] == 'cw-network'):
				continue
		title = jdata['items'][i]['title']
		plot = striphtml(str(jdata['items'][i]['description']))
		url = 'http://www.cwtv.com/shows/' + jdata['items'][i]['slug']
		image = 'http://images.cwtv.com/images/cw/show-hub/' + jdata['items'][i]['slug'] + '.png'
		add_directory2(title,url,30,defaultfanart,image,plot)
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#30
def get_json(name,url,iconimage):
	show = url.rpartition('/')[-1]
	jurl = 'http://www.cwtv.com/feed/mobileapp/videos?show=' + show + '&api_version=3'
	response = br.open(jurl)
	response = br.open(jurl)
	jdata = json.load(response); i = 0
	if 'network' in jdata['videos'][0]['show_type']:
		add_directory2('Show Clips',url,31,defaultfanart,iconimage,plot='Watch video clips from this show.')
	count = len(jdata['videos'])
	for i in range(count):
		if jdata['videos'][i]['fullep'] != 1:
			continue
		get_stuff(jdata,i)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	#add_directory2(title,url,30,image,image,plot=''); i = i + 1
	xbmcplugin.endOfDirectory(addon_handle)


def get_stuff(jdata,i):
	title = jdata['videos'][i]['title']
	image = jdata['videos'][i]['large_thumbnail']
	ep = jdata['videos'][i]['episode']
	airdate = jdata['videos'][i]['airdate']
	description = jdata['videos'][i]['description_long']
	duration = jdata['videos'][i]['duration_secs']
	url = 'https://www.cwtv.com/ioshlskeys/videos' + (image.split('thumbs')[-1]).split('_CWtv')[0] + '.m3u8'
	li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
	li.setProperty('fanart_image', image)
	li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Episode": ep, "Premiered": airdate})
	li.addStreamInfo('video', { 'duration': duration })
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)


#31
def get_clips(url):
	show = url.rpartition('/')[-1]
	url = 'http://www.cwtv.com/feed/mobileapp/videos?show=' + show + '&api_version=3'
	response = br.open(url)
	jdata = json.load(response); i = 0
	count = len(jdata['videos'])
	for i in range(count):
		if jdata['videos'][i]['fullep'] != 0:
			continue
		get_stuff(jdata,i)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	#add_directory2(title,url,30,image,image,plot=''); i = i + 1
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


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

def add_directory2(name,url,mode,fanart,thumbnail,plot,showcontext=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(thumbnail)
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
	sites()
elif mode == 4:
	print "Play Video"
elif mode==533:
	print "CW TV Network Main Menu"
	sites()
elif mode==633:
	print "CW TV Network Main Menu"
	shows(name,url)
elif mode==30:
	print "CW TV Episodes JSON"
	get_json(name,url,iconimage)
elif mode==31:
	print "CW TV Clips JSON"
	get_clips(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
