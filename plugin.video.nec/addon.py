#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests  
import urlparse
import HTMLParser
from urllib import urlopen


_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.nec')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.nec")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Public Domain Video"

defaultimage = 'special://home/addons/plugin.video.nec/icon.png'
defaultfanart = ''
defaulticon = 'special://home/addons/plugin.video.nec/icon.png'
nec = 'special://home/addons/plugin.video.nec/nec.png'

local_string = xbmcaddon.Addon(id='plugin.video.nec').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]

def CATEGORIES():
    mode = 1

    addDir('Archived Events', 'http://necfrontrow.com/fullevent.php', 39, nec)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def nec_sports(url,name):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        match=re.compile('<li><a href=\'(.+?)\'><span>(.+?)</').findall(html)
        for url,sport in match:
            if 'ondemand' in url:
                title = sport
                #if '&#8211;' in name:
                #title = title.replace('&#8211;', '-')
                #title = title.replace('&#8217;', '\'')
                title = title.replace('&amp;', '&')
                url = url.replace('ondemand', 'fullevent')
                url = 'http://necfrontrow.com/' + url
                #print 'NEC url= ' + str(url)
                add_directory2(title,url,40, nec,nec,plot='')
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")
        #xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def nec_events(url,name):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        match=re.compile('<td>\n(.+?)</td>\n<td><a href="(.+?)"').findall(html)
        i = 0
        for event,url in match:
            title = event.lstrip()
            title = title.replace('&#039;', '\'')
            if 'Hit-A-Thon' in title:
                continue
            url = 'http://necfrontrow.com' + url
            #print 'NEC url= ' + str(url)


            #li = xbmcgui.ListItem(title, iconImage=defaultimage, thumbnailImage=defaultimage)
            #li.setProperty('fanart_image', defaultfanart)
            #li.setInfo(type="Video", infoLabels=infoLabels)
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=stream, listitem=li, totalItems=100)

            add_directory2(title,url,41, nec,nec,plot='')
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")
        #xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def nec_stream(url,name):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        match=re.compile('<iframe src="(.+?)" width').findall(html)[0]
        iframe = match
        #print 'NEC iframe= ' + str(iframe)
        html = get_html(iframe)
        key = re.compile('live_video_post_id":(.+?),"').findall(html)[0]
        print 'Key= ' + str(key)
        match=re.compile('m3u8_url":"(.+?)",').findall(html)
        i=1
        h=1
        for url in match:
            print 'NEC Stream= ' + str(url)
            if key in url:
                title = 'Event Stream' + str(i)
                i=i+1
            else:
                title = 'Highlight' + str(h)
                h=h+1
        #item = xbmcgui.ListItem(path=url)
        #return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            li = xbmcgui.ListItem(title, iconImage=nec, thumbnailImage=nec)
        #li.setProperty('fanart_image', defaultfanart)
        #li.setInfo(type="Video", infoLabels=infoLabels)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)

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
	#if url['mode']:
		#u = sys.argv[0] + '?' + urllib.urlencode(url)
	#else:
        p = 1
        p = p+1
        nexturl = 'http://www.flixhouse.com/movie-genre/free/' + 'page/' + str(p) +'/'
	u = nexturl
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = isFolder)
	return ok

def addLink(name, url, mode, iconimage, fanart=False, infoLabels=True):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    if not fanart:
        fanart=defaultfanart
    liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=False)
    return ok

def add_item( action="" , title="" , plot="" , url="" ,thumbnail="" , folder=True ):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] folder=["+str(folder)+"]")

    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
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
    atoz(url,name)
elif mode == 39:
    print "Indexing NEC Sports"
    nec_sports(url,name)
elif mode == 40:
    print "Indexing NEC Events"
    nec_events(url,name)
elif mode == 41:
    print "Get NEC Stream"
    nec_stream(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
