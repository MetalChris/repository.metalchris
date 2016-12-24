#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import html5lib
import json
from datetime import date, datetime, timedelta as td

now = str(datetime.utcnow() - td(hours=5)).split(' ')[0]

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.campus-insiders')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.campus-insiders/icon.png'
defaultfanart = 'special://home/addons/plugin.video.campus-insiders/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.campus-insiders/icon.png'
defaulticon = 'special://home/addons/plugin.video.campus-insiders/icon.png'
baseurl = 'http://campusinsiders.com'
ooyala = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/None/'
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Host':'campusinsiders.com','Referer':'https://campusinsiders.com/','Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'
}

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]
plugin = 'Campus Insiders'


def CATEGORIES():
	addDir('Today\'s Events', 'https://campusinsiders.com/wp-json/events/v1/upcoming?date=' + now + '&posts_per_page=100&return_format=playbook', 1, defaultimage)
	addDir('Upcoming', 'https://campusinsiders.com/videos/', 5, defaultimage)
	addDir('Replay', 'https://campusinsiders.com/videos/', 7, defaultimage)
	addDir('Latest Videos', 'https://campusinsiders.com/videos/', 6, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#1
def INDEX(url):
        jresponse = urllib2.urlopen(url)
        jdata = json.load(jresponse);i=0
	item_dict = jdata
	count = len(item_dict['playbook']['live_events']['value'])
	for item in jdata['playbook']['live_events']['value'][0]['scheduled_events']['value']:
	    title = jdata['playbook']['live_events']['value'][0]['scheduled_events']['value'][i]['title']['value']
	    sport = jdata['playbook']['live_events']['value'][0]['scheduled_events']['value'][i]['category']['value']
	    etime = jdata['playbook']['live_events']['value'][0]['scheduled_events']['value'][i]['timestamp']['value']
	    isLive = jdata['playbook']['live_events']['value'][0]['scheduled_events']['value'][i]['isLive']['value']
	    #dtime = (etime.split(' ',1)[-1]).split(' ',1)[0]
	    #print 'dtime= ' + str(dtime)
	    edate = etime.split(' ',1)[0]
	    etime = etime.split(' ',1)[-1].upper().lstrip("0")
	    if isLive != False:
		etime = 'LIVE'
	    url = jdata['playbook']['live_events']['value'][0]['scheduled_events']['value'][i]['permalink']['value']
	    if len(sport) < 1:
	        title = etime + ' - ' + title
	    else:	
	        title = etime + ' - ' + title + ' - ' + sport
	    i=i+1
	    addDir2(title, url, 2, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#2
def IFRAME(name,url):
	name = (name.split(' - '))[1]
        data = get_data(url)
	soup = BeautifulSoup(data,'html5lib').find_all('div',{'class':'video-player--container'})
	for item in soup:
	    iframe = 'http:' + item.find('iframe')['src']
            data = get_data(iframe)
	    try: stream = re.compile('m3u8_url":"(.+?)"').findall(str(data))[-1]
	    except IndexError:
	        xbmcgui.Dialog().notification(name, 'Stream Not Available', defaultimage, 5000, False)
	        sys.exit()
	    listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	    xbmc.Player().play( stream, listitem )
	    sys.exit()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#3
def VIDEOS(url):
        data = get_data(url)
	soup = BeautifulSoup(data,'html5lib').find_all('div',{'class':'video-grid--item'})
	next_page = BeautifulSoup(data,'html5lib').find_all('a',{'class':'pagination--next button'})
	next = str(re.compile('href="(.+?)"').findall(str(next_page)))[2:-2]
	for item in soup[0:15]:
	    if len(str(item)) < 70:
		continue
	    title = sanitize(striphtml(str(item.find('a')))).replace("&#8217;","\'").replace('&#8220;','\"').replace('&#8221;','\"').replace('&amp;','&')
	    url = item.find('a')['href']
	    code = re.compile('data-asset-embed-code="(.+?)"').findall(str(item))[-1]
	    url = ooyala + code + '?device=html5&domain=www.campusinsiders.com'
	    image = item.find('img',{'class':'video-grid-item--media'})['src']
	    if len(image) < 1:
		continue
	    addDir2(title, url, 4, image, image)
	addDir('Next Page', next, 3, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#4
def PLAY_VIDEO(name,url):
        jresponse = urllib2.urlopen(url)
        jdata = json.load(jresponse);i=0
	code = (jdata['authorization_data'].keys())[0]
	item_dict = jdata
	count = len(item_dict['authorization_data'][code]['streams'])
	while i < count:
	    delivery_type = jdata['authorization_data'][code]['streams'][i]['delivery_type']
	    if delivery_type == 'hls':
	        stream = (jdata['authorization_data'][code]['streams'][i]['url']['data']).decode('base64')#.replace('1200','3000')
	    i=i+1
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( stream, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#5
def date_generator():
	today = str(datetime.utcnow() - td(hours=5)).split(' ')[0]
	current = datetime.utcnow() - td(hours=5)
	date2 = str(current + td(days=10)).split(' ')[0]
	year = (today)[:4]
	month = (today)[5:7]
	day = (today)[8:10]
	year2 = (date2)[:4]
	month2 = (date2)[5:7]
	day2 = (date2)[8:10]
	d1 = date(int(year), int(month), int(day))
	d2 = date(int(year2), int(month2), int(day2))
	for i in range(1,13):
	    title = str(d1 + td(days=i))
	    s = title.replace('-','')
	    title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
	    day = title.strftime ("%Y-%m-%d")
	    title = title.strftime("%B %d, %Y")
	    title = str(title.replace(' 0', ' '))
            url = 'https://campusinsiders.com/wp-json/events/v1/upcoming?date=' + day + '&posts_per_page=100&return_format=playbook'
            addDir(title,url,1, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#6
def conferences(url):
	addDir('All Videos', 'https://campusinsiders.com/videos/', 3, defaultimage)
	confs = ['acc','big-12','conference-usa','mwcdn','pac-12','pldn','sec','wccdn']
	titles = ['ACC','Big 12','Conference USA', 'Mountain West','PAC 12','Patriot League','SEC','WCC']
	for conf, title in zip(confs,titles):
	    url = 'https://campusinsiders.com/videos/categories/' + conf + '/'
	    addDir(title, url, 3, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#7
def archives():
	current = datetime.utcnow() - td(hours=5)
	for i in range(1,11):
    	    aday = str(current - td(days=i)).split(' ')[0]
	    s = aday.replace('-','')
	    title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
	    day = title.strftime ("%Y-%m-%d")
	    title = title.strftime("%B %d, %Y")
	    title = str(title.replace(' 0', ' '))
            url = 'https://campusinsiders.com/wp-json/events/v1/upcoming?date=' + aday + '&posts_per_page=100&return_format=playbook'
            addDir(title,url,1, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


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
    req.add_header('Referer','https://campusinsiders.com/')
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')

    try:
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
    except urllib2.HTTPError:
        response = False
        html = False
    return html


def get_data(url):
        req = urllib2.Request(url)
        req.addheaders = [ ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                            ("Accept-Language", "en-US,en;q=0.5"),
                            ("Accept-Encoding", "gzip, deflate, br"),
                            ("Content-type", "text/html; charset=UTF-8"),
                            ("Connection", "keep-alive"),
                            ("Referer", "http://livestream.com/live/"),
                            ("User-Agent",'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36')]

        response = urllib2.urlopen(req)
	data = response.read()
        response.close()
        return data


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
	print "Campus Insiders Menu"
	CATEGORIES()
elif mode == 1:
	print "Campus Insiders Live"
	INDEX(url)
elif mode == 2:
	print "Campus Insiders Play  Live Event"
	IFRAME(name,url)
elif mode == 3:
	print "Campus Insiders Videos"
	VIDEOS(url)
elif mode == 4:
	print "Campus Insiders Play Video"
	PLAY_VIDEO(name,url)
elif mode == 5:
	print "Campus Insiders Upcoming Schedule"
	date_generator()
elif mode == 6:
	print "Campus Insiders Conferences"
	conferences(url)
elif mode == 7:
	print "Campus Insiders Archives"
	archives()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
