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
import html5lib

live = 'aHR0cDovL29veWFsYWhkMi1mLmFrYW1haWhkLm5ldC9pL25ld3NtYXgwMl9kZWxpdmVyeUAxMTk1NjgvbWFzdGVyLm0zdTg/aGRjb3JlPTIuMTAuMyZnPVdVVFlWRlNWSUVVWQ=='
pre = 'aHR0cDovL3BsYXllci5vb3lhbGEuY29tL3Nhcy9wbGF5ZXJfYXBpL3YxL2F1dGhvcml6YXRpb24vZW1iZWRfY29kZS9Ka2NXczZ2NTNsc1JkR2Z3bENTd2dfYTVDVU12Lw=='
post = 'P2RldmljZT1odG1sNSZkb21haW49d3d3Lm5ld3NtYXh0di5jb20mc3VwcG9ydGVkRm9ybWF0cz1tcDQlMkN3ZWJt'
getv = 'aHR0cDovL3d3dy5uZXdzbWF4dHYuY29tL29veWFsYXNlcnZpY2Uuc3ZjL2dldHBvcHVsYXJ2aWRlb3M/dHlwZT0='
artbase = 'special://home/addons/plugin.video.newsmax/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.newsmax')
self = xbmcaddon.Addon(id='plugin.video.newsmax')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.newsmax")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
#confluence_views = [500,501,502,503,504,508]

plugin = "Newsmax TV"

defaultimage = 'special://home/addons/plugin.video.newsmax/icon.png'
defaultfanart = 'special://home/addons/plugin.video.newsmax/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.newsmax/icon.png'
baseurl = 'http://www.newsmaxtv.com'

local_string = xbmcaddon.Addon(id='plugin.video.newsmax').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#10
def index():
        addDir2('Live', live.decode('base64'), 4, defaultimage)
        addDir('Shows', 'http://www.newsmaxtv.com/shows/', 15, defaultimage)
        addDir('Popular', getv.decode('base64'), 25, defaultimage)
        addDir('Trending', getv.decode('base64'), 25, defaultimage)
        xbmcplugin.endOfDirectory(addon_handle)


#15
def shows(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('div',{'class':'col-md-9'})[1:17]
	images = BeautifulSoup(response,'html5lib').find_all('img',{'class':'img-responsive'})
	for item, image in zip(soup, images):
	    title = item.find('h1').string.encode('utf-8')
	    url = baseurl + str(item.find('a')['href'])
	    add_directory2(title,url,20,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('h6')[1:31]
	for item in soup:
	    title = (str(item.find('a').text.encode('utf-8')).strip()).split(' | ')[-1]
	    url = baseurl + str(item.find('a')['href'])
	    video_id = url.rsplit('/')[-1]
	    json = pre.decode('base64') + video_id + post.decode('base64')
	    add_directory(title,json,30,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#25
def get(name,url):
	name = name.lower()
	url = url + name
	response = get_html(url)
	response = striphtml(response)
	response = response.replace('\\','')
	names = re.compile('name":"(.+?)"').findall(response)
	embeds = re.compile('embed_code":"(.+?)"').findall(response)
	for title, video_id in zip(names, embeds):
	    title = (title)
	    url = baseurl 
	    json = pre.decode('base64') + video_id + post.decode('base64')
	    print 'Newsmax JSON: ' + str(json)
	    add_directory(title,json,30,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	response = get_html(url)
	url = (re.compile('data":"(.+?)"').findall(str(response))[-1]).decode('base64')
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
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=30)
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=30)
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

def addDir2(name, url, mode, iconimage, fanart=True, infoLabels=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty('IsPlayable', 'true')
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image', artbase + 'fanart2.jpg')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok

def addDir(name,url,mode,iconimage, fanart=False, infoLabels=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
    print "Main Menu"
    index()
elif mode == 4:
    print "Play Video"
    play(url)
elif mode==15:
        print "Newsmax Shows"
	shows(url)
elif mode==20:
        print "Newsmax Videos"
	videos(url)
elif mode==25:
        print "Newsmax Get Videos"
	get(name,url)
elif mode==30:
        print "Newsmax Streams"
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
