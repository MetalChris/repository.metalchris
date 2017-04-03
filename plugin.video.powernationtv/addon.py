#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

import xbmcaddon, urllib, xbmcgui, xbmcplugin, urllib2, re, sys
from bs4 import BeautifulSoup
import html5lib

selfAddon = xbmcaddon.Addon(id='plugin.video.powernationtv')
translation = selfAddon.getLocalizedString

API_KEY = '8d2b83696759583b589b42e70006a2a423626ac7'

defaultimage = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaultfanart = 'special://home/addons/plugin.video.powernationtv/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaulticon = 'special://home/addons/plugin.video.powernationtv/icon.png'
baseurl = 'http://www.powerblocknetwork.com/'

pluginhandle = int(sys.argv[1])
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]
plugin = 'PowerNation TV'


def CATEGORIES():
    html = get_html(baseurl)
    soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'col-md-3 col-sm-3 col-xs-6 bottom_spacing'})
    for show in soup:
        url = show.find('a')['href']
        if not 'http:' in url:
            url = 'http:' + show.find('a')['href']
        title = str((re.compile('title="(.+?)"')).findall(str(show)))[2:-2]
        if ' - ' in title:
            title = title.split(' - ')[0]
        if len(str(title)) > 30:
            continue
        if len(str(title)) == 0:
            title = 'Xtreme Off-Road'
        if '/' in title:
            mode = 30
        if '2' in title:
            mode = 60
        else:
            mode = 10
        image = baseurl + show.find('img')['src']
        addDir(title, url, mode, image)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#10
def INDEX(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode-info'})
    #titles = BeautifulSoup(html,'html5lib').find_all('p',{'class':'lighttype faux-h2'});e=0
    #if len(titles) != len(soup):
        #titles = BeautifulSoup(html,'html5lib').find_all('p',{'class':'lighttype'});e=0
    for episode in soup:
        #If it's a "coming soon" show, skip it
        if episode.find(class_="coming_soon"):
            continue
        title = episode.find('a').text.encode('ascii',errors='ignore').strip()
        url = episode.find('a')['href']
        if not 'http:' in url:
            url = 'http:' + episode.find('a')['href']
        image = defaultimage#episode.find('img')['src']
        #If it has metadata, add it to the episode info
        if episode.find('meta'):
            plot = episode.find(itemprop="description")['content'].encode('utf-8').strip()
            episodeNumber = episode.find(itemprop="episodeNumber")['content'].encode('utf-8').strip()
            season = episodeNumber[2:6]
            episodeNum = episodeNumber[-2:]
            aired = episode.find(itemprop="datePublished")['content'].encode('utf-8').strip()
            addDir(title, url, 20, image, image, {'plot': plot, 'season': season, 'episode': episodeNum, 'aired': aired});e=e+1
        else:
            addDir(title, url, 20, image, image)#;e=e+1
    xbmcplugin.setContent(pluginhandle, 'episodes')
    #Fix the sort to be proper episode number order
    #xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_EPISODE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#20
def IFRAME(name,url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('script')
    xbmc.log('SOUP: ' + str(len(soup)))
    iframe = re.compile('script src="(.+?)"').findall(str(soup))
    for item in iframe:
        if 'jwplatform' in item:
            xbmc.log('MATCH')
            xbmc.log('ITEM: ' + str(item))
            iframe = 'http:' + item
            data = get_html(iframe)
            try: stream = re.compile('"file": "(.+?)"').findall(str(data))[0]
            except IndexError:
                xbmcgui.Dialog().notification(name, translation(30000), defaultimage, 5000, False)
                sys.exit()
            listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
            xbmc.log('STREAM: ' + str(stream))
            xbmc.Player().play( "http:" + stream, listitem )
            sys.exit()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#30
def YMM(name,url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('a',{'class':'lighttype'})
    xbmc.log(str(len(soup)))
    for makes in soup:
        title = makes.get('title')
        url = makes.get('href')
        if not 'http:' in url:
            url = 'http:' + url
        addDir(title, url, 40, defaultimage)
    xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#40
def MODELS(name,url):
    html = get_html(url)
    group = BeautifulSoup(html,'html5lib').find_all('div',{'class':'tab-pane fade in active topspacing'})
    soup = BeautifulSoup(str(group),'html5lib').find_all('div',{'class':'pndaily_thumbnail col-xs-12'})
    xbmc.log(str(len(soup)))
    for models in soup:
        title = models.find('a')['title']
        url = models.find('a')['href']
        if not 'http:' in url:
            url = 'http:' + models.find('a')['href']
        image = models.find('img')['src']
        addDir(title, url, 50, image)
    xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#50
def YMM_VIDEOS(name,url):
    html = get_html(url)
    iframes = re.compile('script src="(.+?)"').findall(html)
    for iframe in iframes:
        while 'jwplatform' in iframe:
            iframe = 'http:' + iframe
            data = get_html(iframe)
            try: stream = re.compile('origin_url": "(.+?)"').findall(str(data))[-1]
            except IndexError:
                xbmcgui.Dialog().notification(name, translation(30000), defaultimage, 5000, False)
                sys.exit()
            listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
            xbmc.Player().play( stream, listitem )
            sys.exit()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#60
def TECH(name,url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'epi_tile'})
    xbmc.log(str(len(soup)))
    for makes in soup:
        title = makes.find('p').text
        url = makes.find('a')['href']
        if not 'http:' in url:
            url = 'http:' + url
        addDir(title, url, 20, defaultimage)
    xbmcplugin.setContent(pluginhandle, 'episodes')
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
    #req.add_header('X-API-KEY:','8d2b83696759583b589b42e70006a2a423626ac7')

    try:
        response = urllib2.urlopen(req)
        response.getcode()
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
    if type(infoLabels) is not bool:
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": infoLabels['plot'], "episode": infoLabels['episode'], "season": infoLabels['season'], "aired": infoLabels['aired']})
    else:
        liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    if not fanart:
        fanart=defaultfanart
    liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image',defaultfanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


def addDir3(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
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
    xbmc.log("PowerNation TV Menu")
    CATEGORIES()
elif mode == 10:
    xbmc.log("PowerNation TV Videos")
    INDEX(url)
elif mode == 20:
    xbmc.log("PowerNation TV Play Video")
    IFRAME(name,url)
elif mode == 30:
    xbmc.log("PowerNation TV YMM Makes")
    YMM(name,url)
elif mode == 40:
    xbmc.log("PowerNation TV YMM Models")
    MODELS(name,url)
elif mode == 50:
    xbmc.log("PowerNation TV YMM Videos")
    YMM_VIDEOS(name,url)
elif mode == 60:
    xbmc.log("PowerNation TV 2 Minute Tech Videos")
    TECH(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

