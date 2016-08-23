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
import cookielib

artbase = 'special://home/addons/plugin.video.carbon-tv/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.carbon-tv')
self = xbmcaddon.Addon(id='plugin.video.carbon-tv')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.carbon-tv")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "CarbonTV"

defaultimage = 'special://home/addons/plugin.video.carbon-tv/icon.png'
defaultfanart = 'special://home/addons/plugin.video.carbon-tv/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.carbon-tv/icon.png'
baseurl = 'https://www.carbontv.com/users/login'

local_string = xbmcaddon.Addon(id='plugin.video.carbon-tv').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
q = settings.getSetting(id="quality")
username = settings.getSetting(id="username")
password = settings.getSetting(id="password")
views = settings.getSetting(id="views")
confluence_views = [500,501,502,503,504,508,515]
values = {'data[User][email]' : username,'data[User][password]' : password,'data[User][remember_me]' : '0', 'data[User][remember_me]' : '1'}


#10
def cats(url):
	data = urllib.urlencode(values)
	cookies = cookielib.CookieJar()
	opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(cookies))
	response = opener.open(baseurl, data)
	page = response.read()
	http_headers = response.info()
	response = opener.open('http://www.carbontv.com/channels', data)
	html = response.read()
	check = re.compile('isLoggedInTest = (.+?);').findall(str(html))
	print check
	if check[0] != 'true':               
	    xbmcgui.Dialog().notification(plugin, 'Login Failed', iconimage, 5000, False)
	    return
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'content-listing channels-listing clearfix'})
	for item in soup:
	    title = item.find('h2').string.encode('utf-8').title()
	    url = 'http://www.carbontv.com' + item.find('a',{'class':'channels-cta'})['href']
	    if 'cams' in url:
		continue
	    image = item.find('img')['src']
	    if 'pbr' in url:
		mode = 11
	    else:
		mode = 15
	    add_directory2(title,url,mode,image,image,plot='')
	#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#11
def pbr(url):
	addDir2('On Demand','http://www.carbontv.com/videos/recent/episodes/limit:0/show_id:88/',20,artbase + 'pbr.jpg')
	addDir2('Highlights','http://www.carbontv.com/videos/recent/clips/limit:0/show_id:88/',20,artbase + 'pbr.jpg')
        xbmcplugin.endOfDirectory(addon_handle)


#15
def shows(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('article',{'class':'content-third content-image-container'})
	for item in soup:
	    title = item.find('h3').string.encode('utf-8').strip()
	    image = item.find('img')['src'] 
	    show_id = image.split('/')
	    url = 'http://www.carbontv.com/videos/recent/episodes/limit:0/show_id:' + show_id[9]
	    add_directory2(title,url,20,image,image,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#20
def videos(url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('article',{'class':'content-quarter content-image-container'})
	for item in soup:
	    title = item.find('h5').string.encode('utf-8').strip()
	    url = 'http://www.carbontv.com' + item.find('a',{'class':'content-image video-link'})['href']
	    duration = striphtml(str(item.find('div',{'class':'thumb-duration'})))#.string.encode('utf-8')
	    image = item.find('img',{'class':'category-image full-image'})['src']
	    add_directory2(title,url,30,image,image,plot='')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#30
def streams(name,url):
	response = get_html(url)
	link = re.compile('<link rel="video_src" href="(.+?)"').findall(str(response))[0]
	print link
	response = get_html(link)
	keys = re.compile('2,"id":"(.+?)"').findall(str(response))
	print keys
	if q =='2':
	    key = keys[-1]
	elif q =='1':
	    key = keys[-4]
	elif q =='0':
	    key = keys[-7]
	thumbnail = (re.compile('thumbnailUrl":"(.+?)"').findall(str(response))[0]).replace('\/','/')
	print thumbnail
	stream = (thumbnail.split('version')[0]).replace('cfvod.kaltura.com','carbonmedia-a.akamaihd.net').replace('thumbnail','serveFlavor') + 'v/2/flavorId/' + key + '/forceproxy/true/name/a.mp4'
	print stream
	listitem = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
	xbmc.Player().play( stream, listitem )
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
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
        print 'CarbonTV PBR'
	pbr(url)
elif mode==15:
	print 'CarbonTV Shows'
	shows(url)
elif mode==20:
        print "CarbonTV Videos"
	videos(url)
elif mode==30:
        print "CarbonTV Streams"
	streams(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
