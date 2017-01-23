#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib
import simplejson as json


settings = xbmcaddon.Addon(id="plugin.video.nautilus")
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.nautilus')
addon = xbmcaddon.Addon(id="plugin.video.nautilus")
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')
translation = selfAddon.getLocalizedString
local_string = xbmcaddon.Addon(id='plugin.video.nautilus').getLocalizedString
download = settings.getSetting(id="download")

plugin = "Nautilus Live"

defaultimage = 'special://home/addons/plugin.video.nautilus/icon.png'
defaultfanart = 'special://home/addons/plugin.video.nautilus/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.nautilus/icon.png'
defaulticon = 'special://home/addons/plugin.video.nautilus/icon.png'
baseurl = 'http://nautiluslive.org'
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,510,514]
window_id = xbmcgui.getCurrentWindowId()
xbmc.log(str(window_id))


def CATEGORIES():
	if window_id == 10025:
		addDir('Channel 1', 'http://nautiluslive.org/live/channel-1', 1, defaultimage)
		addDir('Channel 2', 'http://nautiluslive.org/live/channel-2', 1, defaultimage)
		addDir('Quad', 'http://nautiluslive.org/live/quad', 1, defaultimage)
	else:
		get_albums('http://nautiluslive.org/albums')
		#addDir('Photo Albums', 'http://nautiluslive.org/albums', 5, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#1
def INDEX(name,url):
	html = get_html(url)
	try: soup = BeautifulSoup(html,'html5lib').find_all('iframe',{'id':'playerIFrame'})
	except TypeError:
		xbmcgui.Dialog().notification(plugin + ' ' +name, 'Expedition 2016 has ended.  Check back in April 2017.', defaultimage, 5000, False)
		sys.exit()
	for item in soup:
		url = item.get('src')
		urlkey = re.compile('s=(.+?)&').findall(url)[-1]
		jsonurl = 'http://player.piksel.com/ws/get_live_series_events/s/' + urlkey + '/api/62c22d1d-269b-11e3-b5cd-005056865f49/apiv/4/mode/json'
		jresponse = urllib2.urlopen(jsonurl)
		jdata = json.load(jresponse)
		uuid = str(jdata['response']['getLiveSeriesEventsResponse']['liveEvents'])[3:11]
		streamurl = (jdata['response']['getLiveSeriesEventsResponse']['liveEvents'][uuid]['streamPackages'][0]['m3u8'])
		listitem = xbmcgui.ListItem('Nautilus Live ' + name, thumbnailImage = defaultimage)
		xbmc.Player().play( streamurl, listitem )
		sys.exit()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


#5
def get_albums(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'media-widget media-photo-click'})
	for item in soup:
		title = item.find('div',{'class':'title'}).text
		url = baseurl + item.find('a')['href']
		image = baseurl + item.find('img')['src']#re.compile('url\\((.+?)\\)').findall(str(item))[-1]
		addDir(title, url, 10, image)
	xbmcplugin.endOfDirectory(handle=addon_handle, succeeded=True, updateListing=False, cacheToDisc=True)


#10
def get_photos(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'grid-item'})
	for item in soup:
		if item.find('img')['alt']:
			title = remove_crap(striphtml(str(item.find('img')['alt'])))
		else:
			title = remove_crap(name)
		image = baseurl + item.find('img')['src']
		url = unicode(image.replace('photo_thumbnail','photo_display_large'))
		url = ((url.split('itok'))[0])[:-1]
		liz=xbmcgui.ListItem(unicode(title), iconImage=unicode(image),thumbnailImage=unicode(image))
		liz.setInfo( type="Image", infoLabels={ "Title": name })
		#commands = []
		#commands.append
		#liz.addContextMenuItems([('Download Image', 'XBMC.RunPlugin(%s?mode=80&url=%s&name=%s)' % (sys.argv[0], url, title))])
		#xbmcplugin.setContent(addon_handle, 'picture')
		xbmcplugin.addDirectoryItem(handle=addon_handle,url=unicode(url),listitem=liz,isFolder=False)
	#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	xbmcplugin.endOfDirectory(handle=addon_handle, succeeded=True, updateListing=False, cacheToDisc=True)


def downloader(name,url):
		path = addon.getSetting('download')
		if path == "":
			xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
					%(translation(30000), translation(30010), defaulticon))
			addon.openSettings()
			path = addon.getSetting('download')
		if path == "":
			return
		file_name = url.split('/')[-1]
		dlsn = settings.getSetting(id="status")
		bsize = settings.getSetting(id="bsize")
		xbmc.log( 'Buffer Size= ' + str(bsize))
		ret = xbmcgui.Dialog().yesno("Nautilus Live", 'Download Selected File?', str(file_name))
		if ret == False:
			return get_photos
		else:
			xbmcgui.Dialog().notification('Nautilus Live', 'Download Started.', xbmcgui.NOTIFICATION_INFO, 5000)
		xbmc.log( 'URL= ' + str(url))
		xbmc.log( 'Filename= ' + str(file_name))
		xbmc.log( 'Download Location= ' + str(download))
		u = urllib2.urlopen(url)
		f = open(download+file_name, 'wb')
		meta = u.info()
		file_size = float(meta.getheaders("Content-Length")[0])
		file_sizeMB = float(file_size/(1024*1024))
		xbmc.log( "Downloading: %s %s MB" % (file_name, "%.2f" % file_sizeMB))
		file_size_dl = 0
		block_sz = int(bsize)
		while True:
			buffer = u.read(block_sz)
		if not buffer:
			return
		file_size_dl += float(len(buffer))
		file_size_dlMB = float(file_size_dl/(1024*1024))
		f.write(buffer)
		status = "%.2f  [%3.2f%%]" % (file_size_dlMB, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		if dlsn!='false':
			xbmcgui.Dialog().notification('Nautilus Live Download in Progress', str(status) + ' of ' + ("%.2f" % float(file_sizeMB)) + ' MB', xbmcgui.NOTIFICATION_INFO, 2500)
		else:
			pass
		f.close()
		xbmcgui.Dialog().notification('Nautilus Live', 'Download Completed.', xbmcgui.NOTIFICATION_INFO, 5000)
		xbmc.log( 'Download Completed')


def remove_crap(data):
	data = data.replace('&nbsp;',' ').replace('&amp;','&')
	return data	


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def sanitize(data):
	output = ''
	for i in data:
		for current in i:
			if ((current >= '\x20') and (current <= '\xD7FF')) or ((current >= '\xE000') and (current <= '\xFFFD')) or ((current >= '\x10000') and (current <= '\x10FFFF')):
			   output = output + current
	return output



def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')

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

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

xbmc.log( "Mode: " + str(mode))
xbmc.log( "URL: " + str(url))
xbmc.log( "Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log( "Nautilus Live Menu")
	CATEGORIES()
elif mode == 1:
	xbmc.log( "Nautilus Live Play Video")
	INDEX(name,url)
elif mode == 5:
	xbmc.log( "Nautilus Photo Albums")
	get_albums(url)
elif mode == 10:
	xbmc.log( "Nautilus Photos")
	get_photos(name,url)
elif mode == 80:
   xbmc.log( "Download File")
   downloader(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
