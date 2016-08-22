#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmc, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, random, calendar, re, xbmcplugin, sys
from BeautifulSoup import BeautifulStoneSoup as Soup
import HTMLParser
#import simplejson as json
import xml.etree.ElementTree as ET


_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.filmrise')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')

defaultimage = 'special://home/addons/plugin.video.filmrise/fanart.jpg'
defaultfanart = 'special://home/addons/plugin.video.filmrise/fanart.jpg'
fanart = 'special://home/addons/plugin.video.filmrise/fanart.jpg'
forensic = 'special://home/addons/plugin.video.filmrise/forensicfiles.jpg'
mugshots = 'special://home/addons/plugin.video.filmrise/mugshots.jpg'
urbanlegends = 'special://home/addons/plugin.video.filmrise/urbanlegends.jpg'
youngdracula = 'special://home/addons/plugin.video.filmrise/youngdracula.jpg'
tnd = 'special://home/addons/plugin.video.filmrise/tnd.jpg'
adcs1 = 'special://home/addons/plugin.video.filmrise/adcs1.jpg'
adcs2 = 'special://home/addons/plugin.video.filmrise/adcs2.jpg'
adcs3 = 'special://home/addons/plugin.video.filmrise/adcs3.jpg'
adcs4 = 'special://home/addons/plugin.video.filmrise/adcs4.jpg'
adc = 'special://home/addons/plugin.video.filmrise/adc.jpg'
fbi = 'special://home/addons/plugin.video.filmrise/fbi.jpg'

confluence_views = [500,501,502,503,504,508]


def CATEGORIES():
    mode = 1

    addDir('Americas Dumbest Criminals', 'http://filmrise.com/category/americas-dumbest-criminals/', 2, adc)
    addDir('The FBI Files', 'http://filmrise.com/the-fbi-files-season-1-ep-1-polly-klaas-kidnapped/', 9, fbi)
    addDir('Forensic Files', 'http://filmrise.com/forensic-files-season-1-episode-1-the-disappearance-of-helle-crafts/', 9, forensic)
    addDir('Mugshots', 'http://filmrise.com/category/mugshots/', mode, mugshots)
    addDir('The New Detectives', 'http://filmrise.com/category/the-new-detectives/', 7, tnd)
    addDir('Urban Legends', 'http://filmrise.com/category/urban-legends/', mode, urbanlegends)
    #addDir('Young Dracula', 'http://feeds.the-antinet.com/movies/youngdracula.xml', mode, youngdracula)
    #addDir('Movies', 'http://http://filmrise.com/category/movies', 20, defaultimage)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def INDEX(url):

    #if "mugshots" in url or "forensic-files" in url or "the-new-detectives" in url or "the-fbi-files" in url or "americas-dumbest-criminals" in url:
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        next=re.compile('numbers" href="(.+?)">Next').findall(html)
        next=str(next)[2:-2]
        print 'Next Page=' + str(next)
        html_parser = HTMLParser.HTMLParser()
        match=re.compile('<a href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(html)
        for pageurl,name,thumbnail in match: 
            #name = html_parser.unescape(name)
            name = str(pageurl)[20:-1]
            name = name.replace('-',' ')
            name = name.title()
            name = name.replace('Mugshots ','')
            name = name.replace('Urban Legends ','')
            name = str(name)
            print 'name=' + name
            #if len(name)>75:
                #continue
            #print 'url=' + str(url)
            page = get_html(pageurl)
            iframe = re.compile('seamless" src=(.+?)" width').findall(page)
            iframe = str(iframe)[2:-2]
            #print 'iframe=' + str(iframe)
            if len(iframe)<5:
                iframe = re.compile('p><iframe src="(.+?)" width').findall(page)
                iframe = str(iframe)[2:-2]
                #print 'iframe=' + str(iframe)
            if 'youtube' in str(iframe) or len(iframe)<2:
                continue
            print 'iframe=' + str(iframe)
            if len(iframe)>5:
                key = iframe.rsplit('?',1)[0]
                key = key.rsplit('-',1)[-1]
                key = key[:8] + '-' + key[8:]
                key = key[:13] + '-' + key[13:]
                key = key[:18] + '-' + key[18:]
                key = key[:23] + '-' + key[23:]
                streamUrl = 'http://api.ovguide.com/v2/streaming/475697de-3ddc-11e4-b764-0019b9eddb47/' + key + '.m3u8'
                #streamUrl = get_html(iframe)
                #streamUrl = re.compile('file:\'(.+?)\'},').findall(streamUrl)
                #streamUrl = str(streamUrl)[2:-2]
                #print url
            li = xbmcgui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setProperty('fanart_image', thumbnail)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=70)
        if len(next)>5:
            url = next
            addDir2('Next Page',url,1,defaultimage, fanart=False, infoLabels=False)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
        #else:
        #pass

def adc_seasons(url):
        addDir('Season 1', 'http://filmrise.com/americas-dumbest-criminals-season-1-ep-1-return-to-cinder/',3,adcs1)
        addDir('Season 2', 'http://filmrise.com/americas-dumbest-criminals-season-2-ep-1-sticking-to-the-job/',3,adcs2)
        addDir('Season 3', 'http://filmrise.com/americas-dumbest-criminals-season-3-ep-1-best-dressed-burglars/',3,adcs3)
        addDir('Season 4', 'http://filmrise.com/americas-dumbest-criminals-season-4-ep-1-blunted-buglary/',3,adcs4)


def fbi_seasons(url):
        addDir('Season 1', 'http://filmrise.com/the-fbi-files-season-1-ep-1-polly-klaas-kidnapped/',6,fbi)
        addDir('Season 2', 'http://filmrise.com/the-fbi-files-season-2-ep-1-a-model-killer/',6,fbi)
        addDir('Season 3', 'http://filmrise.com/the-fbi-files-season-3-ep-1-driven-to-kill/',6,fbi)
        addDir('Season 4', 'http://filmrise.com/the-fbi-files-season-4-ep-1-the-search-for-lisa-rene/',6,fbi)
        addDir('Season 5', 'http://filmrise.com/the-fbi-files-season-5-ep-1-the-price-of-greed/',6,fbi)

def tnd_seasons(url):
        addDir('Season 1', 'http://filmrise.com/the-new-detectives-season-1-ep-1-solider-stories/',8,tnd)
        addDir('Season 2', 'http://filmrise.com/the-new-detectives-season-2-ep-1-mind-hunters/',8,tnd)
        addDir('Season 3', 'http://filmrise.com/the-new-detectives-season-3-ep-1-fatal-compulsion/',8,tnd)
        addDir('Season 4', 'http://filmrise.com/the-new-detectives-season-4-ep-1-lethal-obsession/',8,tnd)
        addDir('Season 5', 'http://filmrise.com/the-new-detectives-season-5-ep-1-remnant-of-blame/',8,tnd)
        addDir('Season 6', 'http://filmrise.com/the-new-detectives-season-6-ep-1-false-witness/',8,tnd)

def movie_genres(url):
        addDir('Cult', 'http://filmrise.com/category/cult', 1, defaultimage)
        addDir('Comedy', 'http://filmrise.com/category/comedy', 1, defaultimage)
        addDir('Horror', 'http://filmrise.com/category/horror', 1, defaultimage)

def ff_seasons(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        seasons = re.compile('a href=(.+?)Episodes').findall(html)
        seasons= str(seasons)
        #print 'seasons=' + str(seasons)
        seasons = seasons.split(',')
        for item in seasons:
            item = str(item)
            #print 'item=' + str(item)
            purl = re.compile('"(.+?)/">').findall(item)
            #print 'purl=' + str(purl)[2:-2]
            purl = str(purl)[2:-2]
            name = re.compile('/">(.+?)\\(').findall(item)
            #name = name.replace('-',' ')
            #name = name.title()
            name = str(name)[2:-2]
            if 'All' in name:
                continue
            #print 'name=' + str(name)
            if 'the-fbi-files' in purl:
                image = fbi
            else:
                image = forensic

            addDir(name, purl,6,image)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def get_adc_seasons(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        episodes = re.compile('Episodes: </strong>(.+?)<br />').findall(html)
        episodes = str(episodes)
        ep = episodes.split(',')
        for item in ep:
            item = str(item)
            #print item
            url = re.compile('<a href="(.+?)"').findall(item)
            name = str(url)[49:-3]
            name = name.replace('-',' ')
            name = name.title()
            name = str(name)
            pageurl = str(url)[2:-2]
            #print 'pageurl=' + str(pageurl)
            page = get_html(pageurl)
            iframe = re.compile('seamless" src=(.+?)" width').findall(page)
            iframe = str(iframe)[2:-2]
            #print 'iframe=' + str(iframe)
            if len(iframe)<5:
                key = iframe.rsplit('?',1)[0]
                key = key.rsplit('-',1)[-1]
                key = key[:8] + '-' + key[8:]
                key = key[:13] + '-' + key[13:]
                key = key[:18] + '-' + key[18:]
                key = key[:23] + '-' + key[23:]
                streamUrl = 'http://api.ovguide.com/v2/streaming/475697de-3ddc-11e4-b764-0019b9eddb47/' + key + '.m3u8'
                #iframe = re.compile('p><iframe src="(.+?)" width').findall(page)
                #iframe = str(iframe)[2:-2]
                #print 'iframe=' + str(iframe)
            if 'youtube' in str(iframe):
                continue
            print 'iframe=' + str(iframe)
            if len(iframe)>5:
                #streamUrl = get_html(iframe)
                #streamUrl = re.compile('file:\'(.+?)\'},').findall(streamUrl)
                #streamUrl = str(streamUrl)[2:-2]
                key = iframe.rsplit('?',1)[0]
                key = key.rsplit('-',1)[-1]
                key = key[:8] + '-' + key[8:]
                key = key[:13] + '-' + key[13:]
                key = key[:18] + '-' + key[18:]
                key = key[:23] + '-' + key[23:]
                streamUrl = 'http://api.ovguide.com/v2/streaming/475697de-3ddc-11e4-b764-0019b9eddb47/' + key + '.m3u8'
            li = xbmcgui.ListItem(name, iconImage=adc, thumbnailImage=adc)
            li.setProperty('fanart_image', adc)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=26)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def get_fbi_seasons(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        episodes = re.compile('Episodes: </strong>(.+?)<br />').findall(html)
        episodes = str(episodes)
        ep = episodes.split(',')
        for item in ep:
            item = str(item)
            if len(item)<5:
                continue
            #print item
            url = re.compile('<a href="(.+?)"').findall(item)
            name = str(url)[36:-3]
            name = name.replace('-',' ')
            name = name.title()
            name = str(name)
            #print 'name=' + str(name)
            pageurl = str(url)[2:-2]
            #print 'pageurl=' + str(pageurl)
            page = get_html(pageurl)
            iframe = re.compile('seamless" src=(.+?)" width').findall(page)
            iframe = str(iframe)[2:-2]
            #print 'iframe=' + str(iframe)
            if len(iframe)<5:
                iframe = re.compile('p><iframe src="(.+?)" width').findall(page)
                iframe = str(iframe)[2:-8]
                #print 'iframe=' + str(iframe)
            if 'youtube' in str(iframe):
                continue
            #print 'iframe=' + str(iframe)
            if len(iframe)>5:
                key = iframe.rsplit('?',1)[0]
                key = key.rsplit('-',1)[-1]
                key = key[:8] + '-' + key[8:]
                key = key[:13] + '-' + key[13:]
                key = key[:18] + '-' + key[18:]
                key = key[:23] + '-' + key[23:]
                streamUrl = 'http://api.ovguide.com/v2/streaming/475697de-3ddc-11e4-b764-0019b9eddb47/' + key + '.m3u8'
                #streamUrl = get_html(iframe)
                #streamUrl = re.compile('file:\'(.+?)\'},').findall(streamUrl)
                #streamUrl = str(streamUrl)[2:-2]
                print 'streamUrl key= ' + str(key)
            if 'the-fbi-files' in pageurl:
                image = fbi
            else:
                image = forensic
                name = name[1:]
            #print 'streamUrl= ' + str(streamUrl)
            li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
            li.setProperty('fanart_image', image)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=18)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def get_tnd_seasons(url):
        addon_handle = int(sys.argv[1])
        html = get_html(url)
        html_parser = HTMLParser.HTMLParser()
        episodes = re.compile('Episodes: </strong>(.+?)<br />').findall(html)
        episodes = str(episodes)
        ep = episodes.split(',')
        for item in ep:
            item = str(item)
            if len(item)<5:
                continue
            #print item
            url = re.compile('<a href="(.+?)"').findall(item)
            name = str(url)[41:-3]
            name = name.replace('-',' ')
            name = name.title()
            name = str(name)
            pageurl = str(url)[2:-2]
            #print 'pageurl=' + str(pageurl)
            page = get_html(pageurl)
            iframe = re.compile('seamless" src=(.+?)" width').findall(page)
            iframe = str(iframe)[2:-2]
            #print 'iframe=' + str(iframe)
            if len(iframe)<5:
                iframe = re.compile('p><iframe src="(.+?)" width').findall(page)
                iframe = str(iframe)[2:-8]
                #print 'iframe=' + str(iframe)
            if 'youtube' in str(iframe):
                continue
            #print 'iframe=' + str(iframe)
            if len(iframe)>5:
                #streamUrl = get_html(iframe)
                #streamUrl = re.compile('file:\'(.+?)\'},').findall(streamUrl)
                #streamUrl = str(streamUrl)[2:-2]
                key = iframe.rsplit('?',1)[0]
                key = key.rsplit('-',1)[-1]
                key = key[:8] + '-' + key[8:]
                key = key[:13] + '-' + key[13:]
                key = key[:18] + '-' + key[18:]
                key = key[:23] + '-' + key[23:]
                streamUrl = 'http://api.ovguide.com/v2/streaming/475697de-3ddc-11e4-b764-0019b9eddb47/' + key + '.m3u8'
            li = xbmcgui.ListItem(name, iconImage=tnd, thumbnailImage=tnd)
            li.setProperty('fanart_image', tnd)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=streamUrl, listitem=li, totalItems=13)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
	print "Indexing by Season"
	adc_seasons(url)
elif mode == 3:
	print "Get Items by Season"
	get_adc_seasons(url)
elif mode == 4:
    print "Play Video"
elif mode == 5:
	print "Indexing by Season"
	fbi_seasons(url)
elif mode == 6:
	print "Get Items by Season"
	get_fbi_seasons(url)
elif mode == 7:
	print "Indexing by Season"
	tnd_seasons(url)
elif mode == 8:
	print "Get Items by Season"
	get_tnd_seasons(url)
elif mode == 9:
	print "Indexing by Season"
	ff_seasons(url)
elif mode == 10:
	print "Get Items by Season"
	get_ff_seasons(url)

elif mode==20:
        print "Genres"
        movie_genres(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
