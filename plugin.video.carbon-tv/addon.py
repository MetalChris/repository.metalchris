#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, xbmcplugin, sys, os
from bs4 import BeautifulSoup
import html5lib
import cookielib

artbase = 'special://home/addons/plugin.video.carbon-tv/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.carbon-tv')
self = xbmcaddon.Addon(id='plugin.video.carbon-tv')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.carbon-tv")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]
xbmc_monitor = xbmc.Monitor()

plugin = "CarbonTV"

defaultimage = 'special://home/addons/plugin.video.carbon-tv/icon.png'
defaultfanart = 'special://home/addons/plugin.video.carbon-tv/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.carbon-tv/icon.png'
baseurl = 'https://www.carbontv.com/users/login'

local_string = xbmcaddon.Addon(id='plugin.video.carbon-tv').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
q = settings.getSetting(id="quality")
username = settings.getSetting(id="username")
password = settings.getSetting(id="password")
views = settings.getSetting(id="views")
confluence_views = [500,501,502,503,504,508,515]
payload = {'data[User][email]' : username,'data[User][password]' : password,'data[User][remember_me]' : '0','data[User][remember_me]' : '1'}



#10
def cats(url):
	html = get_html('http://www.carbontv.com/channels')
	check = re.compile('isLoggedInTest = (.+?);').findall(str(html))
	xbmc.log(str(check))
	#if check[0] != 'true':
		#xbmcgui.Dialog().notification(plugin, 'Login Failed', iconimage, 5000, False)
		#return
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'content-listing channels-listing clearfix'})
	for item in soup:
		title = item.find('h2').string.encode('utf-8').title()
		url = 'http://www.carbontv.com' + item.find('a',{'class':'channels-cta'})['href']
		if 'cams' in url:
			continue
		image = item.find('img')['src']
		if 'pbr' in url:
			mode = 11
		else:
			mode = 15
		add_directory2(title,url,mode,image,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#11
def pbr(url):
	addDir2('On Demand','http://www.carbontv.com/videos/recent/episodes/limit:999/show_id:88/',20,artbase + 'pbr.jpg')
	addDir2('Highlights','http://www.carbontv.com/videos/recent/clips/limit:999/show_id:88/',20,artbase + 'pbr.jpg')
	xbmcplugin.endOfDirectory(addon_handle)


#15
def shows(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('article',{'class':'content-third content-image-container'})
	for item in soup:
		title = item.find('h3').string.encode('utf-8').strip()
		image = item.find('img')['src']
		show_id = image.split('/')
		url = 'http://www.carbontv.com/videos/recent/episodes/limit:999/show_id:' + show_id[9]
		add_directory2(title,url,20,image,image,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('article',{'class':'content-quarter content-image-container'})
	for item in soup:
		title = item.find('h5').string.encode('utf-8').strip()
		url = 'http://www.carbontv.com' + item.find('a',{'class':'content-image video-link'})['href']
		duration = striphtml(str(item.find('div',{'class':'thumb-duration'})))#.string.encode('utf-8')
		runtime = get_sec(duration)
		thumbnail = item.find('img',{'class':'category-image full-image'})['src']
		purl = 'plugin://plugin.video.carbon-tv?mode=30&url=' + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(thumbnail)
		li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
		li.setProperty('fanart_image', thumbnail)
		li.setProperty('mimetype', 'video/mp4')
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="video", infoLabels={ 'Title': title, 'Plot': '' })
		li.addStreamInfo('video', { 'duration': runtime })
		li.addContextMenuItems([('Mark as Watched/Unwatched', 'Action(ToggleWatched)')])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li, isFolder=False)
		xbmcplugin.setContent(addon_handle, 'episodes')
	xbmc.log('DURATION: ' + str(runtime))
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#30
def streams(name,url):
	response = get_html(url)
	duration = re.compile('duration" content="(.+?)"').findall(str(response))[0]
	runtime = int(get_sec(duration)*1000)
	xbmc.log('DURATION: ' + str(runtime))
	link = re.compile('<link rel="video_src" href="(.+?)"').findall(str(response))[0]
	thumbnail = re.compile('<link rel="image_src" href="(.+?)"').findall(str(response))[0]
	key = link.split('=')[-1]
	if q =='2':
		qkey = 487091#keys[-1]
	elif q =='1':
		qkey = 487081#keys[-4]
	elif q =='0':
		qkey = 487061#keys[-7]
	#stream = (thumbnail.split('version')[0]).replace('cfvod.kaltura.com','carbonmedia-a.akamaihd.net').replace('thumbnail','serveFlavor') + 'v/2/flavorId/' + key + '/forceproxy/true/name/a.mp4'
	stream = 'https://cdnapisec.kaltura.com/p/1897241/sp/189724100/playManifest/entryId/' + key + '/format/download/protocol/https/flavorParamIds/' + str(qkey)
	xbmc.log('STREAM: ' + str(stream))
	listitem = xbmcgui.ListItem(name, path=stream, thumbnailImage=thumbnail)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


def get_sec(time_str):
	try: h, m, s = time_str.split(':')
	except ValueError:
		m, s = time_str.split(':')
		return int(m) * 60 + int(s)
	return int(h) * 3600 + int(m) * 60 + int(s)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	item.setProperty('IsFolder', 'false')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), succeeded=True, listitem=item)


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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu")
	cats(url)
elif mode == 4:
	xbmc.log("Play Video")
elif mode==11:
	xbmc.log('CarbonTV PBR')
	pbr(url)
elif mode==15:
	xbmc.log('CarbonTV Shows')
	shows(url)
elif mode==20:
	xbmc.log("CarbonTV Videos")
	videos(url)
elif mode==30:
	xbmc.log("CarbonTV Streams")
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
