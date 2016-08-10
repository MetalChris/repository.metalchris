#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import simplejson as json
#import requests  
#from lxml import html  
#import urlparse
#import time
#import HTMLParser
from bs4 import BeautifulSoup
#import codecs
#from wkRender import getHtml
#from lxml import etree
from urllib import urlopen
import socket


apiURL = 'http://www.omdbapi.com/'
artbase = 'special://home/addons/plugin.video.moviezoot/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.moviezoot')
self = xbmcaddon.Addon(id='plugin.video.moviezoot')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.moviezoot")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "MovieZoot"

defaultimage = 'special://home/addons/plugin.video.moviezoot/icon.png'
defaultfanart = 'special://home/addons/plugin.video.moviezoot/curtains.jpg'
#defaultvideo = 'special://home/addons/plugin.video.moviezoot/icon.png'
defaulticon = 'special://home/addons/plugin.video.moviezoot/icon.png'
#fanart = 'special://home/addons/plugin.video.moviezoot/fanart.jpg'

local_string = xbmcaddon.Addon(id='plugin.video.moviezoot').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]
mode = 110

#110
def mz_genres(url):	
        html = get_html('http://moviezoot.com')
        genres = re.compile('<div class="list-item-container"><a href="(.+?)"><img src="(.+?)"').findall(html)
        for url, image in genres:
            url = 'http://moviezoot.com' + str(url)[:-1]
            title = url.replace('-',' ').split('/',4)[-1].title()
            image = 'http://moviezoot.com' + str(image)
            add_directory2(title,url,111, defaultfanart ,image,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        add_directory2('Binge Watching','http://moviezoot.com/binge-watching/',112, defaultfanart ,defaulticon,plot='Got some time to kill? How about binge watching some free streaming outstanding comedies from the past?  Or how about some great mysteries? Or documentaries?')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#111
def mz_movies(url):	
        html = get_html(url)
        movies = re.compile('<div class="list-item-container"><a href="(.+?)"><img alt="(.+?)" title="(.+?) />').findall(html)
        for url, title, image in movies:
	    image = re.compile('src="(.+?)"').findall(image)[0]
            #print 'MZ Title= ' + str(title)
            #print 'MZ Image= ' + str(image)
            #print 'MZ URL= ' + str(url)
            html = get_html(url)
            url = re.compile('"file":"(.+?)"').findall(html)[0]
            year = re.compile('Released: <strong>(.+?)</').findall(html)[0]
            qname = title.replace(' ', '+')
            print 'QNAME= ' + str(qname)
            try: response = urllib2.urlopen(apiURL + '?t=' + qname + '&y=' + year + '&plot=full&r=json')
            except urllib2.URLError as e:
                print type(e)    #not catch
            except socket.timeout as e:
                print type(e)
                xbmcgui.Dialog().ok(addonname, 'Timeout Error - Please Try Again')
                return
            jgdata = json.load(response)
            try:plot = unicode(jgdata['Plot'])
            except KeyError:
                continue
            if 'N/A' in plot:
                plot = 'No description available.'
            try:actors = unicode(jgdata['Actors'])
            except KeyError:
                pass
            #actors = '[\'' + actors.replace(', ','\', \'') + '\']'
	    actors = actors.split(",")
	    #print 'Actors= ' + str(actors)
            try:runtime = unicode(jgdata['Runtime'])
            except KeyError:
                continue
            if 'N/A' in runtime:
                runtime = ''
            plot = plot + '\n\n' + runtime
            runtime = runtime.replace(' min','')
            infoLabels = {'title':title,
                          'tvshowtitle':title,
                          'plot':plot,
			  'cast':actors,
                          'duration':runtime}

            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setInfo(type="Video", infoLabels=infoLabels)
            li.setProperty('fanart_image',  defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=40)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


def mz_binge(url):
        html = get_html(url)
        binge = re.compile('<div class="list-item-container"><a href="(.+?)"><img class="alignnone size-full wp-image-217" src="(.+?)" alt="(.+?)"').findall(html)
        #print 'Binge= ' + str(binge)
        for url, image,title in binge:
            url = 'http://moviezoot.com' + str(url)[:-1]
            title = title.lstrip().replace('Binge Watching ','').split(' - ')[0]
            url = url + ',' + image
            add_directory2(title,url,113, defaultfanart ,image,plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


def mz_episodes(url): 
        eurl = url.split(',')[0]
        image = url.split(',')[-1]       
	html = get_html(eurl)
        if 'marx' in eurl:
            episodes = re.compile('<div class="list-item-container"><a href="(.+?)"><img alt="(.+?)"').findall(html)
	else:
            episodes = re.compile('<li><a href="(.+?)">(.+?)</a>').findall(html)
	#print 'Episodes= ' + str(episodes)
        #try: image = re.compile('<div class="binge-image-list-container"><img src="(.+?)"').findall(html)[0]
	#except IndexError:
            #image = thumbnail
        #print 'Image= ' + str(image)
        for url, title in episodes:
	    html = get_html(url)
            url = re.compile('"file":"(.+?)"').findall(html)
	    url = str(url)[2:-2]
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            #li.setInfo(type="Video", infoLabels=infoLabels)
            li.setProperty('fanart_image',  defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=30)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[6])+")")
        xbmcplugin.endOfDirectory(addon_handle)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=10)
        return ok

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
        print "MovieZoot Genres"
	mz_genres(url)
elif mode == 1:
        print "Indexing Videos"
        INDEX(url)
elif mode == 4:
    print "Play Video"

elif mode==100:
        print "search"
        doSearch(url)
elif mode==110:
        print "MovieZoot Genres"
	mz_genres(url)
elif mode==111:
        print "MovieZoot Movies"
	mz_movies(url)
elif mode==112:
        print "MovieZoot Binge"
	mz_binge(url)
elif mode==113:
        print "MovieZoot Episodes"
	mz_episodes(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
