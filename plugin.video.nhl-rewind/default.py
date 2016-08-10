#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
import time
import datetime
from datetime import date, timedelta
from datetime import date, datetime, timedelta as td
#from BeautifulSoup import BeautifulStoneSoup as Soup
from bs4 import BeautifulSoup
import HTMLParser
import simplejson as json
import xml.etree.ElementTree as ET
#from urllib2 import urlopen
#from lxml import etree
#from pprint import pprint
import socket
import requests
import cookielib
from cookielib import CookieJar
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler

#today = datetime.date.today()
#today = today.strftime("%m/%d")
#days7 = date.today() - timedelta(days=7)
#day7 = days7.strftime("%m/%d")

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

    addDir('NHL.tv', 'https://search-api.svc.nhl.com/svc/search/v1/nhl_global_en/query//tag_content:highlight/1/new/video///false/', 10, defaultimage)
    #addDir('Fox Sports', 'http://feed.theplatform.com/f/BKQ29B/foxsports-all?byCustomValue={primary}{nhl}&sort=pubDate|desc&form=rss&range=1-18', 50, defaultimage)
    addDir('Fox Sports', 'http://feed.theplatform.com/f/BKQ29B/foxsports-all?byCustomValue={primary}{nhl}&sort=pubDate|desc&form=rss&range=1-18', 51, defaultimage)
    addDir('NBC Sports', 'http://www.nbcsports.com/video/league/nhl', 89, defaultimage)
    addDir('MSG Network', 'http://feed.theplatform.com/f/TZlbt/raiMSG1-akamai/?form=json', 85, defaultimage)
    addDir('SportsNet.ca', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 20, defaultimage)
    addDir('ESPN', 'http://espn.go.com/video/format/libraryPlaylist?categoryid=2459791', 90, defaultimage)
    addDir('Comcast SportsNet', 'http://feeds.the-antinet.com/nhl/csn', 95, defaultimage)
    #addDir('Game Recaps', 'http://feeds.the-antinet.com/nhl/csn', 99, defaultimage)
    #addDir('Full Game Replays', 'http://feeds.the-antinet.com/nhl/nhlfull.xml', mode, defaultimage)
    #addDir('Condensed Games', 'http://feeds.the-antinet.com/nhl/nhlsched.xml', mode, defaultimage)
    #addDir('Hockey Fights', 'http://feeds.the-antinet.com/nhl/hockeyfights.xml', mode, defaultimage)
    addDir('FC Hockey Fights', 'http://feeds.the-antinet.com/movies/yt/ytfcfightlog.php', 52, defaultimage)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def msg_network(url):
        response = urllib2.urlopen(url)
        msgdata = json.load(response)
        i=0
        for title in msgdata["entries"]:
	    team = str(msgdata["entries"][i]["media$categories"][0]["media$name"])
	    image = (msgdata["entries"][i]["plmedia$defaultThumbnailUrl"])
            smil = (msgdata["entries"][i]["media$content"][0]["plfile$url"])
            try: title = str(msgdata["entries"][i]["title"])
	    except UnicodeEncodeError:
		continue
            i = i + 1
	    if 'MSG-Networks' in team or 'Knicks' in team or 'Four-Courses' in team:
		continue
	    add_directory3(title,smil,86, image ,image,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def msg_smil(name,url):
        html = get_html(url)
	url = re.compile('<video src="(.+?)"').findall(html)[0].replace('1400', '2200')
	print 'SMIL URL= ' + str(url)
	listItem = xbmcgui.ListItem(path=str(url))
	listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


def play_url(url):
    
	print 'URL= ' + str(url)
	xbmc.Player().play( url )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def hockey_fights(url):
        response = urllib2.urlopen(url)
	soup = BeautifulSoup(response,'html.parser')
        for item in soup.find_all(attrs={'class': 'yt-lockup-title'}):
	    link = item.find_all('a')[0]['href'].split('=')[-1]
	    title = item.find_all('a')[0]['title']
	    url = ('plugin://plugin.video.youtube/?action=play_video&videoid=' + link)
            image = 'http://i.ytimg.com/vi/' + link +'/hqdefault.jpg'
	    infoLabels={ "Title": title} 
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', defaultfanart)
            li.setProperty('IsPlayable', 'true')      
            li.setInfo(type="Video", infoLabels=infoLabels)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.endOfDirectory(addon_handle)
	return



def hockey_fights_old(url):
        response = urllib2.urlopen(url)
	fights = re.compile('</a> <a href="(.+?)"><img').findall(response)
	print fights
	for fight in fights:
	    title = str(fight)
	    url = 'http://www.hockeyfights.com' + title
	    print url
	    html = get_html(url)
	    title = re.compile('title" content="(.+?)" />').findall(html)[-1]

            li = xbmcgui.ListItem(title, iconImage=defaultimage, thumbnailImage=defaultimage)
            li.setProperty('fanart_image', defaultfanart)  
            xbmcplugin.addDirectoryItem(handle=addon_handle, url='', listitem=li, totalItems=18)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def fox_sports2(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('item'):
            title = str(item.find('title'))[7:-8]
	    item = str(item)
	    smilurl = re.compile('url="(.+?)" width').findall(item)[0]
	    images = re.compile('img(.+?)"').findall(item)
	    for item in images:
	        if '849x478' in item:
	            image = 'http://fsvideoprod.edgesuite.net/img' + str(item)
		else:
	            pass
	    smil = get_html(smilurl)
	    streamurl = re.compile('<video src="(.+?)\\?').findall(smil)[0]
	    streamurl = 'http://fsvideoprod.edgesuite.net/' + streamurl.split('/z/')[-1].rsplit('_', 1)[0] + '_3000.mp4'
	    print 'Image= ' + str(image)
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)      
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamurl, listitem=li, totalItems=18)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def nhl_cat():

    addDir('Highlights', 'https://search-api.svc.nhl.com/svc/search/v1/nhl_global_en/query//tag_content:highlight/1/new/video///false/', 11, defaultimage)
    addDir('Game Recaps', 'https://search-api.svc.nhl.com/svc/search/v1/nhl_global_en/query//tag_content:highlight/1/new/video///false/', 14, defaultimage)
    #addDir('Game Replays', 'http://statsapi.web.nhl.com/api/v1/schedule?teamId=&startDate=2016-02-17&endDate=2016-02-17&expand=schedule.teams,schedule.linescore,schedule.game.content.media.epg,schedule.broadcasts&', 15, defaultimage)

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


def nhl_replays(url):

    authorization = ''    
    try:
        cj = cookielib.LWPCookieJar(os.path.join(ADDON_PATH_PROFILE, 'cookies.lwp'))     
        cj.load(os.path.join(ADDON_PATH_PROFILE, 'cookies.lwp'),ignore_discard=True)    

        #If authorization cookie is missing or stale, perform login    
        for cookie in cj:            
            if cookie.name == "Authorization" and not cookie.is_expired():            
                authorization = cookie.value 
		print 'Auth= ' +str(authorization)
	    if cookie.name == "SavedSessionKey" and not cookie.is_expired():
		SessionKey = cookie.value
		print 'SK= ' + str(SessionKey)
    except:
        pass


    if authorization == '':
        #login()
        cj = cookielib.LWPCookieJar(os.path.join(ADDON_PATH_PROFILE, 'cookies.lwp'))     
        cj.load(os.path.join(ADDON_PATH_PROFILE, 'cookies.lwp'),ignore_discard=True)    
        for cookie in cj:            
            if cookie.name == "Authorization":
                authorization = cookie.value 
		print authorization

    r = requests.get(url)
    #print str(r.cookies)
    req = urllib2.Request(url)    
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept', '*/*')
    req.add_header('Origin', 'https://www.nhl.com')
    req.add_header('User-Agent', 'User-Agent=PS4Application libhttp/1.000 (PS4) libhttp/3.15 (PlayStation 4)')
    req.add_header('Referer', 'https://www.nhl.com/tv?&affiliateId=NHLTVLOGIN')
    req.add_header('Accept-Language', 'en-US,en;q=0.8')
    req.add_header('Accept-Encoding', 'deflate')
    response = urllib2.urlopen(req)
    #print response.info
    nhldata = json.load(response)
    response.close()
    i=0
    for replay in nhldata['dates'][0]['games']:
	game_id = replay['gamePk']
        away = replay['teams']['away']['team']['teamName']
        home = replay['teams']['home']['team']['teamName']
        a = replay['teams']['away']['team']['abbreviation']
        h = replay['teams']['home']['team']['abbreviation']
	title = str(away) + ' @ ' + str(home)
        url = replay['content']['media']['epg'][3]['items'][0]['playbacks'][2]['url']
	datecode = url.split('/')
	datecode = datecode[5] + datecode[6] + datecode[7]
	url = url.replace('http://md-akc.med.nhl.com/hls', 'http://hlslive-akc.med2.med.nhl.com/ls04').rsplit('/',3)[0] + '/NHL_GAME_VIDEO_' + a + h + '_M2_VISIT_' + datecode + '/5000K/5000_complete-trimmed.m3u8' + '|User-Agent=PS4Application libhttp/1.000 (PS4) libhttp/3.15 (PlayStation 4)&Cookie=Authorization=' + authorization

	#print url

	content_id = replay['content']['media']['epg'][3]['items'][0]['mediaPlaybackId']
	event_id = replay['content']['media']['epg'][0]['items'][0]['eventId']
	#print gamePk

        epoch_time_now = str(int(round(time.time()*1000)))    
        thisurl = 'https://mf.svc.nhl.com/ws/media/mf/v2.4/stream?eventId='+event_id+'&format=json&platform=WEB_MEDIAPLAYER&subject=NHLTV&_='+epoch_time_now
        #print 'thisurl= ' + str(thisurl)

        req = urllib2.Request(thisurl)       
        req.add_header("Accept", "application/json")
        req.add_header("Accept-Encoding", "deflate")
        req.add_header("Accept-Language", "en-US,en;q=0.8")                       
        req.add_header("Connection", "keep-alive")
        req.add_header("Authorization", authorization)
        req.add_header("User-Agent", 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')
        req.add_header("Origin", "https://www.nhl.com")
	referer = "https://www.nhl.com/tv/" + str(game_id) + "/" + str(event_id) + "/" + str(content_id)
        req.add_header("Referer", referer)

        response = urllib2.urlopen(thisurl)
	print response.info()
        json_source = json.load(response)  
        response.close()
        r = requests.get(thisurl)
        print str(r.cookies)
        i = i + 1    
        li = xbmcgui.ListItem(title, iconImage= defaultimage, thumbnailImage= defaultimage)
        li.setProperty('fanart_image',  defaultfanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
        xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


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


def nhl_video(url):
	page = int(url.split('/')[-7]) + 1
        response = urllib2.urlopen(url)
        nhldata = json.load(response)
        i=0
        for video in nhldata["docs"]:
            title = str(nhldata["docs"][i]["title"])
            asset_id = str(nhldata["docs"][i]["asset_id"])
	    url = 'http://nhl.bamcontent.com/nhl/id/v1/' + asset_id +'/details/web-v1.json'
            infoLabels = {'title':title}
            image = (nhldata["docs"][i]["image"]["cuts"]["1136x640"]["src"])
	    print image
            i = i + 1
	    add_directory3(title,url,12, image ,image,plot='')
	nextpage = 'https://search-api.svc.nhl.com/svc/search/v1/nhl_global_en/query//tag_content:highlight/' + str(page) + '/new/video///false/'
	add_directory2('Next 10 Videos', nextpage, 11, defaultfanart, defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def nhl_stream(name,url):
        response = urllib2.urlopen(url)
        vid_data = json.load(response)
	url = (vid_data["playbacks"][2]["url"])
	listItem = xbmcgui.ListItem(path=str(url))
	listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


def msg_cat():
        addDir('MSG: Rangers', 'http://www.msg.com/content/msgsite/en/videos.1.html?tag=New-York-Rangers', 81, artbase + 'msgnyr.jpg')
        addDir('MSG: Islanders', 'http://www.msg.com/content/msgsite/en/videos.1.html?tag=New-York-Islanders', 81, artbase + 'msg.jpg')
        addDir('MSG: Sabres', 'http://www.msg.com/content/msgsite/en/videos.1.html?tag=Buffalo-Sabres', 81, artbase + 'msg.jpg')
        addDir('MSG: Devils', 'http://www.msg.com/content/msgsite/en/videos.1.html?tag=New-Jersey-Devils', 81, artbase + 'msgnjd.jpg')


def nbcsn_nhl(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all(attrs={'class': 'video-event-thumb'}):
	    url = item.find_all('a')[1]
	    url = url.attrs['href']
	    title = str(item.find_all('span')[2])[44:-7]
            url = 'http://www.nbcsports.com' + str(url)
            html = get_html(url)
            videokey = (re.compile('/select/(.+?)?form').findall(html)[0])[:-1]
            smil = 'http://link.theplatform.com/s/BxmELC/' + str(videokey)
	    add_directory3(title, smil, 91, defaultfanart, defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
  

def nbcsn_smil(name,url):
            html = get_html(url)
	    link = re.compile('http(.+?)&hdntl=').findall(html)[1]
	    vlink = 'http' + link
 	    listItem = xbmcgui.ListItem(path=str(vlink))
	    listItem.setInfo('video', {name})
	    xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	    return


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

def sportsnet():
    addDir('Hockey News', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 21,
           defaultimage)
    addDir('Game Highlights', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 22,
           defaultimage)
    addDir('NHL Top Plays', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 23,
           defaultimage)
    addDir('Hockey Central', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 24,
           defaultimage)

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
                    print 'Video= ' + str(video)
                    li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
                    li.setProperty('fanart_image',  image)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=18)
                    xbmcplugin.setContent(pluginhandle, 'episodes')
                xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")

def csn_cat(url):
        addDir('Bay Area', 'http://www.csnbayarea.com/show/sharks', 96, defaultimage)
        addDir('Chicago', 'http://feed.theplatform.com/f/VHZQDC/7VkEePgNHeD1?form=json', 94, defaultimage)
        #addDir('Chicago', 'http://www.csnchicago.com/video-blackhawks', 97, defaultimage)
        addDir('Philadelphia', 'http://www.csnphilly.com/show/flyers-highlights', 96, defaultimage)

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


def csnchi_smil(name,url):
        html = get_html(url)
	print html
	url = re.compile('http(.+?)m3u8').findall(html)[0]
	print 'SMIL URL= ' + str(url)
	url = 'http' + str(url) + 'm3u8'
	listItem = xbmcgui.ListItem(path=str(url))
	listItem.setInfo('video', {name})
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return

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
        

def csn_chi_old(url):
        html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	spans = soup.find_all('span', {'class' : 'field-content'})
	for span in spans:
            print span
        #for item in spans.find('a'):
	    title = 'item'
	    #link = item.find('a')['href']
	    #title = item.attrs['field-content']
	    #url = item.find('a')['href']
            #html = get_html(url)
        #i = 0
        #while i < 15:
            #try:purl=re.compile('content"><a href="http://www.csnchicago(.+?)">').findall(html)[i]
            #except IndexError:
                #continue
            #title = purl.split('/', -1)[-1].replace('-',' ').title().replace('Nhl','NHL')
            #purl = 'http://www.csnchicago' + str(purl)
            #print 'purl= ' + str(purl)
            #html = get_html(purl)
            #videokey = re.compile('/select/(.+?)\\?').findall(html)[0]    
            #print 'videokey= ' + str(videokey)
	    smil = ''
            #smil = 'http://link.theplatform.com/s/pcPFDC/' + str(videokey)
	    #print 'videolink= ' + str(smil)
            #i = i + 1
	    add_directory3(title,smil,86, defaultfanart ,defaultimage,plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        

def game_recaps(url):

        jgresponse = urllib2.urlopen(url)
        jgdata = json.load(jgresponse)
	ti = (jgdata["totalItems"])
	print 'TotalItems= ' + str(ti)
	i = ti - 1
	while i >= 0:
	    title = (jgdata["dates"][0]["games"][i]["content"]["media"]["epg"][2]["items"][0]["blurb"]).split(': ')[-1]
	    image = (jgdata["dates"][0]["games"][i]["content"]["media"]["epg"][2]["items"][0]["image"]["cuts"]["1136x640"]["src"])
	    url = (jgdata["dates"][0]["games"][i]["content"]["media"]["epg"][2]["items"][0]["playbacks"][2]["url"])
            infoLabels = {'title':title}
            i = i - 1
            li = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)
            li.setInfo( type='Video', infoLabels=infoLabels ) 
            xbmcplugin.addDirectoryItem(addon_handle, url, listitem=li, totalItems=15)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def INDEX(url):

    if "hockeyfights" in url:
            addon_handle = int(sys.argv[1])

            jresponse = urllib2.urlopen('https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCxplsYwPGQVKyiopBAdCMYA&type=video&maxResults=50&key=AIzaSyDuxczhyyvHWfxKuF3ygW9p0GWmKlvWLYc')
            jdata = json.load(jresponse)
            i=0
            while i < 50:
                fightid = (jdata['items'][i]['id']['videoId'])
                title = (jdata['items'][i]['snippet']['title'])
                image = (jdata['items'][i]['snippet']['thumbnails']['high']['url'])
	        url = ('plugin://plugin.video.youtube/?action=play_video&videoid=' + fightid)
                name = title 
                i = i + 1
                li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                li.setProperty('fanart_image', defaultfanart)
                li.setProperty('IsPlayable', 'true')               
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
            xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

        #else:
        #pass


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
elif mode == 51:
    print "Get Fox Sports NHL Videos"
    fox_sports2(url)
elif mode == 52:
    print "Get Hockey Fights"
    hockey_fights(url)
elif mode == 80:
    print "Get MSG Teams"
    msg_cat()
elif mode == 85:
    print "Get MSG Network"
    msg_network(url)
elif mode == 86:
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
    print "Get CSN Chicago Video"
    csn_chi(url)
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


