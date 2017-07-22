#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import urlparse
import httplib


artbase = 'special://home/addons/plugin.video.bnwmovies/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.bnwmovies')
self = xbmcaddon.Addon(id='plugin.video.bnwmovies')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.bnwmovies")
download = settings.getSetting(id="download")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Black and White Movies"

defaultimage = 'special://home/addons/plugin.video.bnwmovies/icon.png'
defaultfanart = 'special://home/addons/plugin.video.bnwmovies/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.bnwmovies/icon.png'


local_string = xbmcaddon.Addon(id='plugin.video.bnwmovies').getLocalizedString
addon_handle = int(sys.argv[1])
QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508,515]
airdate = ''


#633
def shows():
	response = get_html('http://www.bnwmovies.com/')
	soup = BeautifulSoup(response,'html.parser').find_all('li',{'class':'menu-item'})
	for genre in soup[2:]:
		title = striphtml(str(genre.find('a')))
		url = 'http://www.bnwmovies.com' + genre.find('a')['href']#genre.get('href')
		thumbnail = defaultimage
		add_directory2(title, url, 636, defaultfanart, thumbnail, plot='')
	xbmc.log('GENRE: ' + str(genre))
	xbmcplugin.endOfDirectory(addon_handle)


#636
def videos(url):
	response = get_html(url)
	if response == False:
		xbmcgui.Dialog().notification(name, 'No Episodes Available', defaultimage, 5000, False)
		sys.exit()
		xbmc.log('PAGE NOT FOUND')
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class': 'cattombstone'})
	xbmc.log('SOUP: ' + str(len(soup)))
	nxt = BeautifulSoup(response,'html.parser').find_all('a',{'class': 'nextpostslink'})
	xbmc.log('NEXT: ' + str(len(nxt)))
	if len(nxt) > 0:
		nxt = nxt[0]
		nurl = nxt.get('href')
		xbmc.log('NURL: ' + str(nurl))
	for item in soup:
		title = striphtml(str(item.find('a')))
		image = defaultimage#item.find('img',{'typeof':'foaf:Image'})
		thumbnail = item.find('img')['src']
		url = item.find('a')['href']
		purl = 'plugin://plugin.video.bnwmovies?mode=637&url=' + url + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(thumbnail)
		li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
		li.setProperty('fanart_image', defaultfanart)
		li.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url)),('Plot Info', 'XBMC.RunPlugin(%s?mode=81&url=%s)' % (sys.argv[0], url))])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li)
		xbmcplugin.setContent(addon_handle, 'movies')
	if len(nxt) > 0:
		add_directory2('Next Page',nurl,636,defaultfanart,defaultimage,plot='Next Page')
	xbmcplugin.endOfDirectory(addon_handle)


#637
def episode(name,url,iconimage):
	response = get_html(url)
	soup = BeautifulSoup(response,'html.parser').find_all('div',{'class': 'box-holder cf centered'})[0]
	links = re.compile('<source src="(.+?)"').findall(str(soup));i = 0
	xbmc.log('links: ' + str(links))
	ret = xbmcgui.Dialog().select('Select File',links)
	xbmc.log(str(ret))
	url = links[ret]
	streams(name,url,iconimage)


#650
def streams(name,url,iconimage):
	item = xbmcgui.ListItem(name, path=url, thumbnailImage=iconimage)
	xbmc.log('URL: ' + str(url))
	xbmc.Player().play( url, item )
	sys.exit("Stop Video")
	xbmcplugin.endOfDirectory(addon_handle)


#81
def plot_info(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser').find_all('span',{'itemprop': 'description'})
	plot = (striphtml(str(soup)))[1:-1]
	xbmcgui.Dialog().ok('Plot Info', plot)


#80
def downloader(url):
		xbmc.log('DOWNLOAD')
		path = addon.getSetting('download')
		if path == "":
			xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
					%(translation(30000), translation(30010), defaulticon))
			addon.openSettings()
			path = addon.getSetting('download')
		if path == "":
			return
		html = get_html(url)
		xbmcgui.Dialog().notification('B&W Movies', 'Getting Download URL.', xbmcgui.NOTIFICATION_INFO, 5000)
		links = re.compile('<source src="(.+?)"').findall(str(html))
		types = ([link.split('.')[-1].upper() for link in links])
		#xbmc.log('links: ' + str(types))
		sizes = [];items = []
		for link in links:
			u = urllib2.urlopen(link)
			#f = open(download+file_name, 'wb')
			meta = u.info()
			file_size = float(meta.getheaders("Content-Length")[0])
			#xbmc.log('FILE SIZE: ' + str(file_size))
			file_sizeMB = str(float(file_size/(1024*1024))).split('.')[0] + ' MB'
			#xbmc.log('FILE SIZE MB: ' + str(file_sizeMB))
			sizes.append(file_sizeMB)
		for type,size in zip(types,sizes):
			info = type + ' ' + size
			#xbmc.log('INFO: ' + str(info))
			items.append(info)
		#xbmc.log('SIZES: ' + str(sizes))
		ret = xbmcgui.Dialog().select('Select File Type',items)
		xbmc.log('RET: ' + str(ret))
		if ret == -1:
			return videos
		xbmc.log(str(ret))
		url = links[ret]
		url = resolve_http_redirect(url)
		xbmc.log('FINAL URL: ' + str(url))
		file_name = url.split('/')[-1]
		dlsn = settings.getSetting(id="status")
		bsize = settings.getSetting(id="bsize")
		print 'bfr Size= ' + str(bsize)
		ret = xbmcgui.Dialog().yesno("B&W Movies", 'Download Selected File?', str(file_name))
		if ret == False:
			return videos
		else:
			xbmcgui.Dialog().notification('B&W Movies', 'Download Started.', xbmcgui.NOTIFICATION_INFO, 3000)
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
			bfr = u.read(block_sz)
			if not bfr:
				break
			file_size_dl += float(len(bfr))
			file_size_dlMB = float(file_size_dl/(1024*1024))
			f.write(bfr)
			status = "%.2f  [%3.2f%%]" % (file_size_dlMB, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			if dlsn!='false':
				xbmcgui.Dialog().notification('B&W Movies Download in Progress', str(status) + ' of ' + ("%.2f" % float(file_sizeMB)) + ' MB', xbmcgui.NOTIFICATION_INFO, 2500)
			else:
				break
		f.close()
		xbmcgui.Dialog().notification('B&W Movies', 'Download Completed.', xbmcgui.NOTIFICATION_INFO, 5000)
		print 'Download Completed'


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(url):
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def resolve_http_redirect(url, depth=0):
    if depth > 10:
        raise Exception("Redirected "+depth+" times, giving up.")
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if headers.has_key('location') and headers['location'] != url:
        return resolve_http_redirect(headers['location'], depth+1)
    else:
        return url


def add_directory2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot,
												"Premiered": airdate} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
		return ok


def add_directory(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot,
												"Premiered": airdate} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok

def get_html(url):
	req = urllib2.Request(url)
	#req.add_header('Host','www.fox.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/50.0')
	#req.add_header('Referer','http://www.fox.com')

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

xbmc.log("Mode: " + str(mode))
xbmc.log("URL: " + str(url))
xbmc.log("Name: " + str(name))

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu")
	shows()
elif mode == 4:
	xbmc.log("Play Video")
elif mode == 80:
	print "Download File"
	downloader(url)
elif mode==81:
	xbmc.log("Get Plot Info")
	plot_info(url)
elif mode==633:
	xbmc.log("Black and White Shows")
	shows()
elif mode==635:
	xbmc.log("Black and White Archive")
	archives(url)
elif mode==636:
	xbmc.log("Black and White Videos")
	videos(url)
elif mode==637:
	xbmc.log("Black and White Episode")
	episode(name,url,iconimage)
elif mode==638:
	xbmc.log("Black and White Most Watched")
	most_watched(name,url)
elif mode==639:
	xbmc.log("Black and White More Shows")
	more_shows(name,url)
elif mode==650:
	xbmc.log("Black and White Shows")
	streams(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
