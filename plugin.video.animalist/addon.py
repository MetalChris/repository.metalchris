#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup


artbase = 'special://home/addons/plugin.video.animalist/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.animalist')
self = xbmcaddon.Addon(id='plugin.video.animalist')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.animalist")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Animalist"

defaultimage = 'special://home/addons/plugin.video.animalist/icon.png'
defaultfanart = 'special://home/addons/plugin.video.animalist/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.animalist/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.animalist').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]




#634
def shows(url):
	response = get_html('http://www.animalist.com/shows')
	soup = BeautifulSoup(response,'html.parser')
	for show in soup.find_all("li",{"class":"grid-item md"}):
		title = striphtml(str(show.find('h5')))
		key = show.find('a')['href']
		url = 'http://animalist.com' + key + '/feed/mp4-large'
		thumbnail = 'http://videos.revision3.com/revision3/images/shows' + key + key + '_web_avatar.jpg'
		add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
	add_directory2('Archives', url, 635, defaultfanart, defaultimage, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#635
def archives(url):
	response = get_html('http://www.animalist.com/shows/archive')
	soup = BeautifulSoup(response,'html.parser')
	for show in soup.find_all("li",{"class":"grid-item md"}):
		title = striphtml(str(show.find('h5')))
		key = show.find('a')['href']
		url = 'http://animalist.com' + key + '/feed/mp4-large'
		thumbnail = 'http://videos.revision3.com/revision3/images/shows' + key + key + '_web_avatar.jpg'
		add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def animalist_videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser').find_all("item")
	for item in soup:
		title = item.find("title").encode('utf-8'); title = re.sub('<[^<]+>', "", title)
		url = item.find("enclosure")["url"]; url = re.sub('--large.', '--hd720p30.', url)
		duration = item.find("media:content")["duration"]#; duration = int(duration)/60
		m, s = divmod(int(duration), 60)
		#runtime = "%02d:%02d"  % (m, s)
		description = item.find("itunes:subtitle").encode('utf-8'); description = re.sub('<[^<]+>', "", description).lstrip()
		image = item.find("media:thumbnail")["url"]
		infoLabels = {'title':title, 'plot':description}
		li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
		li.setProperty('fanart_image',  image)
		li.setProperty('mimetype', 'video/mp4')
		li.setInfo( type='Video', infoLabels=infoLabels )
		li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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
	shows(url)
elif mode == 4:
	xbmc.log("Play Video")
elif mode==634:
	xbmc.log("Animalist Shows")
	shows(url)
elif mode==635:
	xbmc.log("Animalist Archive")
	archives(url)
elif mode==636:
	xbmc.log("Animalist Videos")
	animalist_videos(url)
elif mode==637:
	xbmc.log("Animalist Video")
	animalist_video(url)
elif mode==638:
	xbmc.log("Animalist Most Watched")
	most_watched(name,url)
elif mode==639:
	xbmc.log("Animalist More Shows")
	more_shows(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
