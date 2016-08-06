#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import requests  
import simplejson as json
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import html5lib
#from html5lib import sanitizer
#from html5lib import treebuilders

h = HTMLParser.HTMLParser()
artbase = 'special://home/addons/plugin.video.discovery-channels/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.discovery-channels')
self = xbmcaddon.Addon(id='plugin.video.discovery-channels')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.discovery-channels")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
#confluence_views = [500,501,502,503,504,508]

plugin = "Discovery Channels"

defaultimage = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaulticon = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaultfanart = 'special://home/addons/plugin.video.discovery-channels/fanart.jpg'

local_string = xbmcaddon.Addon(id='plugin.video.discovery-channels').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
#confluence_views = [50,500,501,502,503,504,508,515]
confluence_views = [500,501,502,503,504,508,515]

def CATEGORIES():
    print platform.system(), platform.release()
    dsc = settings.getSetting(id="dsc")
    if dsc!='false':
        addDir2('Discovery Channel', 'https://www.discoverygo.com/discovery/', 530, artbase + 'discovery.png')
    ap = settings.getSetting(id="ap")
    if ap!='false':
        addDir2('Animal Planet', 'https://www.discoverygo.com/animal-planet/', 530, artbase + 'animalplanet.jpg')
    sci = settings.getSetting(id="sci")
    if sci!='false':
        addDir2('Discovery Science', 'http://www.discoverygo.com/science/', 530, artbase + 'sciencechannel.png')
    idsc = settings.getSetting(id="idsc")
    if idsc!='false':
        addDir2('Investigation Discovery', 'http://www.discoverygo.com/investigation-discovery/', 530, artbase + 'investigationdiscovery.jpg')
    dahn = settings.getSetting(id="dahn")
    if dahn!='false':
        addDir2('American Heroes', 'https://www.discoverygo.com/ahc/', 530, artbase + 'ahctv.jpg')
    vel = settings.getSetting(id="vel")
    if vel!='false':
        addDir2('Velocity', 'https://www.discoverygo.com/velocity/', 530, artbase + 'velocity.png')
    dest = settings.getSetting(id="dest")
    if dest!='false':
        addDir2('Destination America', 'https://www.discoverygo.com/destination-america/', 530, artbase + 'destinationamerica.jpg')
    tlc = settings.getSetting(id="tlc")
    if tlc!='false':
        addDir2('TLC', 'https://www.discoverygo.com/tlc/', 530, artbase + 'tlc.jpg')
    dscl = settings.getSetting(id="dscl")
    if dscl!='false':
        addDir2('Discovery Life', 'https://www.discoverygo.com/discovery-life/', 530, artbase + 'discoverylife.jpg')
    dsck = settings.getSetting(id="dsck")
    if dsck!='false':
        addDir2('Discovery Kids', 'http://discoverykids.com/videos/', 535, artbase + 'discoverykids.jpg')
    views = settings.getSetting(id="views")
    if views != 'false':
        xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#530
def discovery_menu(url):
	site = 'http://www.' + (iconimage.rsplit('/', 1)[-1]).split('.')[0] + '.com/videos/'
	r = requests.get(url)
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', r.cookies))
	f = opener.open(url)
        page = f.read()
	auth = re.compile(r'<div class="content-overlay">(.+?)\s/', re.DOTALL).findall(str(page))
	plot = re.compile('data-description="(.+?)"').findall(str(page)); i = 0
	shows = re.compile('data-show-title="(.+?)"').findall(str(page))
	titles = re.compile('data-episode-title="(.+?)"').findall(str(page))
	images = re.compile('img src="(.+?)"').findall(str(page))
	duration = re.compile('data-duration="(.+?)"').findall(str(page))
	dataslug = re.compile('data-slug="(.+?)"').findall(str(page))
	datashowslug = re.compile('data-show-slug="(.+?)"').findall(str(page))
	collection = re.compile('collection-type"(.+?)",').findall(str(page))
	expires = re.compile('data-expiration="(.+?)"').findall(str(page))
	diff = len(shows) - len(expires)
	for authkey in auth:
	    if not 'icon-preview-with-circle' in authkey:
		i = i + 1
		continue
	    if not 'recommended' in collection[i]:
	       i = i + 1
	       continue
	    title = (shows[i] + ' - ' + titles[i]).replace('&amp;', '&').replace('&#x27;','\'').replace('&quot;','\'').replace('&rsquo;','\'')
	    expire = (expires[i].split('T')[0]).split('-')
	    year = expire[0]; month = expire[1]; day = (int(expire[2]) - 1)
	    month = month.lstrip('0')
	    expiry = str(month) + '/' + str(day) + '/' + str(year)
	    key = datashowslug[i] + '/' + dataslug[i]
	    url = 'http://www.discoverygo.com/' + str(key)
	    try: description = plot[i]
	    except IndexError:
	        description = 'No Description Available' #plot[-1]
	    description = description.replace('&amp;', '&').replace('&#x27;','\'').replace('&quot;','\'').replace('&rsquo;','\'')
	    try: icon = images[i]
	    except IndexError:
		icon = images[-1]
	    icon = icon.replace('&amp;', '&')
	    try: runtime = GetInHMS(int(duration[i]))
	    except IndexError:
		runtime = GetInHMS(int(duration[-1]))
	    add_directory3(title, url, 531, artbase + 'fanart2.jpg', icon, plot=description + ' (' + runtime.replace('00:','') + ') ' + expiry)  
	    i = i + 1
	if not 'tlc.com' in site:
            addDir(name +' Video Clips Sorted by Show', site, 533, iconimage, artbase + 'fanart2.jpg')
	else:
            addDir(name +' Video Clips Sorted by Show', site, 533, iconimage, artbase + 'fanart2.jpg')
        xbmcplugin.setContent(pluginhandle, 'episodes')
        views = settings.getSetting(id="views")
	if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#531
def discovery_shows(name,url):
	    r = requests.get(url)
	    opener = urllib2.build_opener()
	    opener.addheaders.append(('Cookie', r.cookies))
	    f = opener.open(url)
            page = f.read()
	    try: m3u8 = re.compile('streamUrl(.+?)hdsStreamUrl').findall(page)[0]
	    except IndexError:                
	        xbmcgui.Dialog().notification(name, ' Episode Not Available', iconimage, 5000, False)
	        return
	    if QUALITY =='2':
	        url = (str(m3u8.replace('\/','/'))[13:-13])
	    elif QUALITY =='1':
	        url = (str(m3u8.replace('\/','/'))[13:-13]).replace('4500k,', '')
	    elif QUALITY =='0':
	        url = (str(m3u8.replace('\/','/'))[13:-13]).replace('2200k,3000k,4500k,', '')
	    description = (re.compile('detailed(.+?)}').findall(page)[0]).replace('&quot;','').replace(':','')
	    play(url)
            xbmcplugin.endOfDirectory(addon_handle)


#532
def discovery_clips(url, iconimage):
        try: response = urllib2.urlopen(url)
	except urllib2.HTTPError:                
	    xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
	    return
        try: dscdata = json.load(response)
	except ValueError:                
	    xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
	    return
        i=0
	if not 'nextVideosList' in dscdata:            
	    xbmcgui.Dialog().notification(name, ' No Streams Found - Try the Search Function', iconimage, 5000, False)
	    return
        for title in dscdata["nextVideosList"]:
	    title = (dscdata["nextVideosList"][i]["post_title"])
	    description = (dscdata["nextVideosList"][i]["video"]["description"])
	    iconimage = (dscdata["nextVideosList"][i]["video"]["thumbnailUrl"])
	    duration = (dscdata["nextVideosList"][i]["video"]["duration"])
	    url = (dscdata["nextVideosList"][i]["video"]["src"])
	    if QUALITY =='1':
	        url = url.replace('4500k,', '')
	    elif QUALITY =='0':
	        url = url.replace('2200k,3000k,4500k,', '')
	    i = i + 1
            infoLabels = {'title':title,
                          'tvshowtitle':title,
                          'plot':description}
            li = xbmcgui.ListItem(title, iconImage= iconimage, thumbnailImage= iconimage)
            li.setProperty('fanart_image', artbase + 'fanart2.jpg')
            li.setInfo(type="Video", infoLabels=infoLabels)
	    li.addStreamInfo('video', { 'duration': duration })
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=15)
            xbmcplugin.setContent(pluginhandle, 'episodes')
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)
	    

#533
def other_shows(url, iconimage):
	print url, iconimage
	add_directory2('Search', url, 538, artbase + 'fanart2.jpg', iconimage,plot='')
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("ul",{"class":"show-list"})[0]
	for show in soup.find_all("h6"):
	    tvshow = show.get('data-value-display').encode('utf-8').replace("\\'","'")
	    if not 'tlc.com' in url:
	        link = url.replace('videos', 'tv-shows') + show.get('data-ssid').split('/')[-1] + '?flat=1'
		mode = 532
	    else:
	        link = url.replace('videos', 'tv-shows') + show.get('data-ssid').split('/')[-1] + '?flat=2'		
		mode = 534
	    add_directory2(tvshow, link, mode, artbase + 'fanart2.jpg', iconimage,plot='')
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#534
def tlc_clips(url, iconimage):
	html = get_html(url)
	try: soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"grid-wrapper"})[0]
	except TypeError:                
	    xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
	    return
	for show in soup.find_all("div",{"class":"caption table-cell"}):
	    paragraph = str(show.find('p',{'class': 'extra video'}))
	    if paragraph == 'None':
		continue
	    tvshow = str(show.find('a'))
	    tvshow =  re.compile('">(.+?)</a>').findall(tvshow)[0]
	    link = show.find('a')['href']
	    link = link + '?flat=1'
	    add_directory2(tvshow, link, 532, artbase + 'fanart2.jpg', iconimage,plot='')
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#535
def dsc_kids(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("ul",{"class":"dropdown-menu"})
	soup = str(soup).split('</a>'); i = 0
	while i < 9:
	    cat = re.compile('data-category="(.+?)"').findall(str(soup))[i]
	    if i == 0:
		cat = 'all'
	        link = 'http://discoverykids.com/app/themes/discoverykids/ajax-load-more/ajax-load-more.php?postType=video&taxonomyName=category&taxonomyTerm=&orderBy=post_date&order=DESC&device=computer&numPosts=24&onScroll=false&pageNumber=1'
	    else:
	        link = 'http://discoverykids.com/app/themes/discoverykids/ajax-load-more/ajax-load-more.php?postType=video&taxonomyName=category&taxonomyTerm=' + cat + '&orderBy=post_date&order=DESC&device=computer&numPosts=24&onScroll=false&pageNumber=1'
	    title = cat.title()
	    i = i + 1
	    add_directory2(title, link, 536, artbase + 'fanart2.jpg', iconimage,plot='')
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#536
def kids_clips(url,iconimage):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"thumbnail super-item"})
	for item in soup:
	    title = item.find('div',{'class':'caption'})
	    plot = (striphtml(str(title)).strip()).splitlines()[-1]
	    title = (striphtml(str(title)).strip()).splitlines()[0]
	    title = sanitize(title)
	    image = item.find('img')['src']
	    link = item.find('a')['href']
	    add_directory3(title, link, 537, artbase + 'fanart2.jpg', image,plot)
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#537
def kids_stream(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib')
	try: url = soup.find('source')['src']
	except TypeError:                
	    xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
	    return
	play(url)
        xbmcplugin.endOfDirectory(addon_handle)


#538
def search(url):
	print iconimage
	url = url.replace('videos/', 'search/?q=')
	print url
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            print 'search= ' + search
            url = url + search.replace(' ','+')
	    print url
	    get_search(url)


#539
def get_search(url):
	site = re.compile('www.(.+?).com').findall(url)
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"item"})
	try :next = 'http://www.' + site[0] + '.com' + re.compile('href="(.+?)"><div class="next').findall(str(html))[-1]
	except IndexError:
	    return
	for item in soup:
	    title = striphtml(str(item.find('h4'))).split(' | ')[0]
	    print title
	    try: icon = item.find('img')['src']
	    except TypeError:
		icon = defaulticon
	    url = item.find('a')['href']
	    if not 'videos' in url:
		continue
	    post_url = url.split('videos')[-1]
	    if len(post_url) < 2:
		continue
	    print url
	    description = striphtml(str(item.find('div',{'class':'item-detail'}))).replace('\n','').strip().split('http')[0]
	    add_directory3(title, url, 540, artbase + 'fanart2.jpg', icon, plot=description)# + ' (' + runtime.replace('00:','') + ')')
	add_directory2('Next Page', next, 539, artbase + 'fanart2.jpg', iconimage, plot='')
        views = settings.getSetting(id="views")
        if views != 'false':
            xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
        xbmcplugin.endOfDirectory(addon_handle)


#540
def search_streams(url):
	html = get_html(url)
	try: m3u8 = ((re.compile('referenceId":"(.+?)m3u8"').findall(str(html))[0]).replace('\\', '') + 'm3u8').split('"src":"')[-1]
	except IndexError:                
	    xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
	    return
	print m3u8
	play(m3u8)
		

def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    ti = "%02d:%02d:%02d" % (hours, minutes, seconds)
    ti = str(ti)
    return ti


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


#999
def play(url):
    print url
    item = xbmcgui.ListItem(path=url)
    item.setProperty('IsPlayable', 'true')
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
        return ok


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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, totalItems=40)
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
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = isFolder)
	return ok

def addLink(name, url, mode, iconimage, fanart=False, infoLabels=True):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration })
    liz.setProperty('IsPlayable', 'true')
    if not fanart:
        fanart=defaultfanart
    liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=False)
    return ok

def add_item( action="" , title="" , plot="" , url="" ,thumbnail="" , folder=True ):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] folder=["+str(folder)+"]")

    listitem = xbmcgui.ListItem( title, iconImage=iconimage, thumbnailImage=iconimage )
    listitem.setInfo( "video", { "Title": name, "Plot": description, "Duration": duration } )
    
    if url.startswith("plugin://"):
        itemurl = url
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem)
    else:
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
        return ok

def addDir(name, url, mode, iconimage, fanart=True, infoLabels=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty('IsPlayable', 'true')
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image', artbase + 'fanart2.jpg')
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok


def addDir2(name,url,mode,iconimage, fanart=False, infoLabels=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if not fanart:
            fanart=defaultfanart
        liz.setProperty('fanart_image', artbase + 'fanart5.jpg')
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
    CATEGORIES()
elif mode == 1:
    print "Indexing Videos"
    INDEX(url)
elif mode == 4:
    print "Play Video"
elif mode == 6:
    print "Get Episodes"
    get_episodes(url)
elif mode==530:
        print "Discovery Menu"
	discovery_menu(url)
elif mode==531:
        print "Discovery Shows"
	discovery_shows(name,url)
elif mode==532:
        print "Discovery Clips"
	discovery_clips(url, iconimage)
elif mode==533:
        print "Other Clips"
	other_shows(url, iconimage)
elif mode==534:
        print "Get TLC Clips"
	tlc_clips(url, iconimage)
elif mode==535:
        print "Get DSC Kids"
	dsc_kids(url)
elif mode==536:
        print "Get Kids Clips"
	kids_clips(url, iconimage)
elif mode==537:
        print "Get Kids Stream"
	kids_stream(name,url)
elif mode==538:
        print "Search"
	search(url)
elif mode==539:
        print "Get Search"
	get_search(url)
elif mode==540:
        print "Search Streams"
	search_streams(url)
elif mode==330:
        print "Discovery Science Menu"
	discovery_sci_menu(url)
elif mode==331:
        print "Discovery Science Shows"
	discovery_sci_clips(url)
elif mode==430:
        print "Animal Planet Menu"
	animal_planet_menu(url)
elif mode==431:
        print "Animal Planet Shows"
	animal_planet_clips(url)
elif mode==999:
        print "Animal Planet Shows"
	play(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
