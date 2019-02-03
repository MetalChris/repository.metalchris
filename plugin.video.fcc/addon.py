#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, re, sys
from bs4 import BeautifulSoup
import html5lib
import simplejson as json

artbase = 'special://home/addons/plugin.video.fcc/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.fcc')
self = xbmcaddon.Addon(id='plugin.video.fcc')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.fcc")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Family Christian Center"

defaultimage = 'special://home/addons/plugin.video.fcc/icon.png'
defaultfanart = 'special://home/addons/plugin.video.fcc/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.fcc/icon.png'
baseurl = 'http://www.huntchannel.tv'
schedule = 'special://home/addons/plugin.video.fcc/resources/media/schedule.json'

local_string = xbmcaddon.Addon(id='plugin.video.fcc').getLocalizedString
addon_handle = int(sys.argv[1])
#q = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]
#if log_notice != 'false':
	#log_level = 2
#else:
	#log_level = 1

log_level = 2
#xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

#https://limelight1.streamspot.com/go/cb6e72ee89_mbr2/playlist.m3u8

def cats():
	addDir2('Live Webcast','https://api.streamspot.com/broadcaster/cb6e72ee89?apiKey=73d4c9e8-2320-4800-a379-6ef591eae4c1',10,defaultimage)
	addDir('Archived Sermons','http://www.fcclive.com/sermon-archives/page/1/',11,defaultimage)
	xbmcplugin.endOfDirectory(addon_handle)


#10
def live(name,url,iconimage):
	response = get_html(url)
	jdata = json.loads(response)
	live_key = (jdata['data']['church']['isBroadcasting'])
	xbmc.log(str(live_key),level=log_level)
	if str(live_key) != 'False':
		stream = (jdata['data']['church']['live_src']['hls'])
		listitem = xbmcgui.ListItem('Family Christian Center ' + name, thumbnailImage=defaulticon)
		listitem.setProperty('mimetype', 'video/x-mpegurl')
		xbmc.Player().play( stream, listitem )
		sys.exit()
	else:
		line1 = "Live Broadcast Schedule:"
		line2 = "Sunday - 8:30 AM, 9:45 AM, 11:15 AM [ET] "
		line3 = "Monday - 7:00 PM [ET] - Campus Night"
		xbmcgui.Dialog().ok(plugin, line1, line2, line3)
		#xbmcgui.Dialog().notification(plugin, 'No Live Broadcast Available.', defaultimage, 5000, False)
		sys.exit()
		xbmc.log('No Live Broadcast Available',level=log_level)
		return
		xbmcplugin.endOfDirectory(addon_handle)


#11
def vod(url):
	addDir('All Sermons','http://www.fcclive.com/sermon-archives/1/',13,defaulticon)
	addDir('Categories','http://www.fcclive.com/sermon-archives/',14,defaulticon)
		xbmcplugin.endOfDirectory(addon_handle)


#13
def get_vod(url):
	this_url = url
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'col-md-9 col-sm-9'})
	xbmc.log('SOUP: ' + str(soup),level=log_level)
	for item in soup:
		url = item.find('a')['href']
		title = item.find('h3').text.encode('utf-8')
		add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
	if 'pagination' in str(html):
		last = BeautifulSoup(html,'html5lib').find_all('ul',{'class':'pagination'})
		links = re.compile('href="(.+?)"').findall(str(last))
		page = int(filter(str.isdigit, this_url))
		nxt = int(page) + 1
		next_url = 'http://www.fcclive.com/sermon-archives/page/' + str(nxt) +'/'
		if str(links[-1]) != str(this_url):
			add_directory2('Next Page',next_url,13,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#14
def categories(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('select',{'id':'sermons-category'})
	xbmc.log(str(len(soup)),level=log_level)
	titles = re.compile('">(.+?)</').findall(str(soup))#.string.encode('utf-8').title()
	titles.pop(0)
	xbmc.log(str(len(titles)),level=log_level)
	links = re.compile('value="(.+?)">').findall(str(soup))
	xbmc.log(str(len(links)),level=log_level)
	for title,link in zip(titles,links):
		if 'Sermons' in title:
		continue
		if 'Sermons' in link:
		link = (link.split('"'))[-1]
		url = 'http://www.fcclive.com/page/1/?sermons-category=' + link
		add_directory2(title,url,15,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#15
def sermons(url):
	this_url = url
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'col-md-9 col-sm-9'})
	for item in soup:
		url = item.find('a')['href']
		title = item.find('h3').text.encode('utf-8')
		add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
	if 'pagination' in str(html):
		category = (this_url.split('='))[-1]
		last = BeautifulSoup(html,'html5lib').find_all('ul',{'class':'pagination'})
		links = re.compile('href="(.+?)"').findall(str(last))
		page = int(filter(str.isdigit, this_url))
		nxt = int(page) + 1
		next_url = 'http://www.fcclive.com/page/' + str(nxt) +'/?sermons-category=' + str(category)
		if str(links[-1]) != str(this_url):
			add_directory2('Next Page',next_url,15,defaultfanart,defaultimage,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'entry-content'})
	for item in reversed(soup):
		title = (item.find('a')['title']).encode('utf-8').strip()
		image = item.find('img')['src']
		#show_id = image.split('/')
		url = item.find('a')['href']
		add_directory2(title,url,30,defaultfanart,image,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#21
def s_videos(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'entry-content'})
	for item in reversed(soup):
		title = (item.find('a')['title']).encode('utf-8').strip()
		image = item.find('img')['src']
		show_id = image.split('/')
		url = item.find('a')['href']
		add_directory2(title,url,31,defaultfanart,image,plot='')
		#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
		xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('div',{'class':'video-container'})
	for item in soup:
		iframe = item.find('iframe')['src']
		if 'http:' not in iframe:
			iframe = 'http:' + str(iframe)
	xbmc.log(str(iframe),level=log_level)
	source = get_iframe(iframe)
	mpeg4 = []
	sources = re.compile('profile":(.+?)}').findall(str(source))
	#xbmc.log(len(sources)
	for item in sources:
		if 'mp4' in item:
			mpeg4.insert(0,item)
	#xbmc.log(len(mpeg4)
	xbmc.log(str(mpeg4),level=log_level)
	for item in mpeg4:
		if '720' in item:
			stream = re.compile('url":"(.+?)"').findall(str(item))[0]
		play(name,stream,defaultimage)
		xbmcplugin.endOfDirectory(addon_handle)


#31
def s_streams(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('iframe')[0]
	iframe = re.compile('src="(.+?)"').findall(str(soup))[0]
	source = get_iframe(iframe)
	thumbnail = re.compile('base":"(.+?)"').findall(str(source))[-1]
	m3u8 = (re.compile('"url":"(.+?)"').findall(str(source))[0]).split(',')
	check = (m3u8[0])[-4:]
	xbmc.log(str(check),level=log_level)
	if check == 'm3u8':
		stream = m3u8[0]
	else:
		stream = m3u8[0] + '/master.m3u8'
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
	xbmc.Player().play( stream, listitem )
	sys.exit()
		xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(name,url,iconimage):
		xbmc.log(str(url),level=log_level)
	listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
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
	req.add_header('Host', 'www.fcclive.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def get_iframe(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'player.vimeo.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	req.add_header('Referer', 'http://huntchannel.tv/')

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

def addListItem(label, image, url, isFolder, infoLabels = False, fanart = False, duration = False):
	listitem = xbmcgui.ListItem(label = label, iconImage = image, thumbnailImage = image)
	if not isFolder:
		if settings.getSetting('download') == '' or settings.getSetting('download') == 'false':
			listitem.setProperty('IsPlayable', 'true')
	if fanart:
		listitem.setProperty('fanart_image', fanart)
	if infoLabels:
		listitem.setInfo(type = 'video', infoLabels = infoLabels)
		if duration:
			if hasattr(listitem, 'addStreamInfo'):
				listitem.addStreamInfo('video', { 'duration': int(duration) })
			else:
				listitem.setInfo(type = 'video', infoLabels = { 'duration': str(datetime.timedelta(milliseconds=int(duration)*1000)) } )
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = isFolder)
	return ok

def addLink(name, url, mode, iconimage, fanart=True, infoLabels=True):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=False)
	return ok

def add_item( action="" , title="" , plot="" , url="" ,thumbnail="" , folder=True ):
	_log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] folder=["+str(folder)+"]")

	listitem = xbmcgui.ListItem( title, iconImage=iconimage, thumbnailImage=iconimage )
	listitem.setInfo( "video", { "Title" : title, "FileName" : title, "Plot" : plot } )

	if url.startswith("plugin://"):
		itemurl = url
		listitem.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem)
	else:
		itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ))
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
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


def addDir2(name,url,mode,iconimage, fanart=True, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',defaultfanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok


def addDirectoryItem2(name, isFolder=True, parameters={}):
	''' Add a list item to the XBMC UI.'''
	li = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
	li.setProperty('fanart_image', defaultfanart)
	url = sys.argv[0] + '?' + urllib.urlencode(parameters)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)


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
	cats()
elif mode == 4:
	xbmc.log("Play Video",level=log_level)
elif mode==10:
		xbmc.log('FCC Live',level=log_level)
	live(name,url,iconimage)
elif mode==11:
		xbmc.log('FCC VOD',level=log_level)
	vod(url)
elif mode==13:
		xbmc.log('FCC VOD ALL',level=log_level)
	get_vod(url)
elif mode==14:
		xbmc.log('FCC VOD CATEGORIES',level=log_level)
	categories(url)
elif mode==15:
		xbmc.log('FCC VOD SERMONS',level=log_level)
	sermons(url)
elif mode==30:
		xbmc.log('FCC VOD ALL',level=log_level)
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
