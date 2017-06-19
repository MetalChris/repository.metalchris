#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or later)

import xbmcplugin, xbmcaddon, xbmcgui, sys, re, urllib2
import time

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.audio.buddha')
translation = selfAddon.getLocalizedString
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
settings = xbmcaddon.Addon(id="plugin.audio.buddha")
q = settings.getSetting(id="quality")
t = settings.getSetting(id="transport")
n = settings.getSetting(id="notify")
base = '://stream.scahw.com.au/live/buddha_'
plugin = "Buddha Radio"
local_string = xbmcaddon.Addon(id='plugin.audio.buddha').getLocalizedString
defaultimage = 'special://home/addons/plugin.audio.buddha/icon.png'


def now_playing():
	if n != 'true':
	    print '===Notification Off==='
	else:
	    html = get_html('http://tunein.com/radio/Buddha-Radio-s172072/')
	    info = (re.compile('data-reactid="262">(.+?)</p').findall(html)[0]).replace('&#39;', '\'').replace('&amp;', '&')
	    print info
            xbmcgui.Dialog().notification('Now Playing on Buddha Radio', info, defaultimage, 7500, False)
	    for i in range(60):
	        if xbmc.Player().isPlayingAudio():
		    song = xbmc.Player().getMusicInfoTag(info)
	            #print song
	            time.sleep(1)
	        else:
		    print '===== EXIT ====='
	            sys.exit()
	    now_playing()


def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

    try:
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
    except urllib2.HTTPError as (e):
	print (e)
        response = False
        html = False
    return html


if q == '1':
	key = '128'
else:
	key = '32'
if t == '1':
	pre = 'http'; post = '.stream/playlist.m3u8'
else:
	pre = 'rtsp'; post = '.stream'

url = pre + base + key + post

item = xbmcgui.ListItem(thumbnailImage=defaultimage)
#item.setInfo("music", {
#        "title": "Buddha Radio",
#})
#item.setProperty("IsPlayable", "true")
xbmc.Player().play( url, item );time.sleep(10); now_playing()
sys.exit()

xbmcplugin.endOfDirectory(addon_handle)
