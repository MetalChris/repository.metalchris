#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

#2019.02.16

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys, os
#import simplejson as json
import json
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
#from ahole import *

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('Host', 'www.cwtv.com')]
br.addheaders = [('User-agent', ua)]
xbmc.log('USER AGENT: ' + str(ua))

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

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
	xbmc.log('RESPONSE: ' + str(response.code),level=log_level)
	page = response.get_data()
	jdata = json.loads(page)
	count = jdata['count']
	xbmc.log('COUNT: ' + str(count),level=log_level)
	for i in range(count):
		if 'Network' in name:
			if (jdata['items'][i]['airtime'] == '') or (jdata['items'][i]['airtime'] == 'COMING SOON') or (jdata['items'][i]['schedule'] == 'coming-soon'):
			#if (jdata['items'][i]['airtime'] == 'STREAM NOW') or (jdata['items'][i]['airtime'] == '') or (jdata['items'][i]['airtime'] == 'COMING SOON') or (jdata['items'][i]['schedule'] == 'coming-soon'):
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
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.endOfDirectory(addon_handle)


#30
def get_json(name,url,iconimage):
	show = url.rpartition('/')[-1]
	xbmc.log('SHOW: ' + str(show),level=log_level)
	jurl = 'http://www.cwtv.com/feed/mobileapp/videos?show=' + show + '&api_version=3'
	response = br.open(jurl)
	#response = br.open(jurl)
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
	#url = 'https://www.cwtv.com/ioshlskeys/videos' + (image.split('thumbs')[-1]).split('_CWtv')[0] + '.m3u8'
	mpx_url = jdata['videos'][i]['mpx_url']
	xbmc.log('MPX_URL: ' + str(mpx_url),level=log_level)
	url = get_m3u8(mpx_url)
	li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
	li.setProperty('fanart_image', image)
	li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Episode": ep, "Premiered": airdate})
	li.addStreamInfo('video', { 'duration': duration })
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)


def get_m3u8(url):
	QUALITY = settings.getSetting(id="quality")
	xbmc.log('QUALITY: ' + str(QUALITY),level=log_level)
	res = ['360', '540', '720', '1080', '']
	xbmc.log('RESOLUTION: ' + str(res[int(QUALITY)]),level=log_level)
	html = get_html(url)
	#xbmc.log('HTML: ' + str(html))
	m3u8_url = re.compile('video src="(.+?)" ').findall(str(html))[0]
	data = get_html(m3u8_url)
	#xbmc.log('M3U8_DATA: ' + str(data),level=log_level)
	streams = re.findall(r'https.*m3u8', str(data), flags=re.MULTILINE);links = [];rqs = []
	xbmc.log('LENGTH: ' + str(len(streams)),level=log_level)
	for stream in streams:
		if res[int(QUALITY)] == '':
			return m3u8_url
		if res[int(QUALITY)] in stream:
			return stream
	#xbmc.log('STREAMS: ' + str(streams),level=log_level)
	#return streams[-1]
	return m3u8_url


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html



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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu",level=log_level)
	sites()
elif mode == 4:
	xbmc.log("Play Video",level=log_level)
elif mode==533:
	xbmc.log("CW TV Network Main Menu",level=log_level)
	sites()
elif mode==633:
	xbmc.log("CW TV Network Main Menu",level=log_level)
	shows(name,url)
elif mode==30:
	xbmc.log("CW TV Episodes JSON",level=log_level)
	get_json(name,url,iconimage)
elif mode==31:
	xbmc.log("CW TV Clips JSON",level=log_level)
	get_clips(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
