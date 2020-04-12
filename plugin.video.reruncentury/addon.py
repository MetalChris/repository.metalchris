#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

# 2020.04.12

import urllib, urllib2, xbmc, xbmcplugin, xbmcaddon, xbmcgui, htmllib, calendar, re, sys
from bs4 import BeautifulSoup
import html5lib

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.reruncentury')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.reruncentury")
log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

defaultimage = 'special://home/addons/plugin.video.reruncentury/icon.png'
defaultfanart = 'special://home/addons/plugin.video.reruncentury/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.reruncentury/icon.png'
addon_handle = int(sys.argv[1])

def CATEGORIES():
    mode = 1
    addDir('Top Shows (More than 40 Episodes)', 'http://www.reruncentury.com/', 2, '')
    addDir('More Shows (More than 10 Episodes)', 'http://www.reruncentury.com/', 5, '')
    addDir('All Shows (Alphabetical)', 'http://www.reruncentury.com/ia/', 3, '')


#2
def top_shows(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'cellMain i20px'})
    xbmc.log('SOUP: ' + str(soup),level=log_level)
    for titles in soup:
        title = titles.find('a').text
        xbmc.log('TITLE: ' + str(title),level=log_level)
        url = 'https://www.reruncentury.com' + titles.find('a')['href']
        xbmc.log('URL: ' + str(url),level=log_level)
        thumbnail = titles.find('img')['src']
        addDir(title, url, 6, thumbnail)
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#3
def all_shows(url):
    html = get_html(url)
    shows = re.compile ('<a href="(.+?)">(.+?)</a>').findall(html)
    for url, title in shows:
        url = 'https://www.reruncentury.com' + str(url)
        if not '/series/pd/' in url:
            continue
        addDir(title, url, 6, '')
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#5
def more_shows(url):
    html = get_html(url)
    shows = re.compile ('<br><a href="(.+?)">(.+?)</a>').findall(html)
    for url, name in shows:
        url = 'http://www.reruncentury.com' + str(url)
        addDir(name, url,6,'')
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#6
def get_episodes(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('div',{'style':'width:300px'})
    for episodes in soup:
        title = episodes.find('a').text
        xbmc.log('TITLE: ' + str(title),level=log_level)
        rurl = 'https://www.reruncentury.com' + episodes.find('a')['href']
        xbmc.log('URL: ' + str(url),level=log_level)
        thumbnail = episodes.find('img')['src']
        url = 'plugin://plugin.video.reruncentury?mode=20&url=' + urllib.quote_plus(rurl)
        li = xbmcgui.ListItem(title)
        li.setProperty('IsPlayable', 'true')
        li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"TV"})
        li.setArt({'thumb':thumbnail,'fanart':defaultfanart})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
        xbmcplugin.setContent(addon_handle, 'episodes')
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

#20
def get_stream(name,url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('video')#,{'type':'video/mp4'})
    xbmc.log('SOUP: ' + str(soup),level=log_level)
    for video in soup:
        url = video.find('source')['src']
        xbmc.log('URL: ' + str(url),level=log_level)
    PLAY(name,url)
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

#99
def PLAY(name,url):
    addon_handle = int(sys.argv[1])
    listitem = xbmcgui.ListItem(path=url)
    xbmc.log(('### SETRESOLVEDURL ###'),level=log_level)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    xbmc.log('URL: ' + str(url), level=log_level)
    xbmcplugin.endOfDirectory(addon_handle)

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


def addDir(name, url, mode, iconimage, fanart=False, infoLabels=True):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=defaulticon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    if not fanart:
        fanart=defaultfanart
    liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
    xbmc.log(("Generate Main Menu"),level=log_level)
    CATEGORIES()
elif mode == 1:
    xbmc.log(("Indexing Videos"),level=log_level)
    INDEX(url)
elif mode == 2:
	xbmc.log(("Indexing Top Shows"),level=log_level)
	top_shows(url)
elif mode == 3:
	xbmc.log(("Get All Shows"),level=log_level)
	all_shows(url)
elif mode == 4:
    xbmc.log(("Play Video"),level=log_level)
elif mode == 5:
	xbmc.log(("Get More Shows"),level=log_level)
	more_shows(url)
elif mode == 6:
	xbmc.log(("Get Episodes"),level=log_level)
	get_episodes(url)
elif mode == 20:
	xbmc.log(("Get Stream"),level=log_level)
	get_stream(name,url)
elif mode == 99:
	xbmc.log("Play Video", level=log_level)
	PLAY(name,url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
