#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later
# 2018.12.02

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, re, xbmcplugin, sys
from bs4 import BeautifulSoup
import mechanize
import html5lib
import simplejson as json

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/48.0')]

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.reuters')
translation = selfAddon.getLocalizedString
settings = xbmcaddon.Addon(id="plugin.video.reuters")

log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)
QUALITY = settings.getSetting(id="quality")
xbmc.log('QUALITY: ' + str(QUALITY),level=log_level)
SITE = settings.getSetting(id="site")
if SITE == '1':
	edition = '?edition=US'
else:
	edition = '?edition=XW'
LENGTH = settings.getSetting(id="length")

defaultimage = 'special://home/addons/plugin.video.reuters/icon.png'
defaultfanart = 'special://home/addons/plugin.video.reuters/fanart.jpg'
baseurl = 'http://www.reuters.tv/'
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}

addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508]
plugin = 'Reuters TV'


def CATEGORIES():
	addDir('Live Stream', baseurl + 'live', 20, defaultimage)
	addDir('Upcoming', baseurl + 'live', 25, defaultimage)
	addDir('Top Stories', 'http://www.reuters.tv/data/json/' + edition + '&time=' + LENGTH, 10, defaultimage)
	addDir('Featured', baseurl + 'featured' + edition, 30, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#10
def TOP(name,url):
	opener = urllib2.build_opener()
	f = opener.open(url)
	html = f.read()
	top_urls = re.compile('HLS","uri":"(.+?)","entityType').findall(html)
	xbmc.log('TOP_URLS: ' + str(top_urls),level=log_level)
	## Attempt to Remove Ads
	for url in top_urls:
		#xbmc.log('URL: ' + str(url),level=log_level)
		plist = str(re.findall(r'assets/(.*?)/master', url))[2:-2].split(',')
		for item in plist[1:-1]:
			if item[:2] == '14':
				plist.remove(item)
			if item[:1] == 'm':
				plist.remove(item)
		playlist = str(plist)[1:-1].replace("'","").replace(' ','')
		#xbmc.log('PLAYLIST: ' + str(playlist),level=log_level)
		if QUALITY == '2':
			res = '1920x1080'
		elif QUALITY == '1':
			res = '1280x720'
		else:
			res = '960x540'
		no_ads = 'https://22-cf-deb05f50f65540958a4bad40060cbbc7.vip2-dal1.dlvr1.net/6d0d214e-f63f-11e8-bc72-f166d0a6bbcf/rest/v2/playlist/assets/' + playlist + '/rendered/resolution/' + res +'/codecs/ignored.m3u8'
		PLAY('Top Stories',no_ads)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#20
def LIVE(name,url):
	test = get_html('http://www.reuters.tv/liveNowIndicator')
	xbmc.log('LIVE TEST: ' + str(test),level=log_level)
	if 'false' in test:
		xbmc.log('NOT LIVE',level=log_level)
		line1 = "No Live Content Currently Available"
		xbmcgui.Dialog().ok(plugin, line1)
		sys.exit()
	br.set_handle_robots( False )
	response = br.open(url)
	html = response.get_data()
	live_urls = re.compile('HLS","uri":"(.+?)"').findall(html)
	#xbmc.log('LIVE_URLS: ' + str(len(live_urls)),level=log_level)
	titles = re.compile(',"title":"(.+?)"').findall(html)
	for url, title in zip(live_urls, titles):
		if 'churro' in url:
			live_stream = url
	playlist = get_html(live_stream)
	streams = re.findall(r'[h]\S*', playlist)
	print str(streams)
	if QUALITY == '2':
		res = '-1'
	elif QUALITY == '1':
		res = '-2'
	else:
		res = '-3'
	PLAY(title, streams[int(res)])
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#25
def UPCOMING(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'playlist'})
	xbmc.log('SOUP LENGTH: ' + str(len(soup)),level=log_level)
	for item in soup:
		live_time = item.find('span',{'class':'live-time'}).text
		if 'ago' in live_time:
			continue
		title = live_time + ': ' + item.find('h2').text.encode('ascii','ignore')
		if 'LIVE' in title:
			mode = 20
			url = baseurl + 'live'
		else:
			mode = None
			url = baseurl #+ item.find('a')['href']
		image = defaultimage #'http:' + item.find('img')['src']
		addDir2(title, url, mode, image)
	jsob = re.compile('RTVJson = (.+?);\\n</script>').findall(str(html));i=0
	xbmc.log('JSOB: ' + str(len(jsob[-1])),level=log_level)
	jdata = json.loads(jsob[-1])
	for item in jdata:
		title = jdata['items'][i]['title'].encode('ascii','ignore')
		status = jdata['items'][i]['type']
		stream = jdata['items'][i]['resources'][-1]['uri']
		image = defaultimage #'http:' + item.find('img')['src']
		title = status.split('_')[-1] + ': ' + title
		addDir2(title, stream, 99, defaultimage);i=i+1
	xbmc.log('ITEMS: ' + str(i),level=log_level)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#30
def FEATURED(name,url):
	html = get_html(url)
	jsob = re.compile('RTVJson = (.+?);\\n</script>').findall(str(html));i=0
	xbmc.log('JSOB LENGTH: ' + str(len(jsob)),level=log_level)
	jdata = json.loads(jsob[-1])
	json_data = json.dumps(jdata)
	item_dict = json.loads(json_data)
	xbmc.log('JSOB ITEMS: ' + str(len(item_dict['items'])),level=log_level)
	total = int(len(item_dict['items']))
	for i in range(total):
		title = jdata['items'][i]['title'].encode('ascii','ignore')
		url = jdata['items'][i]['resources'][0]['uri']
		image = jdata['items'][i]['resources'][3]['uri']
		addDir(title, url, 50, image);i=i+1
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#40
def VIDEOS(name,url):
	response = br.open(url)
	html = response.get_data()
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'cat-single-video'})
	xbmc.log('SOUP LENGTH: ' + str(len(soup)),level=log_level)
	for item in soup:
		title = item.find('h3').text.encode('ascii','ignore')#.title()
		url = item.find('a')['href']#baseurl +
		image = item.find('img')['src']#'http:' +
		addDir2(title, url, 50, image)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#50
def VIDEO(name,url):
	response = br.open(url)
	jsob = response.get_data()
	jdata = json.loads(jsob)
	video_url = jdata['entity']['stream']['uri']
	xbmc.log('VIDEO URL: ' + str(video_url),level=log_level)
	## Attempt to Remove Ads
	for url in video_url:
		#xbmc.log('URL: ' + str(url),level=log_level)
		plist = str(re.findall(r'assets/(.*?)/master', video_url))[2:-2].split(',')
		xbmc.log('PLIST: ' + str(plist),level=log_level)
		for item in plist[1:-1]:
			if item[:2] == '14':
				plist.remove(item)
			if item[:1] == 'm':
				plist.remove(item)
		playlist = str(plist)[1:-1].replace("'","").replace(' ','').replace('"','')
		xbmc.log('PLAYLIST: ' + str(playlist),level=log_level)
		if QUALITY == '2':
			res = '1920x1080'
		elif QUALITY == '1':
			res = '1280x720'
		else:
			res = '960x540'
		no_ads = 'https://deb05f50f65540958a4bad40060cbbc7.dlvr1.net/rest/v2/playlist/assets/' + playlist + '/rendered/resolution/' + res +'/codecs/ignored.m3u8'
	PLAY(name, no_ads)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	listitem.setInfo(type="Video", infoLabels={"Title": name})
	#listitem.setProperty('IsPlayable', 'true')
	#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def addDir(name, url, mode, iconimage, fanart=False, infoLabels=True):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + str(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name, url, mode, iconimage, fanart=False, infoLabels=True):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + str(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok


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
	#req.add_header('Host', 'www.reuters.tv')
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0')
	#req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	#req.add_header('Cookie', 'standings=46; __utma=112427159.1801477545.1473479776.1473479776.1473479776.1; __utmz=112427159.1473479776.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); screen_width=1189; _ga=GA1.2.1801477545.1473479776; ASP.NET_SessionId=ilnama55rt0g0xepaxvwcd45; __utmc=112427159; _gat_tracker0=1')

	try:
		response = urllib2.urlopen(req, timeout = 5)
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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("Reuters Videos",level=log_level)
	CATEGORIES()
elif mode == 10:
	xbmc.log("Reuters Top Stories",level=log_level)
	TOP(name,url)
elif mode == 20:
	xbmc.log("Reuters Live",level=log_level)
	LIVE(name,url)
elif mode == 25:
	xbmc.log("Reuters Upcoming",level=log_level)
	UPCOMING(name,url)
elif mode == 30:
	xbmc.log("Reuters Featured",level=log_level)
	FEATURED(name,url)
elif mode == 40:
	xbmc.log("Reuters Videos",level=log_level)
	VIDEOS(name,url)
elif mode == 50:
	xbmc.log("Reuters Video",level=log_level)
	VIDEO(name,url)
elif mode == 99:
	xbmc.log("Play Video",level=log_level)
	PLAY(name,url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
