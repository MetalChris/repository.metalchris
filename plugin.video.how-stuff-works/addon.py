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


artbase = 'special://home/addons/plugin.video.how-stuff-works/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.how-stuff-works')
self = xbmcaddon.Addon(id='plugin.video.how-stuff-works')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.how-stuff-works")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "How Stuff Works"

defaultimage = 'special://home/addons/plugin.video.how-stuff-works/icon.png'
defaultfanart = 'special://home/addons/plugin.video.how-stuff-works/how-min.jpg'
defaulticon = 'special://home/addons/plugin.video.how-stuff-works/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.how-stuff-works').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]




#634
def shows_how_stuff_works(url):
	response = get_html('http://shows.howstuffworks.com')
        add_directory2('Most Watched', 'http://www.howstuffworks.com/videos', 638, defaultfanart, artbase + 'hsw.png', plot='')
        add_directory2('Recently Added', 'http://www.howstuffworks.com/videos', 638, defaultfanart, artbase + 'hsw.png', plot='')
	soup = BeautifulSoup(response, 'html.parser')
	for show in soup.find_all("div",{"class":"pull-left"})[2:14]:
	    title = show.find('img')['alt']
	    url = show.find('a')['href']
	    if not '.htm' in url:
		url = url + 'video'
	    if 'history' in url or 'techstuff' in url:
		continue
	    if '.htm' in url:
	        mode = 639
	    else:
	        mode = 637
            add_directory2(title, url, mode, defaultfanart, artbase + 'hsw.png', plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#635
def how_stuff_works(url):
	response = get_html(url)
	soup = BeautifulSoup(response, 'html.parser').find_all("div",{"class":"sidebar col-sm-3 hidden-xs"})[0]
	for show in soup.find_all("div",{"class":"img-container"}):
	    title = show.find('img')['title']
	    url = show.find('a')['href']
	    image = show.find('img')['data-src']
            add_directory2(title, url, 636, defaultfanart, artbase + 'hsw.png', plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)

#636
def hsw_videos(url):
	response = get_html(url)
	titles = re.compile('clip_title      :(.+?)\',').findall(response)
	item = 0
	for title in titles:
	    title = title.split(': ')[-1].replace("&#039;","'").replace('&amp;','&').replace('&quot;','"').lstrip(" '")
	    try: m3u8 = re.compile('m3u8            : \'(.+?)\'').findall(response)[item]
	    except IndexError:
		continue
	    duration = re.compile('duration        \: (.+?),').findall(response)[item]
	    image = re.compile('thumbnail_url   : \'(.+?)\',').findall(response)[item]
	    mp4 = re.compile(' "(.+?)"},]').findall(response)[item];mp4 = mp4.split('"src": "')
	    med = re.compile(' "(.+?)"},]').findall(response)[item];med = med.split('"src": "')
	    item = item + 1
	    if QUALITY =='2':
	        url = mp4[-1]
	    elif QUALITY =='1':
	        url = med[-2].split('"')[0]
	    elif QUALITY =='0':
	        url = m3u8
	    item = item + 1
            li = xbmcgui.ListItem(title, iconImage= artbase + 'hsw.png', thumbnailImage= artbase + 'hsw.png')
            li.setProperty('fanart_image',  defaultfanart) 
	    li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#637
def hsw_video(url):
	response = get_html(url)
	titles = re.compile('clip_title: "(.+?)",').findall(response)
	item = 0
	for title in titles:
	    title = title.split(': ')[-1].replace("&#039;","'").replace('&amp;','&').replace('&quot;','"').replace('\\u00c9','').lstrip(" '")
	    m3u8 = re.compile('m3u8: \'(.+?)\'').findall(response)[item]
	    mp4 = re.compile(' "(.+?)"},]').findall(response)[item];mp4 = mp4.split('"src": "')
	    med = re.compile(' "(.+?)"},]').findall(response)[item];med = med.split('"src": "')
	    duration = re.compile('duration: (.+?),').findall(response)[item]
	    item = item + 1
	    if QUALITY =='2':
	        url = mp4[-1]
	    elif QUALITY =='1':
	        url = med[-2].split('"')[0]
	    elif QUALITY =='0':
	        url = m3u8
            li = xbmcgui.ListItem(title, iconImage= artbase + 'hsw.png', thumbnailImage= artbase + 'hsw.png')
            li.setProperty('fanart_image',  defaultfanart)
	    li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#638
def most_watched(name,url):
	response = get_html(url)
	if name == 'Most Watched':
	    soup = BeautifulSoup(response, 'html.parser').find_all("div",{"class":"module module-multi module-grid most-watched"})[0]
	else:
	    soup = BeautifulSoup(response, 'html.parser').find_all("div",{"class":"module module-multi module-grid all-videos"})[0]	
	for video in soup.find_all("p",{"class":"h4"}):
	    title = video.find('a').contents[0]
	    url = video.find('a')['href']#; title = striphtml(url)
            try: add_directory2(title, url, 636, defaultfanart, artbase + 'hsw.png', plot='')
	    except KeyError:
		continue
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)
	

#639
def more_shows(name,url):
        add_directory2('Most Watched', 'http://shows.howstuffworks.com/more-shows/more-shows-videos.htm', 638, defaultfanart, artbase + 'hsw.png', plot='')
        add_directory2('Recently Added', 'http://shows.howstuffworks.com/more-shows/more-shows-videos.htm', 638, defaultfanart, artbase + 'hsw.png', plot='')
	response = get_html(url)
	titles = re.compile('clip_title      :(.+?)\',').findall(response)
	item = 0
	for title in titles:
	    title = title.split(': ')[-1].replace("&#039;","'").replace('&amp;','&').replace('&quot;','"').lstrip(" '")
	    try: m3u8 = re.compile('m3u8            : \'(.+?)\'').findall(response)[item]
	    except IndexError:
		continue
	    image = re.compile('thumbnail_url   : \'(.+?)\',').findall(response)[item]
	    mp4 = re.compile(' "(.+?)"},]').findall(response)[item];mp4 = mp4.split('"src": "')
	    med = re.compile(' "(.+?)"},]').findall(response)[item];med = med.split('"src": "')
	    item = item + 1
	    if QUALITY =='2':
	        url = mp4[-1]
	    elif QUALITY =='1':
	        url = med[-2].split('"')[0]
	    elif QUALITY =='0':
	        url = m3u8
	    item = item + 1
            li = xbmcgui.ListItem(title, iconImage= artbase + 'hsw.png', thumbnailImage= artbase + 'hsw.png')
            li.setProperty('fanart_image',  defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)
	

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
    shows_how_stuff_works(url)
elif mode == 4:
    print "Play Video"
elif mode==634:
        print "How Stuff Works Shows"
	shows_how_stuff_works(url)
elif mode==635:
        print "How Stuff Works Shows"
	how_stuff_works(url)
elif mode==636:
        print "How Stuff Works Videos"
	hsw_videos(url)
elif mode==637:
        print "How Stuff Works Video"
	hsw_video(url)
elif mode==638:
        print "How Stuff Works Most Watched"
	most_watched(name,url)
elif mode==639:
        print "How Stuff Works More Shows"
	more_shows(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
