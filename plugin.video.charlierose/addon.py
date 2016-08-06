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

artbase = 'special://home/addons/plugin.video.charlierose/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.charlierose')
self = xbmcaddon.Addon(id='plugin.video.charlierose')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.charlierose")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Charlie Rose"

defaultimage = 'special://home/addons/plugin.video.charlierose/icon.png'
defaultfanart = 'special://home/addons/plugin.video.charlierose/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.charlierose/icon.png'
baseurl = 'https://www.charlierose.com'

local_string = xbmcaddon.Addon(id='plugin.video.charlierose').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]


#10
def cats(url):
	response = get_html(baseurl)
	soup = BeautifulSoup(response,'html5lib').find_all('nav',{'id':'menu'})
	match = re.compile('href="(.+?)">(.+?)</').findall(str(soup))
	for url, title in match[:-2]:
	    if title == 'More':
		continue
	    if title == 'Collections':
		mode = 11
	    elif title == 'Episodes':
		mode = 12
	    elif title == 'Guests':
		mode = 15
	    else:
		mode = 20
	    #title = item.find('a').string.encode('utf-8').title()
	    url = baseurl + url
	    if 'nofollow' in url:
		continue
	    #duration = item.find('itunes:duration').string.encode('utf-8')
	    image = defaultimage
	    add_directory2(title,url,mode,defaultfanart,defaultimage,plot='')
	#add_directory2('Episodes','http://www.charlierose.com/episodes',12,defaultfanart,defaultimage,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)

#11
def collections(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('ul',{'class':'listing-collections'})
	urls = re.compile('href="(.+?)">').findall(str(soup))
	titles = re.compile('<b>(.+?)</b>').findall(str(soup))
	for url, title in zip(urls, titles):
	    url = 'https://charlierose.com' + url
	    add_directory2(title,url,18,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#12
def years(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('select',{'id':'date_year'})
	years = re.compile('">(.+?)</').findall(str(soup))
	for year in years[1:]:
	    url = 'https://charlierose.com/episodes?date[year]=' + year
	    add_directory2(year,url,13,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#13
def months(url):
	print url
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('select',{'id':'date_month'})
	months = re.compile('">(.+?)</').findall(str(soup)); value = 1
	for month in months[1:]:
	    url = url + '&date[month]=' + str(value); value = value + 1
	    add_directory2(month,url,14,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#14
def episodes(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('ul',{'class':'listing-episodes'})
	days = re.compile('i>(.+?)</').findall(str(soup))
	guests = re.compile('b>(.+?)</').findall(str(soup))
	episodes = re.compile('data-id="(.+?)"').findall(str(soup))
	for day, guest, episode in zip(days, guests, episodes):
	    title = guest + ' (' + day + ')'
	    url = 'https://charlierose.com/video/player/' + episode
	    add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle)


#15
def atoz(url): 
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            name = str(letter)
	    url = 'https://charlierose.com/guests?char=' + name + '&listing_type=az'
            add_directory2(name,url,16,defaultfanart,defaultimage,plot='')    
        xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#16
def guests(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('ul',{'class':'listing-guests'})
	guests = re.compile('b>(.+?)</b').findall(str(soup))
	links = re.compile('href="(.+?)"').findall(str(soup))
	for guest, link in zip(guests, links):
	    url = 'https://charlierose.com' + link
            add_directory2(guest,url,17,defaultfanart,defaultimage,plot='')    
	try:next = ('https://charlierose.com' + re.compile('next" href="(.+?)"').findall(response)[-1]).replace('&amp;','&')
	except IndexError:
	    return
	print next
	add_directory2('Next Page',next,16,defaultfanart,defaultimage,plot='')
        xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#17
def gstreams(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('ul',{'class':'listing-video-full'})
	links = re.compile('href="(.+?)"').findall(str(soup))
	dates = re.compile('Air Date (.+?)</').findall(str(soup))
	images = re.compile('src="(.+?)"').findall(str(soup))
	for link, date, image in zip(links, dates, images):
	    url = 'https://charlierose.com/video/player/' + link.split('/')[-1]
	    add_directory2(date,url,30,defaultfanart,image,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#18
def cvideos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('li',{'class':'video'})
	for item in soup:
	    title = item.find('a')
	    airdate = re.compile('</span>(.+?)\\n').findall(str(title))[-1]
	    title = re.compile('<b>(.+?)</b>').findall(str(title))[-1] + ' (' + airdate + ')'
	    url = 'https://charlierose.com/video/player/' + (item.find('a')['href']).split('/')[-1]
	    print url
	    description = item.find('div',{'class':'over'})
	    image = item.find('img')['src']
	    add_directory2(title,url,30,defaultfanart,image,plot='')#; i = i + 1
	try:next = 'https://charlierose.com' + re.compile('next" href="(.+?)"').findall(response)[-1]
	except IndexError:
	    return
	add_directory2('Next Page',next,18,defaultfanart,defaultimage,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('li',{'class':'video'})
	for item in soup:
	    title = item.find('a')
	    airdate = re.compile('</span>(.+?)\\n').findall(str(title))[-1]
	    title = re.compile('<b>(.+?)</b>').findall(str(title))[-1] + ' (' + airdate + ')'
	    url = ('https://charlierose.com' + item.find('a')['href']).replace('videos', 'video/player')
	    description = item.find('div',{'class':'over'})
	    image = item.find('img')['src']
	    print url
	    add_directory2(title,url,30,defaultfanart,image,plot='')#; i = i + 1
	try:next = 'https://charlierose.com' + re.compile('next" href="(.+?)"').findall(response)[-1]
	except IndexError:
	    return
	add_directory2('Next Page',next,20,defaultfanart,defaultimage,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('source')
	#print soup
	source = re.compile('src="(.+?)"').findall(str(soup))[0]
	#print source
	listitem = xbmcgui.ListItem(name, iconImage=defaultimage, thumbnailImage=defaultimage)
        listitem.setProperty('IsPlayable', 'true')
	#play(url)
	xbmc.Player().play( source, listitem )
	sys.exit()
        xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def play(url):
    print url
    item = xbmcgui.ListItem(path=url)
    item.setProperty('IsPlayable', 'true')
    item.setProperty('IsFolder', 'false')
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), succeeded=True, listitem=item)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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

def addLink(name, url, mode, iconimage, fanart=False, infoLabels=True):
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


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
    cats(url)
elif mode == 4:
    print "Play Video"
elif mode==11:
        print "Charlie Rose Collections"
	collections(url)
elif mode==12:
        print "Charlie Rose Years"
	years(url)
elif mode==13:
        print "Charlie Rose Months"
	months(url)
elif mode==14:
        print "Charlie Rose Episodes"
	episodes(url)
elif mode==15:
        print "Charlie Rose A to Z"
	atoz(url)
elif mode==16:
        print "Charlie Rose Guests"
	guests(url)
elif mode==17:
        print "Charlie Rose Guests"
	gstreams(url)
elif mode==18:
        print "Charlie Rose Collections Videos"
	cvideos(url)
elif mode==20:
        print "Charlie Rose Videos"
	videos(url)
elif mode==30:
        print "Charlie Rose Streams"
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
