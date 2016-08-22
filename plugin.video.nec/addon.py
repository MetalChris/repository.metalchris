#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests  
import urlparse
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import date, datetime, timedelta as td
import m3u8
import os.path

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.nec')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.nec")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "NEC Front Row"

defaultimage = 'special://home/addons/plugin.video.nec/icon.png'
defaultfanart = 'special://home/addons/plugin.video.nec/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.nec/icon.png'
nec = 'special://home/addons/plugin.video.nec/icon.png'

local_string = xbmcaddon.Addon(id='plugin.video.nec').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]

def CATEGORIES():
    #mode = 1
    addDir('Live Events', 'http://necfrontrow.com/', 50, nec)
    #addDir('Live Events', 'http://necfrontrow.com/controlroom.php', 60, nec)
    #addDir('Schedule', 'http://necfrontrow.com/schedule.php', 70, nec)
    addDir('Schedule', 'http://necfrontrow.com/schedule.php', 80, nec)
    #addDir('Archived Events', 'http://necfrontrow.com/fullevent.php', 39, nec)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#80
def date_generator():
	today = str(datetime.utcnow() - td(hours=5)).split(' ')[0]
	print 'today= ' + str(today)
	current = datetime.utcnow() - td(hours=5)
	date2 = str(current + td(days=10)).split(' ')[0]
	#date2 = date2.split('-')
	print 'date2= ' + str(date2)
	year = (today)[:4]
	month = (today)[5:7]
	day = (today)[8:10]
	year2 = (date2)[:4]
	month2 = (date2)[5:7]
	day2 = (date2)[8:10]
        url = 'http://necfrontrow.com/schedule.php'
	d1 = date(int(year), int(month), int(day))
	d2 = date(int(year2), int(month2), int(day2))
	#d2 = date(2016, 2, 29)
	delta = d2 - d1
	for i in range(delta.days + 1):
	    title = str(d1 + td(days=i))
	    s = title.replace('-','')
	    title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
	    title = title.strftime("%B %d, %Y")
	    title = str(title.replace(' 0', ' '))
            add_directory2(title,url,70, defaultfanart,nec,plot='')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#70
def nec_schedule(name, url):
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('tr'):
            #print 'Item= ' + str(item)
            for link in item.find_all('a'):
                url = link.get('href')
		title = str(url)
	        if 'Date' in item:
		    pass
                item = str(item)
	        item = item.split('</td>')
		edate = item[0].split('>',-1)[-1]
		edate = edate.split(',', 1)[-1]
		#print edate
		sport = item[1].split('>',-1)[-1]
		event = item[2].replace('\n<td valign="top">', '')[:-12]
		etime = item[3].split('\n', -1)[-1].upper()
		#title = str(edate) + ' '+ str(etime) + ' - ' + str(event) + ' (' + str(sport) + ')'
		title = str(etime) + ' - ' + str(event) + ' (' + str(sport) + ')'
		#print 'Edate= ' + str(edate)
		#print 'Name= ' + str(name)
		if str(name) in str(edate):
                    li = xbmcgui.ListItem(title, iconImage=defaultimage, thumbnailImage=defaultimage)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
                xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)


#60
def nec_control(url):
	path = _addon_path
	filename = 'nec.m3u8'
        addon_handle = int(sys.argv[1])
        html = get_html(url)
	match = re.compile('<p class="headcat3XX">(.+?)<b>(.+?)</b><br /><a href="(.+?)" target').findall(html)
        for sport, event, url in match:
	    title = str(sport) + str(event)
	    h = HTMLParser.HTMLParser()
	    title = h.unescape(title)
	    #url = 'http://necfrontrow.com/webcast' + str(url)	
	    #print 'Live URL= ' + str(url)
            html = get_html(url)
	    try : iframe = 'http:' +  re.compile('<iframe src="(.+?)" width').findall(html)[0]
	    except IndexError:
		continue
	    #print 'iframe= ' + str(iframe)
            html = get_html(iframe)
	    try: streamurl = re.compile('rtsp_url":"(.+?)",').findall(html)[0]
	    except IndexError:
		continue
	    try: image = re.compile('"thumbnail_url":"(.+?)","').findall(html)[0]
	    except IndexError:
		continue
	    try: smil = re.compile('"play_url":"(.+?)","').findall(html)[0]
	    except IndexError:
		continue
	    #print 'SMIL= ' + str(smil)
	    bw = re.compile('bitrate":(.+?),"').findall(html)[-1].replace('000','')
	    m3u8url = re.compile('secure_m3u8_url":"(.+?)","').findall(html)[0]
            m3u8content = get_html(m3u8url)
	    completeName = os.path.join(path, filename)
	    s = str(m3u8content)
	    f = open(completeName, 'wb')
	    f.write(s)
	    print 'M3U8URL= ' + str(m3u8url)
	    #testfile = urllib.URLopener()
	    #testfile.retrieve(m3u8url, "stream.m3u8")
	    print 'STREAMURL= ' + str(streamurl)
            m3u8content = get_html(m3u8url)
	    #print 'M3U8 Content= ' + str(m3u8content)
	    f = open('streamurl.m3u8','w')
	    f.write(m3u8content) # python will convert \n to os.linesep
	    f.close()
	    #soup = BeautifulSoup(html, 'html.parser')
            html = get_html(smil)
	    soup = BeautifulSoup(html, 'html.parser')
	    #print 'SMIL Content= ' + str(soup)
	    #content = soup.find_all('meta')[0]['title']
	    #httpbase = soup.find_all('meta')[1]['httpBase']
	    #print 'SMIL Content= ' + str(html)
	    #httpbase = re.compile('<meta name="httpBase" content="(.+?)"/>').findall(html)
	    #print 'httpbase= ' + str(httpbase)
	    content = re.compile('<switch id="(.+?)">').findall(html)[0]
	    key = re.compile('@(.+?)" ').findall(html)[-1]
	    #bw = re.compile('system-bitrate="(.+?)"></video>').findall(html)
	    #print 'bw= ' + str(bw)
	    #if len(bw)>1:
		#bw = (bw)[-1]
	    #print 'content= ' + str(content)
	    #print 'key= ' + str(key)
	    #print 'bw= ' + str(bw)#.replace('000','')
	    akstreamurl = 'http://livestream-f.akamaihd.net/i/' + str(content) + '@' + str(key) + '/index_' + str(bw) + '_av-p.m3u8?sd=10&dw=100&rebase=on'
            #m3u8_obj = m3u8.loads(str(m3u8content))  # this could also be an absolute filename
            #print m3u8_obj
            #print m3u8_obj.segments
            #print m3u8_obj.target_duration
	    #print 'StreamURL= ' + str(streamurl)
	    #print 'Akamai StreamURL= ' + str(akstreamurl)
	    #mode = 4
            #add_directory2(title,streamurl,4, defaultfanart,nec,plot='')
	    #m3u8 = _addon_path + '/' + filename
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url='nec.m3u8', listitem=li)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)


def play_url(url):
	r = requests.get(url)
	print r.cookies
        print 'Kookie= ' + str(r.cookies)[54:-3]
	kookie = str(r.cookies)[54:-3]
	#opener = urllib2.build_opener()
	#opener.addheaders.append(('Cookie', kookie))
	#f = opener.open(url)
        #page = f.read()
	play(url)


#50
def nec_live_events(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
	match=re.compile('webcast(.+?)">(.+?)</a>').findall(html)
        for url, title in match:
	    h = HTMLParser.HTMLParser()
	    title = h.unescape(title)
	    url = 'http://necfrontrow.com/webcast' + str(url)	
	    print 'Live URL= ' + str(url)
            html = get_html(url)
	    frame = BeautifulSoup(html,'html.parser').find_all('iframe')
	    print '=========IFRAME ' + str(frame[1])
	    try: iframe =re.compile('src="(.+?)"').findall(str(frame[1]))[0]
	    except IndexError:
		continue
	    print iframe
	    if not  'http:' in iframe:
		iframe =  'http:' +  iframe
	    print 'iframe= ' + str(iframe)
            html = get_html(iframe)
	    if 'livestream' in iframe:
	        try: streamurl = re.compile('m3u8_url":"(.+?)","secure').findall(html)[-1]
	        except IndexError:     
		    continue
	    if 'packnetwork' in iframe:
		try: streamurl = re.compile('src : "(.+?)"').findall(html)[1]
	        except IndexError:     
		    continue
	    if '","' in streamurl:
		streamurl = streamurl.split('","')[0]
		title = '[Replay] ' + title
	    try: image = re.compile('"thumbnail_url":"(.+?)","').findall(html)[0]
	    except IndexError:
		image = defaultfanart
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)


#39
def nec_sports(url,name):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        match=re.compile('<li><a href=\'(.+?)\'><span>(.+?)</').findall(html)
        for url,sport in match:
            if 'ondemand' in url:
                title = sport
                #if '&#8211;' in name:
                #title = title.replace('&#8211;', '-')
                #title = title.replace('&#8217;', '\'')
                title = title.replace('&amp;', '&')
                url = url.replace('ondemand', 'fullevent')
                url = 'http://necfrontrow.com/' + url
                #print 'NEC url= ' + str(url)
                add_directory2(title,url,40, nec,nec,plot='')
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")
        #xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#40
def nec_events(url,name):
        html = get_html(url)
	soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('tr'):
            for link in item.find_all('a'):
                url = link.get('href')
                #print 'URL= ' + str(url)
		title = str(url)
	        if 'Date' in item:
		    pass
                item = str(item)
		#print item
		#itemstrip = striphtml(item).replace('\n', '+')
		#print 'ItemStrip= ' + str(itemstrip)
	        item = item.split('</td>')
		#print item
		edate = item[0].split('>',-1)[-1]
		edate = edate.split(',', 1)[-1]
		#print 'Edate= ' + str(edate)
		sport = item[1].split('>',-1)[-1]
		#print 'Sport= ' + str(sport)
		event = item[2].replace('\n<td>\n   ', '')
		#print 'Event= ' + str(event)
		url = item[3].rpartition('"')[0].partition('"')[-1]
                if not 'http' in url:
		    url = 'http://necfrontrow.com' + str(url)
		#print 'URL= ' + str(url)
		title = str(edate)  + ' - ' + str(event) 
		#title = str(etime) + ' - ' + str(event) + ' (' + str(sport) + ')'

                add_directory2(title,url,41, defaultfanart,nec,plot='')
            #xbmcplugin.addDirectoryItem(handle=addon_handle, url=gurl, listitem=li, totalItems=30)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")
        #xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#41
def nec_stream(url,name):
	path = _addon_path
	filename = 'nec.m3u8'
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        try: match=re.compile('<iframe src="(.+?)" width').findall(html)[0]
	except IndexError:
	    pass
        iframe = match
        #print 'NEC iframe= ' + str(iframe)
        html = get_html(iframe)
        key = re.compile('live_video_post_id":(.+?),"').findall(html)[0]
        print 'Key= ' + str(key)
        match=re.compile('m3u8_url":"(.+?)",').findall(html)
        i=1
        h=1
        for url in match:
            print 'NEC Stream= ' + str(url)
            m3u8content = get_html(url)
	    completeName = os.path.join(path, filename)
	    s = str(m3u8content)
	    f = open(completeName, 'wb')
	    f.write(s)
	    #print 'M3U8 Content= ' + str(m3u8content)
            if key in url:
                title = 'Event Stream' + str(i) + ' - ' + name.split(' - ')[-1]
                i=i+1
            else:
                title = 'Highlight' + str(h) + ' - ' + name.split(' - ')[-1]
                h=h+1
        #item = xbmcgui.ListItem(path=url)
        #return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            li = xbmcgui.ListItem(title, iconImage=nec, thumbnailImage=nec)
        #li.setProperty('fanart_image', defaultfanart)
        #li.setInfo(type="Video", infoLabels=infoLabels)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def play(url):
    item = xbmcgui.ListItem(path=url)
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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
    print "Generate Main Menu"
    CATEGORIES()
elif mode == 1:
    print "Indexing Videos"
    INDEX(url)
elif mode == 4:
    print "Play Video"
    play_url(url)
elif mode == 6:
    print "Get Episodes"
    get_episodes(url)
    atoz(url,name)
elif mode == 39:
    print "Indexing NEC Sports"
    nec_sports(url,name)
elif mode == 40:
    print "Indexing NEC Events"
    nec_events(url,name)
elif mode == 41:
    print "Get NEC Stream"
    nec_stream(url,name)
elif mode == 50:
    print "Get NEC Live Events"
    nec_live_events(url)
elif mode == 60:
    print "Get NEC Control Room"
    nec_control(url)
elif mode == 70:
    print "Get NEC Schedule"
    nec_schedule(name, url)
elif mode == 80:
    print "Get Dates"
    date_generator()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
