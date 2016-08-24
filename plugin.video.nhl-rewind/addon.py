#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
import time
import datetime
from datetime import date, timedelta
from datetime import date, datetime, timedelta as td
from bs4 import BeautifulSoup
import HTMLParser
import simplejson as json
#import xml.etree.ElementTree as ET
from urllib import urlopen
import socket
import requests
import cookielib
from cookielib import CookieJar
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler

#today = datetime.date.today()
#today = today.strftime("%m/%d")
#days7 = date.today() - timedelta(days=7)
#day7 = days7.strftime("%m/%d")

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}

time_var = str(int(round(time.time()*1000)))
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.nhl-rewind')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.nhl-rewind")
addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
ADDON_PATH_PROFILE = xbmc.translatePath(addon.getAddonInfo('profile'))

defaultimage = 'special://home/addons/plugin.video.nhl-rewind/icon.png'
defaultfanart = 'special://home/addons/plugin.video.nhl-rewind/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.nhl-rewind/icon.png'
defaulticon = 'special://home/addons/plugin.video.nhl-rewind/icon.png'
fanart = 'special://home/addons/plugin.video.nhl-rewind/fanart.jpg'
artbase = 'special://home/addons/plugin.video.public-domain/resources/media/'


local_string = xbmcaddon.Addon(id='plugin.video.nhl-rewind').getLocalizedString
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508]

def CATEGORIES():
    mode = 1

    addDir('NHL.tv', 'https://www.nhl.com/video/', 16, defaultimage)
    #addDir('Fox Sports', 'http://feed.theplatform.com/f/BKQ29B/foxsports-all?byCustomValue={primary}{nhl}&sort=pubDate|desc&form=rss&range=1-18', 50, defaultimage)
    addDir('Fox Sports', 'http://feed.theplatform.com/f/BKQ29B/foxsports-all?byCustomValue={primary}{nhl}&sort=pubDate|desc&form=rss&range=1-18', 51, defaultimage)
    addDir('NBC Sports', 'http://www.nbcsports.com/video/league/nhl', 89, defaultimage)
    addDir('MSG Network', 'http://www.msgnetworks.com/teams/rangers.html', 80, defaultimage)
    addDir('SportsNet.ca', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 20, defaultimage)
    addDir('ESPN', 'http://espn.go.com/video/format/libraryPlaylist?categoryid=2459791', 90, defaultimage)
    addDir('Comcast SportsNet', 'http://feeds.the-antinet.com/nhl/csn', 95, defaultimage)
    addDir('All Teams', 'https://www.nhl.com/info/teams', 30, defaultimage)
    #addDir('Game Recaps', 'http://feeds.the-antinet.com/nhl/csn', 99, defaultimage)
    #addDir('Full Game Replays', 'http://feeds.the-antinet.com/nhl/nhlfull.xml', mode, defaultimage)
    #addDir('Condensed Games', 'http://feeds.the-antinet.com/nhl/nhlsched.xml', mode, defaultimage)
    #addDir('Hockey Fights', 'http://feeds.the-antinet.com/nhl/hockeyfights.xml', mode, defaultimage)
    ##addDir('FC Hockey Fights', 'http://feeds.the-antinet.com/movies/yt/ytfcfightlog.php', 52, defaultimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#30
def teams(url):
	print url
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all(attrs={'class': 'ticket-team_name h3'}):
	    city = item.find('span',{'class':'team-city'}).text.encode('utf-8')
	    team = item.find('span',{'class':'team-name'}).text.encode('utf-8')
	    title = city + ' ' + team
	    url = 'http://www.nhl.com/' + team.lower() + '/video'
	    add_directory2(title, url, 31, defaultfanart, defaultimage,plot='')
	print url
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#31
def team_sub(url):
	print url
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all(attrs={'class': 'section-banner__tray-item'}):
	    title = item.find('a').text.encode('utf-8')
	    url = 'http://www.nhl.com' + item.find('a')['href']
	    add_directory2(title, url, 32, defaultfanart, defaultimage,plot='')
	print url
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#32
def team_sub2(url):
	print url
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	keys = re.compile('data-asset-id="(.+?)"').findall(str(html))
        for key in keys:
	    url = 'http://nhl.bamcontent.com/nhl/id/v1/' + key + '/details/web-v1.json'
            response = urllib2.urlopen(url)
            nhldata = json.load(response)
	    title = str(nhldata["title"])
	    add_directory3(title, url, 12, defaultfanart, defaultimage,plot='')
	print url
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#51
def fox_sports2(url):
	s = requests.Session()
	r = s.get(url, headers=headers)
	print r.cookies.values()
	print r.cookies
	html = (r.text.encode('utf-8'))
        html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('item'):
            title = str(item.find('title'))[7:-8]
	    item = str(item)
	    smilurl = (re.compile('url="(.+?)" width').findall(item)[0]) + ''
	    images = re.compile('img(.+?)"').findall(item)
	    for item in images:
	        if '849x478' in item:
	            image = 'http://fsvideoprod.edgesuite.net/img' + str(item)
		else:
	            pass
	    smil = get_html(smilurl)
	    stream = (re.compile('<video src="(.+?)"').findall(smil)[0]).split('.mp4')[0] 
	    streamurl = 'http://fsvideoprod.edgesuite.net/' + stream.split('/z/')[-1] + '.mp4'
	    #print 'Image= ' + str(image)
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)      
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li, totalItems=18)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)



#89
def nbcsn_nhl(url):
        html = get_html(url)
	titles = re.compile('\\{"title":"(.+?)"').findall(str(html))
	print len(titles)
	keys = re.compile('pid":"(.+?)"').findall(str(html))
	print len(keys)
        for title, key in zip(titles, keys):
	    title = title.replace("\u0027", "'")
            smil = 'http://link.theplatform.com/s/BxmELC/media/' + str(key)
	    add_directory3(title, smil, 91, defaultfanart, defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
  

#91
def nbcsn_smil(name,url):
	html = get_html(url)
	#print html
	link = (re.compile('\\n(.+?)\\?').findall(str(html))[0]).split('index')[0] + 'master.m3u8'
	print link
	listItem = xbmcgui.ListItem(path=str(link))
	#listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#80
def msg_cat():
        addDir('MSG: Rangers', 'http://www.msgnetworks.com/teams/rangers.html', 84, artbase + 'msgnyr.jpg')
        addDir('MSG: Islanders', 'http://www.msgnetworks.com/teams/islanders.html', 84, artbase + 'msg.jpg')
        #addDir('MSG: Sabres', 'http://www.msg.com/content/msgsite/en/videos.1.html?tag=Buffalo-Sabres', 81, artbase + 'msg.jpg')
        addDir('MSG: Devils', 'http://www.msgnetworks.com/teams/devils.html', 84, artbase + 'msgnjd.jpg')


#84
def msg_network(url):
	msgbase = 'http://cdn.msgnetwork.com'
	html = get_html(url)
	if 'rangers' in url:
	    titles = re.compile('data-alt="(.+?)"').findall(str(html))[41:59]
	elif 'islanders' in url:
	    titles = re.compile('data-alt="(.+?)"').findall(str(html))[39:51]
	elif 'devils' in url:
	    titles = re.compile('data-alt="(.+?)"').findall(str(html))[43:52]
	keys = re.compile('data-id="(.+?)"').findall(str(html))
	images = re.compile('data-thumbnailUrl="(.+?)"').findall(str(html))
	for title, key, image in zip(titles, keys, images):
	    smil = 'http://feed.theplatform.com/f/TZlbt/raiMSG1-akamai/?form=rss&byId=' + key
	    html = get_html(smil)
	    url = re.compile('url="(.+?)"').findall(str(html))[0]
	    image = msgbase + image + '/jcr:content/renditions/cq5dam.thumbnail.640.360.png'
	    add_directory3(title, url, 85, image, image, plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#85
def msg_smil(name,url):
	html = get_html(url)
	url = re.compile('<video src="(.+?)"').findall(html)[0]
	#print 'SMIL URL= ' + str(url)
	listItem = xbmcgui.ListItem(path=str(url))
	#listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


def play_url(url):
	print 'URL= ' + str(url)
	xbmc.Player().play( url )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#16
def nhl_all(url):
	print url
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all(attrs={'class': 'section-banner__tray-item'}):#[37:54]:
	    link = item.find('a')['href']
	    if len(link) < 1:
		continue
	    title = item.find('a').text.encode('utf-8')
	    key = ((item.find('a')['href']).split('-'))[-1]
	    url = 'https://search-api.svc.nhl.com/svc/search/v2/nhl_global_en/topic/' + key + '?page=1&sort=new&type=video&hl=true&expand=image.cuts.640x360%2Cimage.cuts.1136x640'
            add_directory2(title,url,11, defaultfanart,defaultimage,plot='')
	print url
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def get_cookies(url):
    #Create a CookieJar object to hold the cookies
    cj = cookielib.CookieJar()
    #Create an opener to open pages using the http protocol and to process cookies.
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

    #create a request object to be used to get the page.
    req = Request(url)
    f = opener.open(req)

    #see the first few lines of the page
    html = f.read()
    print html[:50]

    #Check out the cookies
    print "the cookies are: "
    for cookie in cj:
        print cookie


#14
def date_generator():
	thisday = datetime.now()
        week_ago = str(thisday - td(days=8)).split(' ')[0]
	print 'week_ago= ' + str(week_ago)
	today = str(datetime.utcnow() - td(hours=5)).split(' ')[0]
	print 'today= ' + str(today)
	current = datetime.utcnow() - td(hours=5)
	year = (today)[:4]
	month = (today)[5:7]
	day = (today)[8:10]
	year2 = (week_ago)[:4]
	month2 = (week_ago)[5:7]
	day2 = (week_ago)[8:10]
	d2 = date(int(year), int(month), int(day))
	d1 = date(int(year2), int(month2), int(day2))
	delta = d2 - d1
	for i in range(delta.days - 1, 0, -1):
	    gamedate = str(d1 + td(days=i))
	    url = 'http://statsapi.web.nhl.com/api/v1/schedule?date='+gamedate+'&expand=schedule.game.content.media.epg,schedule.teams'
	    print 'game url= ' + str(url)
	    s = gamedate.replace('-','')
	    title = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
	    title = title.strftime("%A %B %d, %Y")
	    title = str(title.replace(' 0', ' '))
            add_directory2(title,url,99, defaultfanart,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#11
def nhl_video(url):
	nextlink = (url.split('?'))[0]
	print nextlink
	page = (url.split('=')[1])
	page = int(page.split('&')[0]) + 1
	print page
        response = urllib2.urlopen(url)
        nhldata = json.load(response)
        i=0
        for video in nhldata["docs"]:
            title = str(nhldata["docs"][i]["title"])
            asset_id = str(nhldata["docs"][i]["asset_id"])
	    url = 'http://nhl.bamcontent.com/nhl/id/v1/' + asset_id +'/details/web-v1.json'
            infoLabels = {'title':title}
            image = (nhldata["docs"][i]["image"]["cuts"]["1136x640"]["src"])
	    #print image
            i = i + 1
	    add_directory3(title,url,12, image ,image,plot='')
	nextpage = nextlink + '?page=' + str(page)# + '/new/video///false/'
	add_directory2('Next 10 Videos', nextpage, 11, defaultfanart, defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#12
def nhl_stream(name,url):
        response = urllib2.urlopen(url)
        vid_data = json.load(response)
	url = (vid_data["playbacks"][4]["url"]).replace('master_wired60.m3u8','asset_5000k.m3u8')
	listItem = xbmcgui.ListItem(path=str(url))
	#listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#90
def espn_nhl(url):
        html = get_html(url)
        match=re.compile('<img src="(.+?)" width="134" height="75" /></a><h5>(.+?)</h5>').findall(html)
        for image,title in match:     
            video = image.replace('a.espncdn.com/media', 'media.video-cdn.espn.com')
            if QUALITY !='0':
	        video = video.replace('.jpg', '_nolbr.m3u8')
            else:
	        video = video.replace('.jpg', '.mp4')            
            li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
            li.setProperty('fanart_image',  defaultfanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=video, listitem=li, totalItems=10)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#20
def sportsnet():
    addDir('Hockey News', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 21,
           defaultimage)
    addDir('Game Highlights', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 22,
           defaultimage)
    addDir('NHL Top Plays', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 23,
           defaultimage)
    addDir('Hockey Central', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 24,
           defaultimage)


#21
def sn_video(url):
            i = 0
            html = get_html(url)
	    soup = BeautifulSoup(html,'html.parser')
            for item in soup.find_all(attrs={'class': 'thumbnail'})[0:18]:
	        url = item.find('a')['href']
		i = i + 1
                html = get_html(url)
                match=re.compile('twitter:title" content="(.+?)">\n<meta name="twitter:image:src" content="(.+?)">\n<meta name="twitter:player" content="(.+?)&').findall(html)
                for title,image,video in match:
                    title = title.replace('&amp;','&').replace("&#8217;","'")
                    video = video.split('=',1)[-1]
                    url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' +str(video)
                    print 'Video= ' + str(video)
                    li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
                    li.setProperty('fanart_image',  image)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
                    xbmcplugin.setContent(pluginhandle, 'episodes')
                xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")



#22
def sn_highlights(url):
            html = get_html(url)
	    soup = BeautifulSoup(html,'html.parser')
            for item in soup.find_all(attrs={'class': 'thumbnail'})[19:36]:
	        url = item.find('a')['href']
                html = get_html(url)
                match=re.compile('twitter:title" content="(.+?)">\n<meta name="twitter:image:src" content="(.+?)">\n<meta name="twitter:player" content="(.+?)&').findall(html)
                for title,image,video in match:
                    title = title.replace('&amp;','&').replace("&#8217;","'")
                    video = video.split('=',1)[-1]
                    url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' +str(video)
                    print 'Video= ' + str(video)
                    li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
                    li.setProperty('fanart_image',  image)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
                    xbmcplugin.setContent(pluginhandle, 'episodes')
                xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#23
def sn_top(url):
            html = get_html(url)
	    soup = BeautifulSoup(html,'html.parser')
            for item in soup.find_all(attrs={'class': 'thumbnail'})[37:54]:
	        url = item.find('a')['href']
                html = get_html(url)
                match=re.compile('twitter:title" content="(.+?)">\n<meta name="twitter:image:src" content="(.+?)">\n<meta name="twitter:player" content="(.+?)&').findall(html)
                for title,image,video in match:
                    title = title.replace('&amp;','&').replace("&#8217;","'")
                    video = video.split('=',1)[-1]
                    url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' +str(video)
                    print 'Video= ' + str(video)
                    li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
                    li.setProperty('fanart_image',  image)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
                    xbmcplugin.setContent(pluginhandle, 'episodes')
                xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#24
def sn_hc(url):
            html = get_html(url)
	    soup = BeautifulSoup(html,'html.parser')
            for item in soup.find_all(attrs={'class': 'thumbnail'})[55:72]:
	        url = item.find('a')['href']
                html = get_html(url)
                match=re.compile('twitter:title" content="(.+?)">\n<meta name="twitter:image:src" content="(.+?)">\n<meta name="twitter:player" content="(.+?)&').findall(html)
                for title,image,video in match:
                    title = title.replace('&amp;','&').replace("&#8217;","'")
                    video = video.split('=',1)[-1]
                    url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' +str(video)
                    #print 'Video= ' + str(video)
                    li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
                    li.setProperty('fanart_image',  image)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
                    xbmcplugin.setContent(pluginhandle, 'episodes')
                xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


def csn_cat(url):
        addDir('Bay Area', 'http://www.csnbayarea.com/show/sharks', 96, defaultimage)
        addDir('Chicago', 'http://feed.theplatform.com/f/VHZQDC/7VkEePgNHeD1?form=json', 94, defaultimage)
        addDir('Philadelphia', 'http://www.csnphilly.com/philadelphia-flyers', 97, defaultimage)

#97
def csn_phi(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all(attrs={'class': 'vod-content__event'}):
	    title = item.find('span', {'class':'media-thumb__title'}).text.encode('utf-8')
	    url = 'http://www.csnphilly.com' + item.find('a')['href']
	    html = get_html(url)
	    soup = BeautifulSoup(html,'html.parser')
	    link = (soup.find('meta', attrs={'name':'twitter:player:stream'})['content'])
	    image = (soup.find('meta', attrs={'property':'og:image'})['content'])
	    #html = get_html(link)
	    url = (get_redirected_url(link)).replace('LOWVIDEO','BESTVIDEO3').replace('300k','1400k')
            li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
            li.setProperty('fanart_image',  image)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
            xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


def get_redirected_url(url):
	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
	request = opener.open(url)
	#print 'Redirect' + str(request.url)
	#playthis = (request.url).replace('300k','2200k')
	#play(playthis)
	return request.url


#94
def csn_chi(url):
        response = urllib2.urlopen(url)
        msgdata = json.load(response)
        i=0
	#while i < 100:
        for title in msgdata["entries"]:
            i = i + 1
	    try: image = (msgdata["entries"][i]["plmedia$defaultThumbnailUrl"])
	    except IndexError:
		continue
            try: title = str(msgdata["entries"][i]["title"])
	    except UnicodeError:
		continue
	    if 'Blackhawks' in title:
		pass
	    else:
		continue
            smil = (msgdata["entries"][i]["media$content"][0]["plfile$url"]).split('?')[0]
	    mediatype = (msgdata["entries"][i]["media$categories"][0]["media$name"])
	    add_directory3(title,smil,87, image ,image,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#87
def csnchi_smil(name,url):
        html = get_html(url)
	url = re.compile('http(.+?)m3u8').findall(html)[0]
	print 'SMIL URL= ' + str(url)
	url = 'http' + str(url) + 'm3u8'
	listItem = xbmcgui.ListItem(path=str(url))
	#listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#96
def csn_nhl(url):
        html = get_html(url)
        if 'philly' in url:
            i = 1
        else:
            i = 0
        while i < 15:
            try:title=re.compile('<a href="/show(.+?)">(.+?)</a>').findall(html)[i]
            except IndexError:
                continue
            title = title[-1].replace('&#039;',"'")
            videokey=re.compile('media-theplatform/(.+?).jpg').findall(html)[i]
            print 'videokey= ' + str(videokey)
            smil = 'http://link.theplatform.com/s/pcPFDC/' + str(videokey)
	    print 'videolink= ' + str(smil)
            i = i + 1
	    add_directory3(title,smil,86, defaultfanart ,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        



def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')


    #retries = 0
    #while retries < 2:

    try:
        response = urllib2.urlopen(req, timeout=60)
        html = response.read()
        response.close()
    except urllib2.HTTPError:
        response = False
        html = False
        #retries = retries + 1
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


def add_directory3(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        liz.setProperty('IsPlayable', 'true')	
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=20)
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
elif mode == 2:
	print "Indexing Replay by Sport"
	REPLAYBYSPORT(url)
elif mode == 4:
    print "Play Video"
elif mode == 10:
    print "Get NHL Categories"
    nhl_cat()
elif mode == 11:
    print "Get NHL Highlights"
    nhl_video(url)
elif mode == 12:
    print "Get NHL Stream"
    nhl_stream(name,url)
elif mode == 14:
    print "Get Dates"
    date_generator()
elif mode == 15:
    print "Get NHL Replays"
    nhl_replays(url)
elif mode == 16:
    print "Get All NHL Video"
    nhl_all(url)
elif mode == 20:
    print "Get SN Categories"
    sportsnet()
elif mode == 21:
    print "Get SN Videos"
    sn_video(url)
elif mode == 22:
    print "Get SNH Videos"
    sn_highlights(url)
elif mode == 23:
    print "Get SN Top Videos"
    sn_top(url)
elif mode == 24:
    print "Get SN HC Videos"
    sn_hc(url)
elif mode == 30:
    print "Get NHL Teams"
    teams(url)
elif mode == 31:
    print "Get NHL Team SubMenu"
    team_sub(url)
elif mode == 32:
    print "Get NHL Team SubMenu2"
    team_sub2(url)
elif mode == 51:
    print "Get Fox Sports NHL Videos"
    fox_sports2(url)
elif mode == 52:
    print "Get Hockey Fights"
    hockey_fights(url)
elif mode == 80:
    print "Get MSG Teams"
    msg_cat()
elif mode == 84:
    print "Get MSG Network"
    msg_network(url)
elif mode == 85:
    print "Get MSG SMIL"
    msg_smil(name,url)
elif mode == 87:
    print "Get CSNCHI SMIL"
    csnchi_smil(name,url)
elif mode == 89:
    print "Get NBC Sports NHL Video"
    nbcsn_nhl(url)
elif mode == 91:
    print "Get NBC Sports SMIL"
    nbcsn_smil(name,url)
elif mode == 90:
    print "Get ESPN NHL Video"
    espn_nhl(url)
elif mode == 94:
    print "Get CSN Chicago"
    csn_chi(url)
elif mode == 95:
    print "Get CSN Cities"
    csn_cat(url)
elif mode == 96:
    print "Get CSN Video"
    csn_nhl(url)
elif mode == 97:
    print "Get CSN Philly Video"
    csn_phi(url)
elif mode == 99:
    print "Get Game Recaps"
    game_recaps(url)
elif mode==100:
        print "PlayURL"
	play_url(url)
elif mode==101:
        print "Get Cookies"
	get_cookies(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


