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
import cookielib
from cookielib import CookieJar


artbase = 'special://home/addons/plugin.video.lifechurch/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.lifechurch')
self = xbmcaddon.Addon(id='plugin.video.lifechurch')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.lifechurch")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Life.Church"

defaultimage = 'special://home/addons/plugin.video.lifechurch/icon.png'
defaultfanart = 'special://home/addons/plugin.video.lifechurch/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.lifechurch/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.lifechurch').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#632
def podcast():
	html = get_html('http://feedpress.me/lifechurchipod')
	soup = BeautifulSoup(html,'html.parser').find_all('item')
	items = sorted(soup, reverse=True)
	for item in items:
	    title = item.find('title').string.encode('utf-8')
	    url = item.find('enclosure')['url']
	    duration = item.find('itunes:duration').string.encode('utf-8')
            li = xbmcgui.ListItem(title, iconImage= defaulticon, thumbnailImage= defaultimage)
            li.setProperty('mimetype', 'video/mp4')
            li.setProperty('fanart_image',  defaultfanart)
            #li.setInfo( type='Video', infoLabels=infoLabels )  
	    li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=50)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#633
def shows():
	#r = requests.get('http://feed.theplatform.com/f/IfSiAC/XyWs4EsDTkxg')
	#print r.headers
	#print r.cookies
	html = get_html('http://www.life.church/watch/')
	soup = BeautifulSoup(html,'html.parser').find_all("div",{"class":"grid-item watch-item"})
	for show in soup:
	    title = striphtml(str(show.find('h6')))
	    #print title
	    url = 'http://life.church' + str(show.find('a')['href'])
	    #print url
	    iconimage = str(show.find('img')['data-retina'])
	    #print iconimage
            add_directory2(title, url, 636, iconimage, iconimage, plot='')
        add_directory2('PodCast', url, 632, defaultfanart, defaultimage, plot='')
        add_directory2('Archives', url, 635, defaultfanart, defaultimage, plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#634
def episodes(url):
	base = url.rpartition('/')[0]
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser')
	for show in soup.find_all("li",{"class":"grid-item md"}):
	    title = striphtml(str(show.find('h5')))
	    #print title
	    key = show.find('a')['href']
	    #print key
	    url = base + key + '/feed/mp4-large'
	    #print url
	    thumbnail = 'http://videos.revision3.com/revision3/images/shows' + key + key + '_web_avatar.jpg'
	    #print thumbnail
            add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
        add_directory2('Archives', url, 635, defaultfanart, defaultimage, plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#635
def archives(url):
	response = get_html('http://www.life.church/watch/archive/')
	soup = BeautifulSoup(response,'html.parser')
	for item in soup.find_all("div",{"class":"grid-items grid-three"})[1:]:
	    group = item.find_all('div',{'class':'watch-item grid-item'})
	    for item in group:
		title = (item.find('h6')).string.encode('utf-8')
		image = str(item.find('img')['data-retina'])
	        url = 'http://life.church' + str(item.find('a')['href'])
                add_directory2(title, url, 636, defaultfanart, image, plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#636
def lifechurch_videos(url, iconimage):
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser').find_all("a",{"class":"message"})
	print len(soup)
	if len(soup) < 1:
	    title = 'Watch the Promo'
	    print title
	    key = re.compile('data-video-player="(.+?)"').findall(str(response))[-1]
	    print key
	    ##url = 'http://link.theplatform.com/s/IfSiAC/media/' + key
	    ###url = 'http://player.theplatform.com/p/IfSiAC/bTc5flAyW_uT/embed/select/media/' + str(key) + '?form=html'
	    playurl = 'http://link.theplatform.com/s/IfSiAC/media/' + key
	    print playurl
	    if QUALITY =='2':
	        playthis = (get_redirected_url(playurl)).replace('_144','_1080')	    
	    elif QUALITY =='1':
	        playthis = (get_redirected_url(playurl)).replace('_144','_720')
	    elif QUALITY =='0':
	        playthis = (get_redirected_url(playurl)).replace('_144','_480')
	    print 'Play This ' + str(playthis)
	    stream = playthis
            li = xbmcgui.ListItem(title, iconImage= iconimage, thumbnailImage= iconimage)
            li.setProperty('fanart_image',  iconimage)
            li.setProperty('mimetype', 'video/mp4')
            #li.setInfo( type='Video', infoLabels=infoLabels )  
	    #li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=stream, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes') 
	   
	for item in soup:
	    title = striphtml(str(item.find('h6')))
	    print title
	    key = re.compile('data-video-player="(.+?)"').findall(str(item))[-1]
	    print key
	    ##url = 'http://link.theplatform.com/s/IfSiAC/media/' + key
	    ###url = 'http://player.theplatform.com/p/IfSiAC/bTc5flAyW_uT/embed/select/media/' + str(key) + '?form=html'
	    playurl = 'http://link.theplatform.com/s/IfSiAC/media/' + key
	    print playurl
	    if QUALITY =='2':
	        playthis = (get_redirected_url(playurl)).replace('_144','_1080')	    
	    elif QUALITY =='1':
	        playthis = (get_redirected_url(playurl)).replace('_144','_720')
	    elif QUALITY =='0':
	        playthis = (get_redirected_url(playurl)).replace('_144','_480')
	    print 'Play This ' + str(playthis)
	    stream = playthis
            li = xbmcgui.ListItem(title, iconImage= iconimage, thumbnailImage= iconimage)
            li.setProperty('fanart_image',  iconimage)
            li.setProperty('mimetype', 'video/mp4')
            #li.setInfo( type='Video', infoLabels=infoLabels )  
	    #li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=stream, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    #print 'Redirect' + str(request.url)
    playthis = request.url
    #play(playthis)
    return request.url


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def play(url):
    item = xbmcgui.ListItem(path=url)
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def add_directory2(name,url,mode,fanart,iconimage,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
        return ok

def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0')

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
    print "Generate Main Menu"
    shows()
elif mode == 4:
    print "Play Video"
elif mode==632:
        print "Life Church PodCast"
	podcast()
elif mode==633:
        print "Life Church Shows"
	shows()
elif mode==634:
	print "Life Church Episodes"
	episodes(url)
elif mode==635:
        print "Life Church Archive"
	archives(url)
elif mode==636:
        print "Life Church Videos"
	lifechurch_videos(url, iconimage)
elif mode==637:
        print "Animalist Video"
	animalist_video(url)
elif mode==638:
        print "Animalist Most Watched"
	most_watched(name,url)
elif mode==639:
        print "Animalist More Shows"
	more_shows(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
