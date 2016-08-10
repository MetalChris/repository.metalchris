#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from BeautifulSoup import BeautifulStoneSoup as Soup
import HTMLParser
import simplejson as json
import xml.etree.ElementTree as ET
from lxml import html


apiURL = 'http://www.omdbapi.com/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.fright-pix')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.fright-pix")
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]

defaultimage = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
defaultfanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
#defaultvideo = 'special://home/addons/plugin.video.fright-pix/icon.png'
#defaulticon = 'special://home/addons/plugin.video.fright-pix/icon.png'
fanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
icon = 'special://home/addons/plugin.video.fright-pix/icon.png'

def get_genres(url):
        addon_handle = int(sys.argv[1])
        html = get_html('http://www.frightpix.com/')
        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
        i = 1
        for gurl,name in match:
            if not 'movies' in gurl:
                continue
            gurl = 'http://www.frightpix.com' + str(gurl)
            i = i + 1
            if i < 18:
                add_directory2(name,gurl,1, fanart, 'DefaultMovies.png',plot='')
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")



def INDEX(url):

        addon_handle = int(sys.argv[1])
        html = get_html(url)
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)"').findall(html)  
        items = int(len(match))/2
        i = 0
        for purl,image in match:
            name = re.compile('/(.+?)/').findall(purl)[0]
            if '%20' in name:
                name = name.replace('%20', ' ')
            elif '-' in name:
                name = name.replace('-', ' ')
                name = name.title()
            else:
                name = name.capitalize()
            print name            
            purl = 'http://www.frightpix.com' + str(purl)
            page = get_html(purl)
            plot = Soup(page)
            plot = str(plot.find('dd', attrs={'itemprop': 'description'}))[27:-5]
            plot = plot.strip()
            try: vurl = re.compile('data-videosrc="(.+?)"').findall(page)[0]
            except:
                items = items - 1
                continue
            print plot
            infoLabels = {'title':name,
                          'tvshowtitle':name,
                          'plot':plot}
            i = i + 1
            if i <= items:
                li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                li.setProperty('fanart_image', defaultfanart)
                li.setInfo(type="Video", infoLabels=infoLabels)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=vurl, listitem=li, totalItems=50)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)



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
    print "Indexing Genres"
    get_genres(url)
elif mode == 1:
    print "Indexing Videos"
    INDEX(url)
elif mode == 2:
	print "Indexing Replay by Sport"
	REPLAYBYSPORT(url)
elif mode == 4:
    print "Play Video"

elif mode == 20:
    print "Indexing Genres"
    get_genres(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


