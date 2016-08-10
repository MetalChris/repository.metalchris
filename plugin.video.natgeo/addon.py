#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import HTMLParser
import simplejson as json
import html5lib

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.natgeo')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.natgeo/icon.png'
defaultfanart = 'special://home/addons/plugin.video.natgeo/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.natgeo/icon.png'
defaulticon = 'special://home/addons/plugin.video.natgeo/icon.png'
baseurl = 'http://video.nationalgeographic.com'
pre_smil = 'aHR0cDovL2xpbmsudGhlcGxhdGZvcm0uY29tL3MvbmdzL21lZGlhL2d1aWQvMjQyMzEzMDc0Ny8='
post_smil = 'P21icj10cnVlJnBvbGljeT0xMjQ0MTM4NSZtYW5pZmVzdD1mNG0mZm9ybWF0PVNNSUwmVHJhY2tpbmc9dHJ1ZSZFbWJlZGRlZD10cnVlJmZvcm1hdHM9RjRNLE1QRUc0'


pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]


def CATEGORIES():
        html = get_html(baseurl)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'dropdown-container dropdown'})[0]
	urls = re.compile('href="(.+?)"').findall(str(soup))
	titles = re.compile('">(.+?)</').findall(str(soup))
	for url,title in zip(urls,titles):
	    title = (title).replace('&amp;','&')
	    url = baseurl + url
	    addDir(title, url, 2, defaultimage)
	addDir('Latest 100', url, 1, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#1
def INDEX():
	html = get_html('http://video.nationalgeographic.com/')
	feed = re.compile('data-feed-url="(.+?)"').findall(html)[0]
	print feed
        html = get_html(feed)
	soup = BeautifulSoup(html,'html5lib').find_all('item')
        for item in soup:
	    title = item.find('title').text.encode('utf-8')
	    url = (item.find('media:content')['url'])
	    image = (item.find('media:thumbnail')['url'])
            addDir(title, url, 99, image)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#2
def SUBCATEGORIES(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'dropdown-container dropdown'})[-1]
	urls = re.compile('href="(.+?)"').findall(str(soup))
	titles = re.compile('">(.+?)</').findall(str(soup))
	for url,title in zip(urls,titles):
	    title = (title).replace('&amp;','&')
	    url = baseurl + url #+ '?gs=&gp=0'
	    addDir(title, url, 3, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#3
def VIDEOS(url):
        html = get_html(url)
	match = re.compile('href="(.+?)data-feed').findall(str(html))
	for item in match[::2]:
	    title = re.compile('data-title="(.+?)"').findall(item)[0]
	    title = (title).replace('&amp;','&').replace('&mdash;','-').replace('&quot;','\"').replace('&rsquo;','\'').replace('&#39;','\'')# + ' - ' + url
	    guid = (item.split('guid="')[-1]).replace('" ','')
	    url = pre_smil.decode('base64') + guid + post_smil.decode('base64')
            addDir2(title, url, 98, defaultimage)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#98
def PLAYSMIL(name,url):
        html = get_html(url)
	video = (re.compile('video src="(.+?)"').findall(html)[0]).replace('/z/','/i/').replace('manifest.f4m','master.m3u8')
	print video
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( video, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


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
    req.add_header('Host', 'video.nationalgeographic.com')
    req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
    req.add_header('Referer', 'http://video.nationalgeographic.com/video')
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
	print "NatGeo Menu"
	CATEGORIES()
elif mode == 1:
	print "NatGeo Latest 100"
	INDEX()
elif mode == 2:
	print "NatGeo Sub Menu"
	SUBCATEGORIES(url)
elif mode == 3:
	print "Indexing Videos"
	VIDEOS(url)
elif mode == 98:
	print "Play SMIL"
	PLAYSMIL(name,url)
elif mode == 99:
	print "Play Video"
	PLAY(name,url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


