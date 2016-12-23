#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import HTMLParser
import html5lib
import requests
import json
import datetime
from pytz import timezone

now = datetime.datetime.now(timezone('US/Eastern'))
xbmc.log('Now Hour: ' + str(now.hour))
daynum = int(now.strftime("%w"))
xbmc.log('Day Number: ' + str(daynum))

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.120sports')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.120sports/icon.png'
defaultfanart = 'special://home/addons/plugin.video.120sports/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.120sports/icon.png'
defaulticon = 'special://home/addons/plugin.video.120sports/icon.png'
#rtmp://cp279796.live.edgefcs.net/live/120sports_c101_n3000@183136 live=true

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]
plugin = '120 Sports'


def CATEGORIES():
	addDir('Live Stream', 'http://c.120sportsstatic.com/gen/client/state.json', 1, defaultimage)
	#addDir2('Twitter', 'https://twitter.com/i/live_video_stream/status/807393889451544576?client=web', 2, defaultimage)
	addDir('Latest Videos', 'http://c.120sportsstatic.com/gen/client/timeline.json', 3, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#1
def INDEX(url):
        jresponse = urllib2.urlopen(url)
        jdata = json.load(jresponse)
	key = jdata['HTTP_CLOUD_WIRED']
	xbmc.log(str(key))
	if (0 < daynum < 7) and (20 < now.hour < 23):
	    xbmc.log('The Rally')
	    xbmc.log(str(key))
	    url = 'rtmp://cp279796.live.edgefcs.net/live/120sports_c101_n3000@183136 live=true'
	    play(plugin + ' ' + name,url)
	elif (key != 'on'):                 
	    xbmc.log('No Live Broadcast Available') 
	    line1 = "Live Stream Currently Unavailable"
	    line2 = "Check the Live Schedule for More Info"
	    xbmcgui.Dialog().ok(plugin, line1, line2)
	    LIVE(url)
	else:
	    url = 'rtmp://cp279796.live.edgefcs.net/live/120sports_c101_n3000@183136 live=true'
	    play(plugin + ' ' + name,url)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#2
def TWITTER(url):
        jresponse = urllib2.urlopen(url)
        jdata = json.load(jresponse)
	stream = 'rtmp://cp279796.live.edgefcs.net/live/120sports_c101_n3000@183136'
	xbmc.log(str(stream))
	play(stream)            
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#3
def VIDEOS(url):
        jresponse = urllib2.urlopen(url)
        jdata = json.load(jresponse);i=0
	item_dict = jdata
	count = len(item_dict['segment'])
	xbmc.log(str(count))
	for i in range(0,count-4):
	    title = jdata['segment'][i]['title']
	    url = jdata['segment'][i]['media_playback_urls']['HTTP_CLOUD_WIRED']['url']
	    try:images = str(jdata['segment'][i]['images'])
	    except KeyError:
		image = defaultimage
		continue
	    image = str(re.compile("480x270': u'(.+?)'").findall(images))[2:-2]
	    addDir2(title, url, 99, image)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#4
def LIVE(url):
	addDir2('120 Morning Run M-F 8-11 AM ET', 'http://c.120sportsstatic.com/gen/client/state.json', None, defaultimage)
	addDir2('120 Spotlight M-F 11 AM ET', 'http://c.120sportsstatic.com/gen/client/state.json', None, defaultimage)
	addDir2('The Rally M-F 9-11 PM ET', 'http://c.120sportsstatic.com/gen/client/state.json', None, defaultimage)
	addDir2('120 Sports M-S 11 PM - 2 AM ET', 'http://c.120sportsstatic.com/gen/client/state.json', None, defaultimage)
	return
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#99
def play(name,url):
    listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
    xbmc.Player().play( url, listitem )
    sys.exit()


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
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')

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
        liz.setProperty('IsPlayable', 'true')
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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("120 Sports Menu")
	CATEGORIES()
elif mode == 1:
	xbmc.log("120 Sports Live")
	INDEX(url)
elif mode == 2:
	xbmc.log("120 Sports Play  Live Event")
	TWITTER(url)
elif mode == 3:
	xbmc.log("120 Sports Videos")
	VIDEOS(url)
elif mode == 4:
	xbmc.log("120 Sports Live Schedule")
	LIVE(url)
elif mode == 99:
	xbmc.log("120 Sports Play Video")
	play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
