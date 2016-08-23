#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests  
import urlparse
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
#from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
from cookielib import CookieJar


artbase = 'special://home/addons/plugin.audio.radionomy/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.audio.radionomy')
self = xbmcaddon.Addon(id='plugin.audio.radionomy')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.audio.radionomy")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Radionomy"

defaultimage = 'special://home/addons/plugin.audio.radionomy/icon.png'
defaultfanart = ''
defaulticon = 'special://home/addons/plugin.audio.radionomy/icon.png'
headers = {
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'X-Requested-With':'XMLHttpRequest',
}

local_string = xbmcaddon.Addon(id='plugin.audio.radionomy').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


def r_genres():

	r = requests.get('https://www.radionomy.com/en/style')
	print r.cookies
        print 'Kookie= ' + str(r.cookies)[54:-72]
	kookie = str(r.cookies)[54:-72]
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', kookie))
	f = opener.open('https://www.radionomy.com/en/style')
        page = f.read()
        match = re.compile('<option data-style-id="(.+?)</option>').findall(page)
        match = str(match)
        rematch = re.compile('href="(.+?)"').findall(match)
	for url in rematch[2:17]:
            title = url.split('/',3)[-1].title()
            url = 'https://www.radionomy.com' + str(url)
            add_directory2(title,url,131, defaultfanart ,defaultimage,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#131
def r_sub_genres(url):

	r = requests.get(url)
	print r.cookies
	kookie1 = r.cookies
	print ' Kookie1= ' + str(kookie1)
        print 'Kookie= ' + str(r.cookies)[54:-72]
	kookie = str(r.cookies)[54:-72]
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', kookie))
	f = opener.open(url)
        page = f.read()
        soup = BeautifulSoup(page,'html.parser')
        for item in soup.find_all(attrs={'id': 'browseSubGenre'}):
            for link in item.find_all('a'):
                l = link.get('href')
                url = 'https://www.radionomy.com' + str(l).replace(' ', '%20')
                title = url.split('/',6)[-1].title().replace('%20', ' ')
                add_directory2(title,url,132, defaultfanart ,defaultimage,plot='')
                xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#132
def r_sub2_genres(url):

	r = requests.get(url)
	print r.cookies
	kookie1 = r.cookies
	print ' Kookie1= ' + str(kookie1)
        print 'Kookie= ' + str(r.cookies)[54:-72]
	kookie = str(r.cookies)[54:-72]
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', kookie))
	f = opener.open(url)
        page = f.read()
	match = re.compile('href="(.+?)" rel="internal"><img class="radioCover" src="(.+?)" alt="(.+?)" ').findall(page)
        for url,image,title in match:
	    url = str(url).replace('/en/radio', 'http://listen.radionomy.com').replace('/index', '.m3u')
            h = HTMLParser.HTMLParser()
            try: title = h.unescape(title)	  
	    except UnicodeDecodeError:
		continue  
	    image = image.replace('s67.jpg', 's400.jpg')
	    #r = requests.get(url)
	    #opener = urllib2.build_opener()
	    #f = opener.open(url)
            #page = f.read()
	    # page = get_html(url)
	    # stream = re.compile('http(.+?)$').findall(page)[0]
            #print 'Stream= ' + str(stream)
	    # stream = stream.replace('\r', '')
            # print 'Stream URL= ' + 'https' + str(stream)
            # url = 'https' + str(stream)
	    #url = ''
            #li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            #li.setProperty('IsPlayable', 'true')      
	    #print 'SubGenre2URL= ' + str(url)
            try: add_directory3(title,url,133, defaultfanart ,image,plot='')
	    except KeyError:
	        continue
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=30)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#133
def r_play_url(url):
    
	print 'SubGenre2URL= ' + str(url)
	#page = get_html(url)
	#stream = re.compile('http(.+?)$').findall(page)[0]
            #print 'Stream= ' + str(stream)
	#stream = stream.replace('\r', '')
        #print 'Stream URL= ' + 'https' + str(stream)
        #url = 'https' + str(stream)
	#print 'PlayURL= ' + str(url)
	#xbmc.executebuiltin("PlayWith('PAPLAYER')")
	#xbmc.executebuiltin( "PlayMedia(url)" )
	#{"jsonrpc":"2.0","id":1,"method":"Player.Open","params":{"item":{"file":"url"}}}
	xbmc.Player().play( url )

def add_directory2(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=100)
        return ok


def add_directory3(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=100)
        return ok

def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')

    try:
        response = urllib2.urlopen(req, timeout = 60)
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
        print "Radionomy Genres"
	r_genres()
elif mode==131:
        print "Radionomy Sub Genres"
	r_sub_genres(url)
elif mode==132:
        print "Radionomy Sub2 Genres"
	r_sub2_genres(url)
elif mode==133:
        print "Radionomy PlayURL"
	r_play_url(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
