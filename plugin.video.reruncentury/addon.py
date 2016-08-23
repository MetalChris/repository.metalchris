#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmc, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
import HTMLParser

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.reruncentury')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')

#defaultvideo = 'special://home/addons/plugin.video.nhl-rewind/icon.png'
#defaulticon = 'special://home/addons/plugin.video.nhl-rewind/icon.png'
defaultfanart=''



def CATEGORIES():
        mode = 1


        addDir('Top Shows (More than 40 Episodes)', 'http://www.reruncentury.com/', 2, '')
        addDir('More Shows (More than 10 Episodes)', 'http://www.reruncentury.com/', 5, '')
        addDir('All Shows (Alphabetical)', 'http://www.reruncentury.com/ia/', 3, '')


def top_shows(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        match=re.compile('<dd><a href="(.+?)"><img align=middle width=144 height=99 hspace=12 src="(.+?)">(.+?)</a>').findall(html)
        for url,thumbnail,name in match: 
            print 'name=' + name
            print 'purl=' + str(url)
            addDir(name, url,6,thumbnail)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def all_shows(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        shows = re.compile ('<dd><a href="(.+?)">(.+?)</a>').findall(html)
        for url, name in shows:
            url = 'http://www.reruncentury.com' + str(url)
            addDir(name, url,6,'')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
            
def more_shows(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        shows = re.compile ('<br><a href="(.+?)">(.+?)</a>').findall(html)
        for url, name in shows:
            url = 'http://www.reruncentury.com' + str(url)
            addDir(name, url,6,'')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def get_episodes(url):
        addon_handle = int(sys.argv[1])

        page = get_html(url)
        episodes = re.compile('<a href="(.+?)"><nobr>(.+?)</n').findall(page)
        print 'episodes=' + str(episodes)
        for purl, name in episodes:
            print 'name=' + name
            print 'purl=' + purl
            purl = str(purl)
            page = get_html(purl)
            image = str(re.compile('poster="(.+?)"').findall(page))[2:-2]
            streamUrl = str(re.compile('<source src="(.+?)" type="video/mp4').findall(page))[2:-2]
            print 'image=' + str(image)
            print 'streamUrl=' + str(streamUrl)
            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=100)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
elif mode == 2:
	print "Indexing Top Shows"
	top_shows(url)
elif mode == 3:
	print "Get All Shows"
	all_shows(url)
elif mode == 4:
    print "Play Video"
elif mode == 5:
	print "Get More Shows"
	more_shows(url)
elif mode == 6:
	print "Get Episodes"
	get_episodes(url)
elif mode == 7:
	print "Indexing by Season"
	tnd_seasons(url)
elif mode == 8:
	print "Get Items by Season"
	get_tnd_seasons(url)
elif mode == 9:
	print "Indexing by Season"
	ff_seasons(url)
elif mode == 10:
	print "Get Items by Season"
	get_ff_seasons(url)

elif mode==20:
        print "Genres"
        movie_genres(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
