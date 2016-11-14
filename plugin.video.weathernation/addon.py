#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
from bs4 import BeautifulSoup
from urllib import urlopen
import simplejson as json

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.weathernation')
self = xbmcaddon.Addon(id='plugin.video.weathernation')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.weathernation")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "WeatherNation TV"

defaultimage = 'special://home/addons/plugin.video.weathernation/icon.png'
defaultfanart = 'special://home/addons/plugin.video.weathernation/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.weathernation/icon.png'
defaulturl='aHR0cDovL2NkbmFwaS5rYWx0dXJhLmNvbS9odG1sNS9odG1sNWxpYi92Mi40Mi9td0VtYmVkRnJhbWUucGhwPyZ3aWQ9XzkzMTcwMiZ1aWNvbmZfaWQ9Mjg0Mjg3NTEmZW50cnlfaWQ9'
liveurl = 'aHR0cDovL2thbHNlZ3NlYy1hLmFrYW1haWhkLm5ldDo4MC9kYy0wL20vcGEtbGl2ZS1wdWJsaXNoNi9rTGl2ZS9zbWlsOjFfb29yeGNnZTJfYWxsLnNtaWwv'

local_string = xbmcaddon.Addon(id='plugin.video.weathernation').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
#LIVE = settings.getSetting(id="live")
confluence_views = [500,501,502,503,504,508,515]

def categories():
    mode = 1

    addDir('WeatherNation Live', 'http://cdnapi.kaltura.com/html5/html5lib/v2.34/mwEmbedFrame.php?&wid=_931702&uiconf_id=28428751&entry_id=1_oorxcge2', 635, defaultimage)#1_o06v504o
    #addDir('WeatherNation Videos', 'http://www.weathernationtv.com/on_tv/?play=1', 634, defaultimage)
    addDir('WeatherNation Videos', 'http://www.weathernationtv.com/video/', 634, defaultimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#634
def wn_videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response, 'html5lib').find_all('div',{'class':'col-md-4 video-item'})
	print len(soup)
	for show in soup[0:15]:#.find_all("div",{"class":"pull-left"}): 0:15, 15:30, 30:56, 56:72
	    title = show.find('h4').text.title().encode('utf-8')#('img')['alt'].title()
	    image = 'http://www.weathernationtv.com' + show.find('img')['data-src']
	    video_id = (show.find('a')['data-id'])
	    url = defaulturl.decode('base64') + video_id
            add_directory2(title, url, 636,   defaultfanart, image, plot='')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#635
def wn_live(name,url):
	response = get_html(url)
	stream = (re.compile('hls","url":"(.+?)"').findall(str(response))[0]).replace('\\','')
	listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
        listitem.setProperty('IsPlayable', 'true')
	xbmc.Player().play( stream, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)



def play(url,name):
	jdata = get_html(url)
	data = re.compile('kalturaIframePackageData =(.+?);\n\t\t\tvar isIE8').findall(str(jdata))[0]
	bitkeys = re.compile('2,"id":"(.+?)","entryId').findall(data)
	if QUALITY =='1':
	    bitkey = bitkeys[3]
	elif QUALITY =='0':
	    bitkey = bitkeys[2]
	else:
	    bitkey = bitkeys[5]
	url = 'http://www.kaltura.com/p/243342/sp/24334200/playManifest/entryId/' + url[-10:] + '/flavorId/' + bitkey + '/format/url/protocol/http/a.mp4'
	listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
        listitem.setProperty('IsPlayable', 'true')
	xbmc.Player().play( url, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


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


def add_directory2(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=15)
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
        categories()
elif mode == 1:
        print "Indexing Videos"
        INDEX(url)
elif mode == 4:
        print "Play Video"
elif mode == 6:
        print "Get Episodes"
        get_episodes(url)
elif mode==634:
        print "WeatherNation Videos"
	wn_videos(url)
elif mode==635:
        print "WeatherNation Live"
	wn_live(name,url)
elif mode==636:
        print "WeatherNation Play Videos"
	play(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
