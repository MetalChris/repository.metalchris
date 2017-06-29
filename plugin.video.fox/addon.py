#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup


artbase = 'special://home/addons/plugin.video.fox/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.fox')
self = xbmcaddon.Addon(id='plugin.video.fox')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.fox")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "FOX"

defaultimage = 'special://home/addons/plugin.video.fox/icon.png'
defaultfanart = 'special://home/addons/plugin.video.fox/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.fox/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.fox').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]
airdate = ''


#633
def shows():
	response = get_html('http://www.fox.com/full-episodes')
	soup = BeautifulSoup(response,'html.parser').find_all('li',{'class':'leaf depth-3'})
	for show in soup:
		title = striphtml(str(show.find('a')))
		url = show.find('a')['href']
		if not 'full-episodes' in url:
			url = url + '/full-episodes'
		thumbnail = defaultimage
		add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#636
def FOX_videos(url):
	if 'prisonbreak' in url:
		url = url.replace('prisonbreak','prison-break')
	if 'kicking-and-screaming' in url:
		url = url.replace('kicking-and-screaming','kicking-screaming')
	response = get_html(url)
	if response == False:
		xbmcgui.Dialog().notification(name, 'No Episodes Available', defaultimage, 5000, False)
		sys.exit()
		xbmc.log('PAGE NOT FOUND')
	soup = BeautifulSoup(response,'html.parser').find_all('div')
	xbmc.log('SOUP: ' + str(len(soup)))
	for item in soup:
		if not item.find('h2'):
			continue
		if not item.find('div',{'class':'views-field views-field-field-image-thumb'}):
			continue
		if item.find('div',{'class':'video-lock mvpd-locked'}):
			continue
		title = item.find('h2').text.encode('utf-8')
		if 'FULL EPISODES' in title:
			continue
		url = 'http://www.fox.com' + item.find('a')['href']
		purl = 'plugin://plugin.video.fox?mode=637&url=' + url
		image = item.find('img',{'typeof':'foaf:Image'})
		thumbnail = image.get('src')
		airdate = item.find('span',{'class':'date-display-single'})#.text
		airdate = airdate.get('content').split('T')[0].replace('-','/')
		ep = item.find('span',{'class':'ep-num'}).text.split(' ')[-1]
		if not item.find('p'):
			continue
		li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
		li.setProperty('fanart_image', defaultfanart)
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Episode": ep, "Premiered": airdate})
		#li.addStreamInfo('video', { 'duration': duration })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
    	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#637
def episode(url):
	response = get_html(url)
	platform = re.compile('release_url":"(.+?)"').findall(response)[0].replace('\\','') + '&manifest=m3u'
	xbmc.log('PLATFORM: ' + str(platform))
	streams(platform)


#650
def streams(url):
	response = get_html(url)
	stream = re.compile('video src="(.+?)"').findall(str(response))[0]
	xbmc.log('STREAM: ' + str(stream))
	xbmc.Player().play( stream )
	sys.exit("Stop Video")
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
												"plot": plot,
												"Premiered": airdate} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok


def add_directory(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot,
												"Premiered": airdate} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok

def get_html(url):
	req = urllib2.Request(url)
	req.add_header('Host','www.fox.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/50.0')
	req.add_header('Referer','http://www.fox.com')

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
	shows()
elif mode == 4:
	xbmc.log("Play Video")
elif mode==633:
	xbmc.log("FOX Shows")
	shows()
elif mode==635:
	xbmc.log("FOX Archive")
	archives(url)
elif mode==636:
	xbmc.log("FOX Videos")
	FOX_videos(url)
elif mode==637:
	xbmc.log("FOX Episode")
	episode(url)
elif mode==638:
	xbmc.log("FOX Most Watched")
	most_watched(name,url)
elif mode==639:
	xbmc.log("FOX More Shows")
	more_shows(name,url)
elif mode==650:
	xbmc.log("FOX Shows")
	streams(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
