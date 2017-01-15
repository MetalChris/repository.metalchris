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
#import simplejson as json
import urlparse

num_digits = 32
myhex = os.urandom(num_digits / 2).encode('hex')
xbmc.log(myhex)

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.asn')
translation = selfAddon.getLocalizedString
#usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.asn/icon.png'
defaultfanart = 'special://home/addons/plugin.video.asn/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.asn/icon.png'
defaulticon = 'special://home/addons/plugin.video.asn/icon.png'
baseurl = 'http://americansportsnet.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]
plugin = 'American Sports Network'


def CATEGORIES():
	addDir('ASN Live Stream', 'http://livevideostatus.sinclairstoryline.com/status/ASN1', 5, defaultimage)
	addDir('Live Schedule', 'http://americanspnet.wpengine.com/schedule-iframe', 3, defaultimage)
	addDir('Featured', 'http://americansportsnet.com/news/video', 1, defaultimage)
	#addDir('Game Archive', 'http://americansportsnet.com/category/game-vault', 1, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#1
def INDEX(url):
	s = requests.Session()
	#s.get('http://www.americansportsnet.com/category/video/')
	r = s.get(url, headers=headers)
	#print(r.text.encode('utf-8'))[0:200]
	#xbmc.log(r.cookies
	html = (r.text.encode('utf-8'))
	soup = BeautifulSoup(html,'html5lib').find_all('a',{'class':'ref-section-card collapsed'})
	for item in soup:
	    title = item.find('h1').text.encode('utf-8')
	    url = 'http://www.americansportsnet.com' + (item.get('href'))
	    image = 'http:' + item.find('img')['data-src']
	    addDir2(title, url, 2, image)
            xbmcplugin.setContent(pluginhandle, 'episodes')
	#next = BeautifulSoup(html,'html5lib').find_all('div',{'class':'nav-previous'})
	#next_url = re.compile('href="(.+?)"').findall(str(next))[-1]
	#addDir('Older Posts', next_url, mode, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#2
def IFRAME(name,url):
        html = get_html(url)
	#soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'embed-container'})[0]
	#iframe = re.compile('src="(.+?)"').findall(str(soup))[-1]
	#xbmc.log('iframe = ' + str(iframe)
	#content = get_html(iframe)
	stream = re.compile("file: '(.+?)'").findall(str(html))[-1]
	xbmc.log('ASN Stream: ' + str(stream))
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( stream, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#3
def LIVE(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('tr')
	for item in soup[1:]:
	    edate = str(re.compile('column-1">(.+?)</').findall(str(item)))[2:-2]
	    if len(edate) <1:
		continue
	    sport = str(re.compile('column-2">(.+?)</').findall(str(item)))[2:-2]
	    hteam = str(re.compile('column-3">(.+?)</').findall(str(item)))[2:-2]
	    #hteam = item.find('td', {'class':'column-3'}).text.strip()
	    ateam = str(re.compile('column-4">(.+?)</').findall(str(item)))[2:-2]
	    #ateam = item.find('td', {'class':'column-4'}).text.strip()
	    etime = str(re.compile('column-5">(.+?)</').findall(str(item)))[2:-2]
	    link = str(re.compile('column-7">(.+?)</').findall(str(item)))[2:-2]
	    if len(link) < 1:
		continue
	    if len(ateam) < 1:
		title = edate + ' [' + etime + ']' + ' - ' + sport + ' - ' + hteam
	    else:
	        title = edate + ' [' + etime + ']' + ' - ' + sport + ' - ' + hteam + ' @ ' + ateam
	    url = baseurl + '/' + link.replace('<!---{','').replace('}--->','')
	    addDir2(title, url, 4, defaultimage)
            xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#4
def LIVE_IFRAME(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'embed-container'})[0]
	iframe = re.compile('src="(.+?)"').findall(str(soup))[-1]
	xbmc.log('iframe = ' + str(iframe))
	if 'sinclair' in iframe:
	    key = (iframe.rpartition('/')[-1]).replace('.html','')
	    xbmc.log(key)
	    jurl = 'http://livevideostatus.sinclairstoryline.com/status/' + key
	    xbmc.log(jurl)
            jgresponse = urllib2.urlopen(jurl)
            jgdata = json.load(jgresponse)
	    jkey = (jgdata['assetId'])
	    xbmc.log(jkey)
	    jstuff = (jgdata['assetSignature'])
	    xbmc.log(jstuff)
	    channel = (jgdata['channelId'])
	    xbmc.log(channel)
	    purl = 'http://content.uplynk.com/preplay/channel/' + channel + '.json'
            jpresponse = urllib2.urlopen(purl)
            jpdata = json.load(jpresponse)
	    stream = (jpdata['playURL'])
	    s = requests.Session()
	    r = s.get(stream, headers=headers)
	    xbmc.log(r)
	    parsed = urlparse.urlparse(stream)
	    xbmc.log('--------' +str(urlparse.parse_qs(parsed.query)['pbs']))
	else:
	    content = get_html(iframe)
	    stream = re.compile("main_url = '(.+?)'").findall(str(content))[-1]
	xbmc.log(stream)
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.Player().play( stream, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#5
def LIVE_STREAM(name,url):
        jresponse = get_purl(url)#urllib2.urlopen(url)
        jdata = json.loads(jresponse)
	isLive = (jdata['isLive'])
	xbmc.log('isLive: ' + str(isLive))
	if str(isLive) != 'False':
	    assetId = (jdata['assetId'])
	    jstuff = (jdata['assetSignature'])
	    purl = 'http://content.uplynk.com/preplay/' + assetId + '.json'
            jpresponse = urllib2.urlopen(purl)
            jpdata = json.load(jpresponse)
	    playURL = (jpdata['playURL'])
	    stream = playURL + '?' + jstuff
	    listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	    xbmc.Player().play( stream, listitem )
	    sys.exit()
	else:                
	    xbmc.log('No Live Broadcast Available')
	    line1 = "Live Stream Currently Unavailable"
	    line2 = "Check the Live Schedule for More Info"
	    xbmcgui.Dialog().ok(plugin, line1, line2)
	    #xbmcgui.Dialog().notification(plugin, 'No Live Broadcast Available.', defaultimage, 5000, False)
	    #sys.exit()
	    LIVE('http://americanspnet.wpengine.com/schedule-iframe')
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
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')

    try:
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
    except urllib2.HTTPError:
        response = False
        html = False
    return html


def get_purl(url):
    req = urllib2.Request(url)
    #req.add_header('Host','livevideostatus.sinclairstoryline.com')
    req.add_header('Referer','http://videobase.sinclairstoryline.com/jwplayer/jwplayer.flash.swf')
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language','en-US,en;q=0.5')
    req.add_header('DNT','1')
    req.add_header('Connection','keep-alive')

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
	xbmc.log("American Sports Network Menu")
	CATEGORIES()
elif mode == 1:
	xbmc.log("American Sports Network Videos")
	INDEX(url)
elif mode == 2:
	xbmc.log("American Sports Network Play Video")
	IFRAME(name,url)
elif mode == 3:
	xbmc.log("American Sports Network Live")
	LIVE(url)
elif mode == 4:
	xbmc.log("American Sports Network Play Live Event")
	LIVE_IFRAME(name,url)
elif mode == 5:
	xbmc.log("American Sports Network Play Live Stream")
	LIVE_STREAM(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
