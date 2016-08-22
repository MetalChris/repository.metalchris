#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import simplejson as json

artbase = 'special://home/addons/plugin.video.bigstar/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.bigstar')
self = xbmcaddon.Addon(id='plugin.video.bigstar')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.bigstar")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "BigStar Movies"

defaultimage = 'special://home/addons/plugin.video.bigstar/icon.png'
defaultfanart = 'special://home/addons/plugin.video.bigstar/fanart.jpg'
fanart = 'special://home/addons/plugin.video.bigstar/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.bigstar/icon.png'

local_string = xbmcaddon.Addon(id='plugin.video.bigstar').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


def CATEGORIES():
    mode = 1

    addDir('Recently Added', 'http://www.bigstar.tv/mobile/movies/genre/recently-added/page/1/limit/60/os/web/device', 139,
           defaultimage)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#140
def bigstar_genres(url):

        add_directory2('Search','http://www.bigstar.tv/mobile/movies/q/', 144, defaultfanart ,defaultimage,plot='')
        response = urllib2.urlopen('http://www.bigstar.tv/mobile/genres/os/web/device/undefined')
        jgdata = json.load(response) 
	for item in jgdata["items"]:
            title = item["name"]
	    genre = item["url"]
	    url = 'http://www.bigstar.tv/mobile/movies/genre/' + str(genre) + '/page/1/limit/30/os/web/device'
	    if 'TV Episodes' in title:
		mode = 142
	    else:
		mode = 141
            add_directory2(title,url,mode, defaultfanart ,defaultimage,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#141
def bigstar_movies(url):
	print 'URL= ' + str(url)
	page = re.compile('page/(.+?)/limit').findall(url)[0]
	page = int(page) + 1
        response = urllib2.urlopen(url)
        jgdata = json.load(response) 
	for item in jgdata["films"]:
            title = item["title"]
	    image = item["cover_large"]
	    fanart = item["imageUrl1"]
	    desc = item["desc"]
	    tv = str(item["hasEpisodes"])
	    print 'TV= ' + str(tv)
	    if 'True' in tv:
		continue
            infoLabels = {'title':title,
                         'tvshowtitle':title,
                         'plot':desc}
	    streamkeys = image.split('/')
	    key1 = streamkeys[7]
	    key2 = streamkeys[-1].split('_')[0]
	    streamurl = 'http://bigstar-vh.akamaihd.net/i/smil/studio/' + str(key1) + '/stream/' + str(key2) + '_web_ads_wifi.smil/index_1500000_av.m3u8?null='
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setInfo(type="Video", infoLabels=infoLabels)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li, totalItems=60)
            xbmcplugin.setContent(pluginhandle, 'episodes')
	next = url.rsplit('/', 6)[0]
	next = str(next) + '/' + str(page) + '/limit/30/os/web/device'
        add_directory2('Next Page>>', next,141, defaultfanart , artbase + 'big-star.png',plot='')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)

	
#142
def bigstar_tv(url):

        add_directory2('Search','http://www.bigstar.tv/mobile/movies/q/', 145, defaultfanart ,defaultimage,plot='')
	print 'URL= ' + str(url)
	page = re.compile('page/(.+?)/limit').findall(url)[0]
	page = int(page) + 1
	next = url.rsplit('/', 6)[0]
	next = str(next) + '/' + str(page) + '/limit/30/os/web/device'
        response = urllib2.urlopen(url)
        jgdata = json.load(response) 
	for item in jgdata["films"]:
            title = item["title"]
	    image = item["cover_large"]
	    desc = item["desc"]
	    plot = desc
	    show = item["id"]
	    url = 'http://www.bigstar.tv/mobile/movies/boxset/' + str(show) + '/os/web/device'
            infoLabels = {'title':title,
                         'tvshowtitle':title,
                         'plot':desc}
            add_directory2(title, url,143, defaultfanart , image,plot)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        add_directory2('Next Page>>', next,142, defaultfanart , artbase + 'big-star.png',plot='')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)	


#143
def bigstar_episodes(url):
	
	print 'Episode URL= ' + str(url)
        response = urllib2.urlopen(url)
        jgdata = json.load(response) 
	for item in jgdata["films"]:
            title = item["title"]
	    image = item["cover_large"]
	    fanart = item["imageUrl1"]
	    desc = item["desc"]
            infoLabels = {'title':title,
                         'tvshowtitle':title,
                         'plot':desc}
	    streamkeys = image.split('/')
	    key1 = streamkeys[7]
	    key2 = streamkeys[-1].split('_')[0]
	    streamurl = 'http://bigstar-vh.akamaihd.net/i/smil/studio/' + str(key1) + '/stream/' + str(key2) + '_web_ads_wifi.smil/index_1500000_av.m3u8?null='
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setInfo(type="Video", infoLabels=infoLabels)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li, totalItems=30)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)	


#144
def bigstar_search(url):

        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            print 'search= ' + search
            url = url + search
	    print url
        response = urllib2.urlopen(url)
        jgdata = json.load(response) 
	for item in jgdata["films"]:
            title = item["title"]
	    image = item["cover_large"]
	    fanart = item["imageUrl1"]
	    desc = item["desc"]
	    tv = str(item["hasEpisodes"])
	    print 'TV= ' + str(tv)
	    if 'True' in tv:
		continue
            infoLabels = {'title':title,
                         'tvshowtitle':title,
                         'plot':desc}
	    streamkeys = image.split('/')
	    key1 = streamkeys[7]
	    key2 = streamkeys[-1].split('_')[0]
	    streamurl = 'http://bigstar-vh.akamaihd.net/i/smil/studio/' + str(key1) + '/stream/' + str(key2) + '_web_ads_wifi.smil/index_1500000_av.m3u8?null='
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setInfo(type="Video", infoLabels=infoLabels)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li, totalItems=60)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#145
def bigstar_tvsearch(url):

        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            print 'search= ' + search
            url = url + search
	    print url
        response = urllib2.urlopen(url)
        jgdata = json.load(response) 
	for item in jgdata["films"]:
            title = item["title"]
	    image = item["cover_large"]
	    desc = item["desc"]
	    tv = str(item["hasEpisodes"])
	    print 'TV= ' + str(tv)
	    if 'False' in tv:
		continue
	    plot = desc
	    show = item["id"]
	    url = 'http://www.bigstar.tv/mobile/movies/boxset/' + str(show) + '/os/web/device'
            infoLabels = {'title':title,
                         'tvshowtitle':title,
                         'plot':desc}
            add_directory2(title, url,143, defaultfanart , image,plot)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)	


def sanitize(data):
    output = ''
    for i in data:
        for current in i:
            if ((current >= '\x20') and (current <= '\xD7FF')) or ((current >= '\xE000') and (current <= '\xFFFD')) or ((current >= '\x10000') and (current <= '\x10FFFF')):
               output = output + current
    return output

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
        return ok

def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Roku/DVP-4.3 (024.03E01057A), Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

    try:
        response = urllib2.urlopen(req, timeout=60)
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
	bigstar_genres(url)
elif mode == 1:
        print "Indexing Videos"
        INDEX(url)
elif mode == 4:
        print "Play Video"
elif mode==140:
        print "BigStar Genres"
	bigstar_genres(url)
elif mode==141:
        print "BigStar Movies"
	bigstar_movies(url)
elif mode==142:
        print "BigStar TV"
	bigstar_tv(url)
elif mode==143:
        print "BigStar Episodes"
	bigstar_episodes(url)
elif mode == 144:
        print "BigStar Search"
        bigstar_search(url)
elif mode == 145:
        print "BigStar TV Search"
        bigstar_tvsearch(url)





xbmcplugin.endOfDirectory(int(sys.argv[1]))
