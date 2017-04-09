#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib


youtube = 'youtube'
vimeo = 'vimeo'
artbase = 'special://home/addons/plugin.video.docstorm/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.docstorm')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.docstorm")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Documentary Storm"

defaultimage = 'special://home/addons/plugin.video.docstorm/icon.png'
defaultfanart = 'special://home/addons/plugin.video.docstorm/fanart.jpg'
#defaultvideo = 'special://home/addons/plugin.video.docstorm/icon.png'
defaulticon = 'special://home/addons/plugin.video.docstorm/icon.png'
#fanart = 'special://home/addons/plugin.video.docstorm/fanart.jpg'
back = ''


local_string = xbmcaddon.Addon(id='plugin.video.docstorm').getLocalizedString

addon_handle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


def CATEGORIES():
	html = get_html('http://documentarystorm.com/')
	match=re.compile('category/(.+?)/" title="').findall(html)
	for name in match:
		url = 'http://documentarystorm.com/category/' + str(name)
		name = name.title()
		addDir(name,url,10,defaulticon,defaultfanart)
		#xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
	xbmcplugin.setContent(addon_handle, 'episodes')
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#10
def get_movies(url):
	html = get_html(url)
	try: nextpage = re.compile('"next" href="(.+?)"').findall(html)[0]
	except IndexError:
		nextpage = 'None'
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'item'})
	for item in soup:
		title = (item.find('img')['alt']).encode('ascii','ignore')
		#xbmc.log('TITLE: ' + str(title))
		image = item.find('img')['src']
		#xbmc.log('IMAGE: ' + str(image))
		url = item.find('a')['href']
		#xbmc.log('URL: ' + str(url))
		plot = item.find('p').text
		plot = re.sub('\s+',' ',plot)
		#xbmc.log('PLOT: ' + str(plot))
		if 'season-3' in url:
			addDir(title,url,30,image,defaultfanart)
		else:
			add_directory(title,url,20,defaultfanart,image,plot=plot)
	if len(nextpage) > 4:
		addDir('Next Page',nextpage,10,defaulticon,defaultfanart)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#20
def get_iframe(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib')#.find_all('iframe')
	#xbmc.log('SOUP: ' + str(soup))
	#for item in soup:
	iframe = soup.find('iframe')['src']
	#iframe = re.compile('src="(.+?)"').findall(str(soup))
	xbmc.log('IFRAME: ' + str(iframe))
	if 'youtube' in str(iframe):
		if 'list' in iframe:
			videoId = iframe.rpartition('=')[-1]
			streamUrl = 'plugin://plugin.video.youtube/play/?playlist_id=' + videoId
			PLAY(name,streamUrl)
		#videoId = str(iframe[0].split('/', 4)[-1])#[:-2]
		else:
			videoId = str(iframe).rpartition('/')[-1]
			xbmc.log('YT videoId: ' + str(videoId))
			streamUrl = ('plugin://plugin.video.youtube/play/?video_id=' + videoId)
	if len(str(iframe)) > 13 and 'snagfilms' in str(iframe):
		iframe = str(iframe)[2:-2].replace('/embed.','/www.')
		snag = get_html(iframe)
		streamUrl = re.compile('src: "(.+?)"').findall(snag)[-1]
		xbmc.log('STREAM URL: ' + str(streamUrl))
	if len(str(iframe)) > 13 and 'vimeo' in str(iframe):
		iframe = str(iframe)[2:-2]#.replace('/embed.','/www.')
		vimeo = get_html(iframe)
		streamUrl = str(re.compile('"url":"(.+?)"').findall(vimeo)[4])
		xbmc.log('STREAM URL: ' + str(streamUrl))
	if len(str(iframe)) > 13 and 'rt.com' in str(iframe):
		xbmc.log('RT')
		iframe = str(iframe)#.replace('/embed.','/www.')
		rt = get_html(iframe)
		soup = BeautifulSoup(rt,'html5lib').find_all('script')[4]
		streamUrl = 'https://rtd.rt.com/files/films/' + str(re.compile("file: '(.+?)'}").findall(rt)[0]).split(' + ')[-1].replace("'","")
		xbmc.log('STREAM URL: ' + str(streamUrl))
	if len(str(iframe)) > 13 and 'nfb.ca' in str(iframe):
		xbmc.log('NFB')
		iframe = str(iframe)[2:-2]#.replace('/embed.','/www.')
		nfb = get_html(iframe)
		entryId = str(re.compile('"entry_id": "(.+?)"').findall(nfb)[-1])
		streamUrl = 'http://www.kaltura.com/p/243342/sp/24334200/playManifest/entryId/' + entryId + '/flavorId/1_6wf0o9n7/format/url/protocol/http/a.mp4'
		xbmc.log('STREAM URL: ' + str(streamUrl))
	PLAY(name,streamUrl)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#30
def episodes(name,url):
	html = get_html(url)
	image = re.compile('image" content="(.+?)"').findall(html)[0]
	iframe = re.compile('frame src="(.+?)"').findall(html)[-1]
	xbmc.log('IFRAME: ' + str(iframe))
	if 'list' in iframe:
		videoId = iframe.rpartition('=')[-1]
		streamUrl = 'plugin://plugin.video.youtube/play/?playlist_id=' + videoId
		PLAY(name,streamUrl)
	videoId = str(iframe).rpartition('/')[-1]
	streamUrl = ('plugin://plugin.video.youtube/play/?video_id=' + videoId)
	title = name + ' Episode 1'
	add_directory(title,streamUrl,99,defaultfanart,image,plot='')
	xbmcplugin.setContent(addon_handle, 'episodes')
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'id':'episode-links'})
	match = re.compile('<a href="(.+?)"><span>(.+?)</span>').findall(str(soup))
	for url, episode in match:
		title = name + ' Episode ' + episode
		add_directory(title,url,20,defaultfanart,image,plot='')
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)



#99
def PLAY(name,url):
	print url
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def add_directory(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		liz.setProperty('IsPlayable', 'true')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
		return ok


def add_directory2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		liz.setProperty('IsPlayable', 'true')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=10)
		return ok

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
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
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
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
	print "Generate Main Menu"
	CATEGORIES()
elif mode == 1:
	print "Indexing Videos"
	INDEX(url)
elif mode == 4:
	print "Play Video"
elif mode == 6:
	print "Get Episodes"
	get_episodes(url)
elif mode == 10:
	print "Indexing Videos"
	get_movies(url)
elif mode == 20:
	print "Documentary Storm IFRAME"
	get_iframe(name,url)
elif mode == 30:
	print "Documentary Storm EPISODES"
	episodes(name,url)
elif mode == 99:
	print "Play Video"
	PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


