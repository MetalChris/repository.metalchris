#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)


import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests  
import urlparse
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
import simplejson as json
import html5lib


#widget = 'Lz93aWRnZXRDb250ZW50SWQ9MjA1Nzk4NyZ3aWRnZXROYW1lPWFkdmFuY2VkU2VhcmNoJndpZGdldFZpZXc9Y29sdW1uJmFqYXhjYWxsPXllcyZzZWFyY2hCeT13ZWVrJm1pbkRhdGU9MDEtMTAtMjAxMyZtYXhEYXRlPWN1cnJEYXRlQW5kSG91ciZzdGFydEluZGV4PTA='
base = 'aHR0cDovL2lsLnNyZ3Nzci5jaC9pbnRlZ3JhdGlvbmxheWVyLzEuMC91ZS9yc2kvdmlkZW8vcGxheS8='
token_url = 'aHR0cDovL3RwLnNyZ3Nzci5jaC9ha2FoZC90b2tlbj9hY2w9JTJGaSUyRnJzaSUyRio='
#live_token = 'aHR0cDovL3RwLnNyZ3Nzci5jaC9ha2FoZC90b2tlbj9hY2w9JTJGaSUyRmVuYzExdW5pX2NoJTQwMTkxNDU1JTJGKg=='
artbase = 'special://home/addons/plugin.video.rsi-telegiornale/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.rsi-telegiornale')
self = xbmcaddon.Addon(id='plugin.video.rsi-telegiornale')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.rsi-telegiornale")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "RSI - Telegiornale"

defaultimage = 'special://home/addons/plugin.video.rsi-telegiornale/icon.png'
defaultfanart = 'special://home/addons/plugin.video.rsi-telegiornale/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.rsi-telegiornale/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.rsi-telegiornale').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#p = settings.getSetting(id="parser")
#e = settings.getSetting(id="encoding")
confluence_views = [500,501,502,503,504,508,515]


#533
def sites():
        addDir('Telegiornale', 'http://www.rsi.ch/la1/programmi/informazione/telegiornale', 633, defaultimage)
        #addDir('Edizioni', 'http://www.rsi.ch/la1/programmi/informazione/telegiornale/', 633, defaultimage)
        addDir('Scelti Per Voi', 'http://www.rsi.ch/la1/programmi/informazione/telegiornale/scelti-per-voi/', 634, defaultimage)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


#633
def edizioni(url):
	response = get_html(url)
	titles = re.compile('data-widget-title="(.+?)"').findall(response)
	subs = re.compile('data-widget-subtitle="(.+?)"').findall(response)
	video_ids = re.compile('data-widget-video-id="(.+?)"').findall(response)
	#images = re.compile('data-widget-imageUrl="(.+?)"').findall(response)
	items = zip(titles, subs, video_ids)
	for title, sub, video_id in items:
	    title = (title + ' - ' + sub).replace('&#039;', '\'').replace('&amp;', '&')
	    jurl = base.decode('base64') + video_id + '.json'
	    add_directory2(title,jurl,40,defaultfanart,defaultimage,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)


#634
def videos(url):
	response = get_html(url)
	titles = re.compile('data-video-title="(.+?)"').findall(response)
	video_ids = re.compile('data-widget-video-id = "(.+?)"').findall(response)
	#images = re.compile('<img src="(.+?)"').findall(response)[1:22]
	#print len(images)
	items = zip(titles, video_ids)
	for title, video_id in items:
	    title = title.replace('&#039;', '\'').replace('&amp;', '&')
	    jurl = base.decode('base64') + video_id + '.json'
	    add_directory2(title,jurl,40,defaultfanart,defaultimage,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)


#40
def streams(name,url):
	response = urllib2.urlopen(url)
        jdata = json.load(response)
	stream = jdata['Video']['Playlists']['Playlist'][1]['url'][0]['text']
	key = jdata['Video']['AssetSet']['title']
	print key
	t_url = token_url.decode('base64')
	tresponse = urllib2.urlopen(t_url)
        tdata = json.load(tresponse) 
	token = tdata['token']['authparams']
	url = stream + '?' + token
	thumbnail = defaultimage
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
        listitem.setProperty('mimetype', 'video/mp4')
	listitem.addStreamInfo('video', { 'title': name })
	xbmc.Player().play( url, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


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

def add_directory2(name,url,mode,fanart,thumbnail,plot,showcontext=False):
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

def addLink(name, url, mode, iconimage, fanart=False, infoLabels=True):
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
        print "RSI - Telegiornale"
	sites()
elif mode==633:
        print "RSI - Telegiornale Edizioni"
	edizioni(url)
elif mode==634:
        print "RSI - Telegiornale Videos"
	videos(url)
elif mode==40:
        print "RSI - Telegiornale Streams"
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
