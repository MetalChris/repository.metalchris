#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import HTMLParser
import simplejson as json
import html5lib
from urllib import urlopen
import requests

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.bigsouth')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.bigsouth/icon.png'
defaultfanart = 'special://home/addons/plugin.video.bigsouth/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.bigsouth/icon.png'
defaulticon = 'special://home/addons/plugin.video.bigsouth/icon.png'
baseurl = 'http://video.nationalgeographic.com'
live = 'aHR0cDovL2JpZ3NvdXRoc3BvcnRzLmNvbS9zZXJ2aWNlcy9hbGxhY2Nlc3MuYXNoeC8yL21lZGlhL2dldD90eXBlPUxpdmU='
archive = 'aHR0cDovL2JpZ3NvdXRoc3BvcnRzLmNvbS9zZXJ2aWNlcy9hbGxhY2Nlc3MuYXNoeC8yL21lZGlhL2dldD90eXBlPUFyY2hpdmU='
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]


def CATEGORIES():
	addDir('Live & Upcoming', live.decode('base64'), 1, defaultimage)
	addDir('Video On Demand', archive.decode('base64'), 1, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#1
def INDEX(name,url):
	response = get_html(url)
	data = json.loads(response)#; i = 0
        for i in range(30):
	    title = (data['data'][i]['title'])
	    sport_title = (data['data'][i]['sport_title'])
	    date_utc = (data['data'][i]['date_utc']).replace('-','/').split('T')
	    utc_date = (data['data'][i]['date_utc']).replace('T',' ')
	    start = (date_utc[1]).split(':')
	    etime = start[0] + ':' + start[1] + ' UTC'
	    if 'Live' in name:
		event = '[' + (date_utc[0])[5:]  + ' ' + etime + '] ' + title + ' (' + sport_title + ')'
	    else:
	        event = '[' + (date_utc[0])[5:] + '] ' + title + ' (' + sport_title + ')'
	    url = (data['data'][i]['formats']['MobileH264'])
	    if 'Demand' in name:
	        r = requests.head(url)
	        if r.status_code == 404:
		    continue
	    image = (data['data'][i]['poster'])
            li = xbmcgui.ListItem(event, iconImage= image, thumbnailImage= image)
	    li.addStreamInfo('video', { 'title': title })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=30)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

#99
def PLAY(name,url):
        html = get_html(url)
	video = (re.compile('video src="(.+?)"').findall(html)[0]).replace('/z/','/i/') + '/master.m3u8'
	print video
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( video, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def sanitize(data):
    output = ''
    for i in data:
        for current in i:
            if ((current >= '\x20') and (current <= '\xD7FF')) or ((current >= '\xE000') and (current <= '\xFFFD')) or ((current >= '\x10000') and (current <= '\x10FFFF')):
               output = output + current
    return output



def get_html(url):
    req = urllib2.Request(url)
    req.add_header('Host', 'bigsouthsports.com')
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

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
	print "Big South Sports Menu"
	CATEGORIES()
elif mode == 1:
	print "Big South Sports Events"
	INDEX(name,url)
elif mode == 2:
	print "Big South Sports Sub Menu"
	SUBCATEGORIES(url)
elif mode == 99:
	print "Play Video"
	PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
