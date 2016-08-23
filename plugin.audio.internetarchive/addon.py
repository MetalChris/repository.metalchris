#!/usr/bin/python
#
#
# Constructed by MetalChris
# Released under GPL(v2)

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, string, htmllib, os, platform, re, xbmcplugin, sys
import HTMLParser
from bs4 import BeautifulSoup
from urllib import urlopen
#import lxml.html
#import socket

settings = xbmcaddon.Addon(id="plugin.video.internetarchive")
artbase = 'special://home/addons/plugin.audio.internetarchive/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.audio.internetarchive')
translation = selfAddon.getLocalizedString
local_string = xbmcaddon.Addon(id='plugin.video.internetarchive').getLocalizedString
dsort = settings.getSetting(id="dsort")
ssort = settings.getSetting(id="ssort")
download = settings.getSetting(id="download")
sort = settings.getSetting(id="sort")
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.audio.internetarchive")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
baseurl = 'https://archive.org/'

plugin = "Internet Archive [Audio]"

defaultimage = 'special://home/addons/plugin.audio.internetarchive/icon.png'
defaultfanart = 'special://home/addons/plugin.audio.internetarchive/fanart.jpg'
defaulticon = 'special://home/addons/plugin.audio.internetarchive/icon.png'

local_string = xbmcaddon.Addon(id='plugin.audio.internetarchive').getLocalizedString
addon_handle = int(sys.argv[1])
pluginhandle = int(sys.argv[1])
#confluence_views = [500,501,502,503,504,508,515]
#xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


def ia_categories():
        data = urllib2.urlopen(baseurl).read() 
        add_directory2('Search', baseurl, 65, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
        soup = BeautifulSoup(data,'html.parser')
        for item in soup.find_all(attrs={'class': 'row toprow fivecolumns audio'}):
            for link in item.find_all('a'):
                l = link.get('href')
                title = link.get('title')
                if title == 'TV NSA Clip Library':
                    mode = 64
                    url = l + '&page=1'
                else:
                    url = l
                if len(url) <5:
                    continue
                if str(url)[0] == '/':
                    url = 'https://archive.org' + url
                if title not in link:
                    link = str(link)
                    title = re.compile('>(.+?)</a>').findall(link)[0]
                    if 'img' in title:
                        continue
                    if '</span> ' in title:
                        title = re.compile('</span> (.+?)</').findall(link)[0]
                    if title == 'All Audio':
                        mode = 61
                    else:
                        mode = 62
                url = url + '?&sort=-date&page=1'
                print 'IA URL= ' + str(url)
                add_directory2(title,url, mode,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
        xbmcplugin.setContent(pluginhandle, 'episodes')


def ia_sub_cat(url):
        url = url.replace('?&sort=-date&page=1','')
        print 'IA Audio Sub_Cat URL= ' + str(url)
        data = urllib2.urlopen(url).read() 
        soup = BeautifulSoup(data,'html.parser')
        for item in soup.find_all(attrs={'class': 'collection-title'}):
            for link in item.find_all('a'):
                l = link.get('href')
                url = 'https://archive.org' + l + '?&sort=-date&page=1'
                if len(url) <25:
                    continue
                link = str(link)
                title = re.sub('\s+',' ',link)
                title = re.compile('<div>(.+)</div>').findall(title)[0]
                title = title.replace('&amp;','&')
                if title == 'Television Archive':
                    mode = 61
                else:
                    mode = 62
                add_directory2(title,url, mode, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
        xbmcplugin.setContent(pluginhandle, 'episodes')


def ia_sub2_audio(url):
        page = (url)[-1]
        print 'page= ' + str(page)
        thisurl = url[:-7]
        print 'thisurl= ' + str(thisurl)
        req = urllib2.Request(url)
        try: data = urllib2.urlopen(req, timeout = 5) 
        except urllib2.HTTPError , e:
            print 'Error Type= ' + str(type(e))    #not catch
            print 'Error Args= ' + str(e.args)
            line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
            dialog = xbmcgui.Dialog()
            xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again') 
            return 
        except urllib2.URLError , e:
            print 'Error Type= ' + str(type(e))
            print 'Error Args= ' + str(e.args)
            line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
            dialog = xbmcgui.Dialog()
            xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
            return 
        #except socket.timeout , e:
            #print 'Error Type= ' + str(type(e))
            #print 'Error Args= ' + str(e.args)
            #line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
            #dialog = xbmcgui.Dialog()
            #xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
            #return 
        #except ssl.SSLError , e:
            #print 'Error Type= ' + str(type(e))    #not catch
            #print 'Error Args= ' + str(e.args)
            #line1 = str(e.args).partition("'")[-1].rpartition("'")[0]
            #dialog = xbmcgui.Dialog()
            #xbmcgui.Dialog().ok(addonname, line1, 'Please Try Again')
            #return 
        soup = BeautifulSoup(data,'html.parser')
        for item in soup.find_all(attrs={'class': 'item-ttl C C2'}):
            for link in item.find_all('a'):
                l = link.get('href')
                purl = 'https://archive.org' + l
                title = link.get('title').encode('utf8')
                html = get_html(purl)
                lineage = str(re.compile('Lineage</span> <span class="value">(.+?)</span>').findall(html))
                lineage = lineage.replace('&gt;','>').replace('&amp;','&')
                if lineage == '[]':
                    title = title
                else:
                    title = title + ' - ' + 'Lineage: ' + lineage[2:-2]
                url = purl
                add_directory2(title,url, 63, artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
            xbmcplugin.setContent(pluginhandle, 'episodes')
        page = str(int(page) + 1)
        thisurl = thisurl.replace('?&sort=-date','')
        url = thisurl + '?&sort=-date&page=' + page
        print 'IA Next Page URL= ' + str(url)
        add_directory2('Next Page', url, 62,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)

def ia_audio_files(url):
            html = get_html(url)
            tracks = re.compile('"title":"(.+?)",').findall(html)
            songs = re.compile('title(.+?)}]').findall(html)
            #c = len(tracks)
            i = 0
            for track in tracks:
                title = str(track.split('.')[-1])
                #if i < c:
                try:song = re.compile('"file":"(.+?)mp3').findall(html)[i]
                except IndexError:
                    pass
                duration = re.compile('duration(.+?)sources').findall(html)[i]
                duration = duration[2:-2]
                i = i + 1
                tracknumber = int(i)
                url = 'https://archive.org' + str(song) + 'mp3'
                print 'URL= ' + str(url)
                infoLabels = {'title':title, 'duration':duration, 'tracknumber':tracknumber}
                li = xbmcgui.ListItem(title, iconImage=artbase + 'ia.png', thumbnailImage=artbase + 'ia.png')
                li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
                #li.setProperty(Playcount)
                li.setInfo(type = 'music', infoLabels = infoLabels)
                commands = []
                commands.append
                    #li.addContextMenuItems([('Download File', 'XBMC.RunScript(special://home/addons/plugin.video.internetarchive/downloader.py)',)])
                li.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url))])
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
                xbmcplugin.setContent(addon_handle, 'episodes')
            xbmcplugin.endOfDirectory(addon_handle)


def ia_nsa(url):            
        data = get_html(url)
        page = (url)[-1]
        match = re.compile('<video src="(.+?)"').findall(data)
        for link in match:
            url = 'https://archive.org' + link
            title = url

            li = xbmcgui.ListItem(title, iconImage=artbase + 'ia.png', thumbnailImage=artbase + 'ia.png')
            li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
        page = str(int(page) + 1)
        url = 'https://archive.org/details/nsa?page=' + page
        print 'IA NSA Next Page URL= ' + str(url)
        add_directory2('Next Page', url, 64,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
        xbmcplugin.endOfDirectory(addon_handle)


def ia_search():
        if sort == '0':
            sval = '-publicdate'
            sname = 'Date'
        elif sort == '1':
            sval = 'titleSorter'
            sname = 'Title'
        elif sort == '2':
            sval = '-downloads'
            sname = 'Views'
        else:
            sval = 'creatorSorter'
            sname = 'Creator'
            print 'sval= ' + str(sval)
        keyb = xbmc.Keyboard('', 'Search and Sort By ' + sname)
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            print 'search= ' + search

            url = 'https://archive.org/search.php?query=' + search + '&and[]=mediatype%3A%22audio%22&sort=' + sval + '&page=1'
            #url = 'https://archive.org/search.php?query=' + search + '&and[]=mediatype%3A%22audio%22&page=1'
            ia_sub2_audio(url)
        else:
            ia_categories()


def ia_search_audio(url):
        page = (url)[-1]
        print 'page= ' + str(page)
        thisurl = url[:-7]
        print 'thisurl= ' + str(thisurl)
        data = urllib2.urlopen(url).read() 
        soup = BeautifulSoup(data,'html.parser')
        for item in soup.find_all(attrs={'class': 'item-ttl C C2'}):
            for link in item.find_all('a'):
                l = link.get('href')
                purl = 'https://archive.org' + l
                title = link.get('title')
                html = get_html(purl)
                match=re.compile('<meta property="og:video" content="(.+?)"/>').findall(html)
                clipstream = re.compile('TV.clipstream_clips  = (.+?);').findall(html)
                if str(clipstream) == '[]':
                    url = str(match)[2:-2]
                    if len(url) <25:
                        continue
                    li = xbmcgui.ListItem(title, iconImage= artbase + 'ia.png', thumbnailImage= artbase + 'ia.png')
                    li.setProperty('fanart_image',  artbase + 'internetarchive.jpg')
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=70)
                else:
                    url = str(clipstream)[3:-3]
                    url = url.replace('"','')
                    try: add_directory2(title,url,63,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')
                    except KeyError:
                        continue
        page = str(int(page) + 1)
        thisurl = thisurl.replace('?&sort=-date','')
        url = thisurl + '&page=' + page
        print 'IA Next Page URL= ' + str(url)
        add_directory2('Next Page', url, 66,  artbase + 'internetarchive.jpg', artbase + 'ia.png',plot='')

        xbmcplugin.endOfDirectory(addon_handle)


#80
def downloader(url):    
        path = addon.getSetting('download')
        if path == "":
            xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
                    %(translation(30000), translation(30010), defaulticon))
            addon.openSettings()
            path = addon.getSetting('download')
        if path == "":
            return
        file_name = url.split('/')[-1]
        dlsn = settings.getSetting(id="status")
        bsize = settings.getSetting(id="bsize")
        print 'Buffer Size= ' + str(bsize)
        ret = xbmcgui.Dialog().yesno("Internet Archive [Video]", 'Download Selected File?', str(file_name))
        if ret == False:
            return ia_sub2_video
        else:
            xbmcgui.Dialog().notification('IA [Video]', 'Download Started.', xbmcgui.NOTIFICATION_INFO, 5000)
        print 'URL= ' + str(url)
        print 'Filename= ' + str(file_name)
        print 'Download Location= ' + str(download)
	u = urllib2.urlopen(url)
	f = open(download+file_name, 'wb')
	meta = u.info()
	file_size = float(meta.getheaders("Content-Length")[0])
        file_sizeMB = float(file_size/(1024*1024))
	print "Downloading: %s %s MB" % (file_name, "%.2f" % file_sizeMB)
	file_size_dl = 0
	block_sz = int(bsize)
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	    file_size_dl += float(len(buffer))
            file_size_dlMB = float(file_size_dl/(1024*1024)) 
	    f.write(buffer)
	    status = "%.2f  [%3.2f%%]" % (file_size_dlMB, file_size_dl * 100. / file_size)
 	    status = status + chr(8)*(len(status)+1)
            if dlsn!='false':
                xbmcgui.Dialog().notification('IA [Video] Download in Progress', str(status) + ' of ' + ("%.2f" % float(file_sizeMB)) + ' MB', xbmcgui.NOTIFICATION_INFO, 2500)
            else:
                pass
	f.close()
        xbmcgui.Dialog().notification('IA [Video]', 'Download Completed.', xbmcgui.NOTIFICATION_INFO, 5000)
        print 'Download Completed'


def add_directory2(name,url,mode,fanart,thumbnail,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="music", infoLabels={ "Title": name,
                                                } )
        if not fanart:
            fanart=''
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=70)
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

def addListItem(label, image, url, isFolder, infoLabels = True, fanart = False, duration = False):
	listitem = xbmcgui.ListItem(label = label, iconImage = image, thumbnailImage = image)
	if not isFolder:
		if settings.getSetting('download') == '' or settings.getSetting('download') == 'false':
			listitem.setProperty('IsPlayable', 'true')
	if fanart:
		listitem.setProperty('fanart_image', fanart)
	if infoLabels:
                listitem.setInfo( type="music", infoLabels={ "Title": name,
                                                } )
		if duration:
			if hasattr(listitem, 'addStreamInfo'):
				listitem.addStreamInfo('video', { 'duration': int(duration) })
			else:
				listitem.setInfo(type = 'music', infoLabels = { 'duration': str(datetime.timedelta(milliseconds=int(duration)*1000)) } )
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = isFolder)
	return ok

def addLink(name, url, mode, iconimage, fanart=False, infoLabels=True):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "Title": name,
                                                } )
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
    liz.setInfo( type="music", infoLabels={ "Title": name,
                                                } )
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
        liz.setInfo( type="music", infoLabels={ "Title": name,
                                                } )
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
    ia_categories()
elif mode == 1:
    print "Indexing Audio"
    index(url)
elif mode == 4:
    print "Play Audio"
elif mode == 6:
    print "Get Episodes"
    get_episodes(url)
elif mode == 60:
    print "Get IA Audio Categories"
    ia_video(url)
elif mode == 61:
    print "Get IA Audio Sub Categories"
    ia_sub_cat(url)
elif mode == 62:
    print "Get IA Audio Sub2 Categories"
    ia_sub2_audio(url)
elif mode == 63:
    print "Get Audio Files"
    ia_audio_files(url)
elif mode == 64:
    print "Get IA NSA"
    ia_nsa(url)
elif mode == 65:
    print "IA Search"
    ia_search()
elif mode == 66:
    print "IA Search Audio"
    ia_search_audio(url)
elif mode == 80:
   print "IA Download File"
   downloader(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
