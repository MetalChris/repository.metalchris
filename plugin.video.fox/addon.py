#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import simplejson as json

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
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))

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
	response = get_json('https://api.fox.com/fbc-content/v1_4/screenpanels/58daf1b54672070001df1400/items?itemsPerPage=50')
	jsob = json.loads(response)
	totalItems = jsob['totalItems']
	for i in range(totalItems):
		seriesType = jsob['member'][i]['seriesType']
		title = jsob['member'][i]['name']
		if (seriesType == 'special'):# or (title == 'MasterChef'):
			continue
		thumbnail = jsob['member'][i]['images']['seriesList']['FHD']
		fanart = jsob['member'][i]['images']['still']['FHD']
		if ('eason' in thumbnail):
			season = (thumbnail.split('eason')[-1])[:3].replace('/','')
			if len(season) < 3:
				season = season.replace('_','_0')
			if 'Family' in title:
				season = '_15'
		elif not 'eason' in thumbnail:
			if 'Simpsons' in title:
				season = '_28'
			if title == 'Rosewood':
				season = '_02'
			if title == 'MasterChef':
				season = '_07'
		else:
			season = '_01'
		show = jsob['member'][i]['url'].rpartition('/')[-1]
		url = 'https://api.fox.com/fbc-content/v1_4/seasons/' + show + season + '/episodes'
		add_directory2(title, url, 636, fanart, thumbnail, plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
		#xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.endOfDirectory(addon_handle)


#636
def FOX_videos(url):
	print '1st'
	response = get_json(url)
	#print response
	try: jsob = json.loads(response)
	except TypeError:
		url = url.rpartition('_')[0]
		url = url + '/episodes'
		print url
		print '2nd'
		response = get_json(url)
	totalItems = jsob['totalItems']
	for i in range(totalItems)[:5]:
		title = jsob['member'][i]['trackingData']['properties']['title'].encode('ascii', 'ignore')
		print title
		contentId = jsob['member'][i]['trackingData']['properties']['contentId']
		url = 'https://api.fox.com/fbc-content/v1_4/screens/video-detail/' + contentId
		thumbnail = jsob['member'][i]['images']['seriesList']['FHD']
		fanart = jsob['member'][i]['images']['still']['FHD']
		description = jsob['member'][i]['description']
		duration = jsob['member'][i]['durationInSeconds']
		originalAirDate = jsob['member'][i]['originalAirDate'].split('T')[0].split('-')
		month = originalAirDate[2]; day = originalAirDate[1]; year = originalAirDate[0]
		airdate = str(month) + '/' + str(day) + '/' + str(year)
		purl = 'plugin://plugin.video.fox?mode=637&url=' + url + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(thumbnail)
		li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
		li.setProperty('fanart_image', fanart)
		#li.setInfo(type="Video", infoLabels={"Title": title, "Episode": ep, "Plot": description, "Premiered": airdate})
		li.setInfo(type="Video", infoLabels={"Title": title, "Plot": description, "Premiered": airdate})
		li.addStreamInfo('video', { 'duration': duration })
		li.addContextMenuItems([('Mark as Watched/Unwatched', 'Action(ToggleWatched)')])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li)
		xbmcplugin.setContent(addon_handle, 'episodes')
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#637
def episode(name,url,iconimage):
	response = get_json(url)
	xbmcgui.Dialog().notification(name, 'Getting URL', defaultimage, 2500, False)
	jsob = json.loads(response)
	videoReleaseURL = jsob['panels']['member'][0]['items']['member'][0]['videoRelease']['url']
	xbmcgui.Dialog().notification(name, 'Following Redirect', defaultimage, 2500, False)
	redirect = get_redirected_url(videoReleaseURL)
	xbmcgui.Dialog().notification(name, 'Fetching Stream URL', defaultimage, 2500, False)
	r = get_json(redirect)
	jsob = json.loads(str(r))
	stream = jsob['playURL']
	xbmc.log('playURL: ' + str(stream))
	streams(name,stream,iconimage)
	xbmcplugin.endOfDirectory(addon_handle)


#650
def streams(name,url,iconimage):
	#response = get_html(url)
	#stream = re.compile('video src="(.+?)"').findall(str(response))[0]
	item = xbmcgui.ListItem(name, path=url, thumbnailImage=iconimage)
	xbmc.log('STREAM: ' + str(url))
	xbmc.executebuiltin("Action(ToggleWatched)")
	xbmc.Player().play( url, item )
	sys.exit("Stop Video")
	xbmcplugin.endOfDirectory(addon_handle)


def get_redirected_url(url):
	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
	opener.addheaders.append(('Host', 'api.fox.com'))
	opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0'))
	opener.addheaders.append(('Accept','application/json, text/plain, */*'))
	#opener.addheaders.append(('apikey','abdcbed02c124d393b39e818a4312055'))
	try:request = opener.open(url)
	except urllib2.HTTPError:
		xbmcgui.Dialog().notification(name, 'Stream Not Available', defaultimage, 5000, False)
		sys.exit()
	return request.url


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
	#req.add_header('Referer','http://www.fox.com')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def get_json(url):
	req = urllib2.Request(url)
	#xbmc.log('JSON_URL: ' + str(url))
	host = url.split('/')[2]
	xbmc.log('HOST: ' + str(host))
	req.add_header('Host', host)
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/50.0')
	#req.add_header('Accept','application/json, text/plain, */*')
	req.add_header('apikey','abdcbed02c124d393b39e818a4312055')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError, error:
		message = error.read()
		xbmc.log('ERROR: ' + str(message))
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
	episode(name,url,iconimage)
elif mode==638:
	xbmc.log("FOX Most Watched")
	most_watched(name,url)
elif mode==639:
	xbmc.log("FOX More Shows")
	more_shows(name,url)
elif mode==650:
	xbmc.log("FOX Shows")
	streams(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
