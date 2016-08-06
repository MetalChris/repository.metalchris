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
import html5lib
import simplejson as json
import datetime
from pytz import timezone

artbase = 'special://home/addons/plugin.video.hunt-channel/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.hunt-channel')
self = xbmcaddon.Addon(id='plugin.video.hunt-channel')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.hunt-channel")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Hunt Channel"

defaultimage = 'special://home/addons/plugin.video.hunt-channel/icon.png'
defaultfanart = 'special://home/addons/plugin.video.hunt-channel/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.hunt-channel/icon.png'
baseurl = 'http://www.huntchannel.tv'
schedule = 'special://home/addons/plugin.video.hunt-channel/resources/media/schedule.json'

local_string = xbmcaddon.Addon(id='plugin.video.hunt-channel').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#q = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]

now = datetime.datetime.now(timezone('US/Eastern'))
now_minus_30 = now + datetime.timedelta(minutes = -30)
print now.year, now.month, now.day, now_minus_30.hour, now_minus_30.minute
if now.hour >12:
	hour = now.hour - 12
else:
	hour = now.hour
if now.minute < 29:
	minute = '00'
else:
	minute = '30'
showday = now.strftime("%A")
nowstring = str(hour) + ':' + minute + ' ' + now.strftime("%p")
schedpath = 'file://' + urllib.pathname2url(_addon_path) + '/schedule.json'
data = json.load(urllib2.urlopen(schedpath))
shows = data[nowstring]
for show in shows:
	if showday in show:
		program = shows[showday]
		if len(program) <2:
			program = 'No Info Available'


#10
def cats():
	addDir2('Live Stream' + ': ' + program,'http://json.dacast.com/b/60923/c/82360',12,defaultimage)
	addDir('On Demand','http://www.huntchannel.tv',11,defaultimage)
        xbmcplugin.endOfDirectory(addon_handle)


#11
def vod(url):
	addDir('Featured','http://www.huntchannel.tv',13,defaulticon)
	addDir('Recently Added','http://huntchannel.tv/feed/',14,defaulticon)
	addDir('All Shows','http://huntchannel.tv/shows/',15,defaulticon)
        xbmcplugin.endOfDirectory(addon_handle)


#12
def get_live(url,iconimage):
        response = urllib2.urlopen(url)
        jdata = json.load(response)
	m3u8 = jdata['hls']
	print m3u8
	listitem = xbmcgui.ListItem('Hunt Channel Live Stream' + ': ' + program, thumbnailImage=defaulticon)
	xbmc.Player().play( m3u8, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


#13
def get_vod(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'scroll-text'})
	titles = re.compile('<li>(.+?)</li>').findall(str(soup))
	for title in titles:
	    url = str(re.compile('href=(.+?)>').findall(str(title)))[3:-3]
	    title = striphtml(title)
	    add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#14
def recent(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('item')
	for item in soup:
	    title = item.find('title').string.encode('utf-8').title()
	    url = item.find('comments').string.split('#')[0]
	    add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#15
def shows(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'entry-content'})
	for item in soup:
	    title = (item.find('a')['title']).encode('utf-8').strip()
	    image = item.find('img')['src'] 
	    show_id = image.split('/')
	    url = item.find('a')['href']
	    add_directory2(title,url,20,defaultfanart,image,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'entry-content'})
	for item in reversed(soup):
	    title = (item.find('a')['title']).encode('utf-8').strip()
	    image = item.find('img')['src'] 
	    show_id = image.split('/')
	    url = item.find('a')['href']
	    add_directory2(title,url,30,defaultfanart,image,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('iframe')[0]
	iframe = re.compile('src="(.+?)"').findall(str(soup))[0]
	source = get_html(iframe)
	thumbnail = re.compile('base":"(.+?)"').findall(str(source))[-1]
	m3u8 = (re.compile('"url":"(.+?)"').findall(str(source))[0]).split(',')
	key = (m3u8[-1]).split('/')[0]
	stream = (m3u8[0]).rpartition('/')[0] + '/' + key + '/playlist.m3u8?p=6'
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
	xbmc.Player().play( stream, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def play(name,url,iconimage):
        print url
	listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
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

def addLink(name, url, mode, iconimage, fanart=True, infoLabels=True):
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


def addDir2(name,url,mode,iconimage, fanart=True, infoLabels=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image',defaultfanart)
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
    cats()
elif mode == 4:
    print "Play Video"
elif mode==11:
        print 'Hunt Channel VOD'
	vod(url)
elif mode==12:
        print 'Hunt Channel Live'
	get_live(url,iconimage)
elif mode==13:
        print 'Hunt Channel Featured'
	get_vod(url)
elif mode==14:
        print 'Hunt Channel Recent'
	recent(url)
elif mode==15:
	print 'Hunt Channel Shows'
	shows(url)
elif mode==20:
        print "Hunt Channel Videos"
	videos(url)
elif mode==30:
        print "Hunt Channel Streams"
	streams(name,url)
elif mode==40:
        print "Hunt Channel Live"
	play(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
