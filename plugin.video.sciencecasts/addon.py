#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib


artbase = 'special://home/addons/plugin.video.sciencecasts/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.sciencecasts')
self = xbmcaddon.Addon(id='plugin.video.sciencecasts')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "NASA ScienceCasts"

defaultimage = 'special://home/addons/plugin.video.sciencecasts/icon.png'
defaultfanart = 'special://home/addons/plugin.video.sciencecasts/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.sciencecasts/icon.png'
baseurl = 'http://feeds.feedburner.com/NasaSciencecasts?format=xml'

local_string = xbmcaddon.Addon(id='plugin.video.sciencecasts').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]


#636
def videos(url):
	response = get_html(baseurl)
	soup = BeautifulSoup(response,'html5lib').find_all('item')
	for item in soup:
	    print item
	    title = item.find('title').string.encode('utf-8')
	    duration = item.find('itunes:duration').string.encode('utf-8')
	    description = item.find('itunes:summary').string.encode('utf-8') + ' (' + duration + ')'
	    image = item.find('itunes:image')['href']
	    url = image.replace('episode_thumbs/','').replace('-poster.jpg','.m4v')
	    infoLabels = {'Title':title, 'Plot':description}
            li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
            li.setProperty('fanart_image',  image)
            li.setProperty('mimetype', 'video/x-m4v')
            li.setInfo( type='Video', infoLabels=infoLabels )  
	    #li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)



def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


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
    videos(url)
elif mode == 4:
    print "Play Video"
elif mode==635:
        print "NASA ScienceCasts Archive"
	archives(url)
elif mode==636:
        print "NASA ScienceCasts Videos"
	msl_videos(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
