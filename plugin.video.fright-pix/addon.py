#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
import time
import datetime
from datetime import date, timedelta
from BeautifulSoup import BeautifulStoneSoup as Soup
import HTMLParser
import simplejson as json
import xml.etree.ElementTree as ET
#import pyxbmct.addonwindow as pyxbmct 
#from urllib2 import urlopen
#from lxml import etree


today = datetime.date.today()
today = today.strftime("%m/%d")
days7 = date.today() - timedelta(days=7)
day7 = days7.strftime("%m/%d")

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.fright-pix')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.fright-pix")

defaultimage = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
defaultfanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'
#defaultvideo = 'special://home/addons/plugin.video.fright-pix/icon.png'
#defaulticon = 'special://home/addons/plugin.video.fright-pix/icon.png'
fanart = 'special://home/addons/plugin.video.fright-pix/fanart.jpg'

#SHOWHADIALOG = settings.getSetting(id="showhadialog")
#SHOWHADIALOGLIVE = settings.getSetting(id="showhadialoglive")
#local_string = xbmcaddon.Addon(id='plugin.video.fright-pix').getLocalizedString
#ACTION_SELECT_ITEM = 7
#QUALITY = settings.getSetting(id="quality")
#ACTION_MOUSE_LEFT_CLICK = 100

def CATEGORIES():
    mode = 1

    addDir('New Arrivals', 'http://feeds.the-antinet.com/movies/fpnew.xml', mode,
           defaultimage)
    addDir('Staff Picks', 'http://feeds.the-antinet.com/movies/fpstaff.xml', mode,
           defaultimage)
    addDir('Most Popular', 'http://feeds.the-antinet.com/movies/fpmost.xml', mode,
           defaultimage)
    addDir('Sexy Horror', 'http://feeds.the-antinet.com/movies/fpsexy.xml', mode,
           defaultimage)
    addDir('Troma', 'http://feeds.the-antinet.com/movies/fptroma.xml', mode,
           defaultimage)
    addDir('Scary Good', 'http://feeds.the-antinet.com/movies/fpscary.xml', mode,
           defaultimage)
    addDir('Supernatural', 'http://feeds.the-antinet.com/movies/fpsuper.xml', mode,
           defaultimage)
    addDir('Screaming Worldwide', 'http://feeds.the-antinet.com/movies/fpscreaming.xml', mode,
           defaultimage)
    addDir('Creature Feature', 'http://feeds.the-antinet.com/movies/fpcreature.xml', mode,
           defaultimage)
    addDir('Slasher', 'http://feeds.the-antinet.com/movies/fpslasher.xml', mode,
           defaultimage)
    addDir('Zombies', 'http://feeds.the-antinet.com/movies/fpzombies.xml', mode,
           defaultimage)
    addDir('Vampires', 'http://feeds.the-antinet.com/movies/fpvampires.xml', mode,
           defaultimage)
    addDir('Demons', 'http://feeds.the-antinet.com/movies/fpdemons.xml', mode,
           defaultimage)
    addDir('Cult', 'http://feeds.the-antinet.com/movies/fpcult.xml', mode,
           defaultimage)
    addDir('The CAMP Ground', 'http://feeds.the-antinet.com/movies/fpcamp.xml', mode,
           defaultimage)
    addDir('Creepy Documentaries', 'http://feeds.the-antinet.com/movies/fpcreepy.xml', mode,
           defaultimage)
    addDir('Horror-ble', 'http://feeds.the-antinet.com/movies/fphorror.xml', mode,
           defaultimage)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def INDEX(url):

    if "fpnew" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)
        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]  
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "staff" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)
        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "most" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)
        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "sexy" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "troma" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "scary" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "super" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "screaming" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "creature" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "slasher" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "zombies" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "vampires" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "demons" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "cult" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "camp" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "creepy" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

    if "horror" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        soup = Soup(html)

        for event in soup.findAll('item'):
            msg_attrs = dict(event.attrs)
            eventname = str(event.find('title'))
            html_parser = HTMLParser.HTMLParser()
            name = eventname[7:-8]
            mode=4
            url = str(event.find('media'))[7:-8]     
            image = str(event.find('image'))[7:-8]   

            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass


def onAction(self, action):
    if action == ACTION_MOUSE_LEFT_CLICK:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(local_string(31300), local_string(31310),'','',local_string(31320),local_string(31330))
            if ret == 0:
                print "HOME"
                liz=xbmcgui.ListItem(home, iconImage=defaulticon, thumbnailImage=homeimg)
                liz.setInfo( type="Video", infoLabels=False)
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(homelink,liz)                
            else:
                print "AWAY"
                liz=xbmcgui.ListItem(away, iconImage=defaulticon, thumbnailImage=awayimg)
                liz.setInfo( type="Video", infoLabels=False)
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(awaylink,liz)

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
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
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
    print "Generate Main Menu"
    CATEGORIES()
elif mode == 1:
    print "Indexing Videos"
    INDEX(url)
elif mode == 4:
    print "Play Video"



xbmcplugin.endOfDirectory(int(sys.argv[1]))


