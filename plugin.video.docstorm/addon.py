#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import simplejson as json
import requests  
import urlparse
import HTMLParser
import codecs
from lxml import etree
from urllib import urlopen
import socket

youtube = 'youtube'
vimeo = 'vimeo'
apiURL = 'http://www.omdbapi.com/'
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

defaultimage = ''
defaultfanart = ''
#defaultvideo = 'special://home/addons/plugin.video.docstorm/icon.png'
defaulticon = 'special://home/addons/plugin.video.docstorm/icon.png'
#fanart = 'special://home/addons/plugin.video.docstorm/fanart.jpg'
back = ''


local_string = xbmcaddon.Addon(id='plugin.video.docstorm').getLocalizedString

pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]

def CATEGORIES():
    mode = 1

    addon_handle = int(sys.argv[1])
    html = get_html('http://documentarystorm.com/')
    match=re.compile('category/(.+?)/" title="').findall(html)
    print match
    for name in match:
        url = 'http://documentarystorm.com/category/' + str(name)
        name = name.title()
        add_directory2(name,url,10, back, back,plot='')
        #xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
    xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
    #xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#def INDEX(url):

def get_movies(url):
        mode = 1

        addon_handle = int(sys.argv[1])
        html = get_html(url)
        nextpage = re.compile('"next" href="(.+?)"').findall(html)[0]
        html_parser = HTMLParser.HTMLParser()
        match = re.compile('<a href="(.+?)" data').findall(html)
        for purl in match: 
            if '=' in purl:
                continue
            page = get_html(purl)
            match = re.compile('<img src="(.+?)" alt="(.+?)"').findall(page)            
            for image, name in match:
                name = name.replace('&#038;', '&')
                name = name.replace('&#8211;', '-')
                name = name.replace('&#8217;', '\'')
                try:description = re.compile('"description" content="(.+?)"').findall(page)[-1]
                except IndexError:
                    description = 'No description available'
                try:description = html_parser.unescape(description)
                except UnicodeDecodeError:
                    description = 'No description available'
                print description
                iframe = str(re.compile('<iframe(.+?)</iframe>').findall(page))
                iframe = str(re.compile('src="(.+?)"').findall(iframe))
                iframe = str(iframe)
                if 'snagfilms' not in str(iframe) and 'list' not in str(iframe):
                    iframe = str(iframe.split('?', 1)[0])
                    iframe = str(iframe.split('/', 4)[-1])
                if 'list' in str(iframe):
                    videoId = str(iframe.split('/', 4)[-1])[:-2]
                    streamUrl = ('plugin://plugin.video.youtube/play/?video_id=' + videoId)
                    print streamUrl                 
                elif len(str(iframe)) == 13:
                    videoId = str(iframe)[0:-2]
                    streamUrl = ('plugin://plugin.video.youtube/play/?video_id=' + videoId)
                elif len(str(iframe)) == 8 or len(str(iframe)) == 9:
                    vframe = 'http://player.vimeo.com/video/' + str(iframe)
                    vimeo = get_html(vframe)
                    vimeoUrl = str(re.compile('"url":"(.+?)"').findall(vimeo)[0])
                    streamUrl = vimeoUrl
                elif len(str(iframe)) > 13 and 'snagfilms' in str(iframe):
                    iframe = str(iframe)[2:-2]
                    snag = get_html(iframe)
                    try:streamUrl = re.compile('file: "(.+?)"').findall(snag)[-1]
                    except IndexError:
                        streamUrl = ('plugin://plugin.video.youtube/play/?video_id=9sZaxvpEmDY')
                else:
                    streamUrl=('plugin://plugin.video.youtube/play/?video_id=9sZaxvpEmDY')
                infoLabels = {'title':name,
                              'tvshowtitle':name,
                              'plot':description}
            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            li.setProperty('IsPlayable', 'true')      
            li.setInfo(type="Video", infoLabels=infoLabels)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=24)
        url = str(nextpage)
        add_directory2('Next Page',url,10,back,back,plot='')
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
elif mode == 10:
    print "Indexing Videos"
    get_movies(url)
elif mode == 20:
    print "Indexing Genres"
    get_genres(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


