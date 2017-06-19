#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, sys


artbase = 'special://home/addons/plugin.video.moviezoot/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.moviezoot')
self = xbmcaddon.Addon(id='plugin.video.moviezoot')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.moviezoot")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "MovieZoot"

defaultimage = 'special://home/addons/plugin.video.moviezoot/icon.png'
defaultfanart = 'special://home/addons/plugin.video.moviezoot/curtains.jpg'
defaulticon = 'special://home/addons/plugin.video.moviezoot/icon.png'

local_string = xbmcaddon.Addon(id='plugin.video.moviezoot').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]
mode = 110

#110
def mz_genres(url):
		html = get_html('http://moviezoot.com')
		genres = re.compile('<div class="list-item-container"><a href="(.+?)"><img src="(.+?)"').findall(html)
		for url, image in genres:
			url = 'http://moviezoot.com' + str(url)[:-1]
			title = url.replace('-',' ').split('/',4)[-1].title()
			image = 'http://moviezoot.com' + str(image)
			add_directory2(title,url,111, defaultfanart ,image,plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		add_directory2('Binge Watching','http://moviezoot.com/binge-watching/',112, defaultfanart ,defaulticon,plot='Got some time to kill? How about binge watching some free streaming outstanding comedies from the past?  Or how about some great mysteries? Or documentaries?')
		xbmcplugin.endOfDirectory(addon_handle)


#111
def mz_movies(url):
		html = get_html(url)
		movies = re.compile('<div class="list-item-container"><a href="(.+?)"><img alt="(.+?)" title="(.+?) />').findall(html)
		for url, title, image in movies:
			image = re.compile('src="(.+?)"').findall(image)[0]
			add_directory(title,url,120,defaultfanart,image,plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		xbmcplugin.endOfDirectory(addon_handle)


#112
def mz_binge(url):
		html = get_html(url)
		binge = re.compile('<div class="list-item-container"><a href="(.+?)"><img class="alignnone size-full wp-image-217" src="(.+?)" alt="(.+?)"').findall(html)
		for url, image,title in binge:
			url = 'http://moviezoot.com' + str(url)[:-1]
			title = title.lstrip().replace('Binge Watching ','').split(' - ')[0]
			url = url + ',' + image
			add_directory2(title,url,113, defaultfanart ,image,plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		xbmcplugin.endOfDirectory(addon_handle)


#113
def mz_episodes(url):
		eurl = url.split(',')[0]
		image = url.split(',')[-1]
		html = get_html(eurl)
		if 'marx' in eurl:
			episodes = re.compile('<div class="list-item-container"><a href="(.+?)"><img alt="(.+?)"').findall(html)
		else:
			episodes = re.compile('<li><a href="(.+?)">(.+?)</a>').findall(html)
		for url, title in episodes:
			add_directory(title,url,120,defaultfanart,image,plot='')
			xbmcplugin.setContent(pluginhandle, 'episodes')
		xbmcplugin.endOfDirectory(addon_handle)


#114
def get_episode(url):
	html = get_html(url)
	url = re.compile('"file":"(.+?)"').findall(html)
	url = str(url)[2:-2]
	get_stream(url)
	xbmcplugin.endOfDirectory(addon_handle)


#120
def get_stream(url):
	html = get_html(url)
	stream = re.compile('file":"(.+?)"').findall(str(html))[0]
	play(stream)
	xbmcplugin.endOfDirectory(addon_handle)


def play(url):
	print url
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	item.setProperty('IsFolder', 'false')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), succeeded=True, listitem=item)



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
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=10)
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
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=10)
		return ok


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

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
	print "MovieZoot Genres"
	mz_genres(url)
elif mode == 1:
	print "Indexing Videos"
	INDEX(url)
elif mode == 4:
	print "Play Video"

elif mode==100:
	print "search"
	doSearch(url)
elif mode==110:
	print "MovieZoot Genres"
	mz_genres(url)
elif mode==111:
	print "MovieZoot Movies"
	mz_movies(url)
elif mode==112:
	print "MovieZoot Binge"
	mz_binge(url)
elif mode==113:
	print "MovieZoot Episodes"
	mz_episodes(url)
elif mode==114:
	print "MovieZoot Episode Stream"
	get_episodes(url)
elif mode==120:
	print "MovieZoot Get Stream"
	get_stream(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
