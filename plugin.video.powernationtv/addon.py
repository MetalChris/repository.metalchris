#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

#2019.01.27

import xbmcaddon, urllib, xbmcgui, xbmcplugin, urllib2, re, sys, os
from bs4 import BeautifulSoup
import html5lib
import mechanize
import cookielib

#LOGDEBUG

settings = xbmcaddon.Addon(id="plugin.video.powernationtv")
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.powernationtv')
translation = selfAddon.getLocalizedString
cookies = xbmc.translatePath(os.path.join(addon_path_profile+'cookies.lwp'))
CookieJar = cookielib.LWPCookieJar(os.path.join(addon_path_profile, 'cookies.lwp'))
br = mechanize.Browser()
br.set_cookiejar(CookieJar)
br.set_handle_robots(False)
br.set_handle_equiv(False)

defaultimage = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaultfanart = 'special://home/addons/plugin.video.powernationtv/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaulticon = 'special://home/addons/plugin.video.powernationtv/icon.png'
baseurl = 'https://www.powernationtv.com/'

addon_handle = int(sys.argv[1])
confluence_views = [500,501,503,504,515]
force_views = settings.getSetting(id="force_views")
log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)
plugin = 'PowerNation TV'




def CATEGORIES():
	html = get_html(baseurl)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'show_card'})
	#soup = BeautifulSoup(html,'html5lib').find_all('a',{'class':'dropdown-item'})
	xbmc.log('SOUP: ' + str(len(soup)),level=log_level)
	for show in soup:
		url = show.find('a')['href']
		if len(str(url)) < 1:
			continue
		if not 'shows' in url:
			continue
		image = show.find('img')['data-pagespeed-lazy-src']
		title = show.find('img')['alt'].strip()
		if ('Shorts' in title) or ('Daily' in title):
			continue
		addDir(title, url, 10, image)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#10
def INDEX(url):
	xbmc.log('GET SHOWS',level=log_level)
	html = get_html(url); murl = url
	xbmc.log('MURL: ' + str(murl),level=log_level)
	surl = BeautifulSoup(html,'html5lib').find_all('link',{'rel':'alternate'})[1]
	#xbmc.log('SURL: ' + str(surl),level=log_level)
	s_url = re.compile('href="(.+?)"').findall(str(surl))[0].rpartition('/')[0]
	#xbmc.log('S_URL: ' + str(s_url),level=log_level)
	html = get_html(s_url)
	seasons = BeautifulSoup(html,'html5lib').find_all('li',{'class':'sublink'})
	#seasons = BeautifulSoup(html,'html5lib').find_all('ul')
	xbmc.log('SEASONS: ' + str(len(seasons)),level=log_level)
	#xbmc.log('SEASONS: ' + str(seasons),level=log_level)
	#xbmc.log('FOUND',level=log_level)
	for s in seasons[2:]:
		season = s_url + s.find('a')['href']
		title = s.find('a').text
		#xbmc.log('SEASON: ' + str(title),level=log_level)
		#xbmc.log('SEASON: ' + str(season),level=log_level)
		addDir(title, season, 15, defaultimage, defaultfanart)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode'});e=0
	for episode in soup:
		#If it's a "coming soon" show, skip it
		if episode.find(class_="coming_soon"):
			continue
		#If it's a "subscription" show, skip it
		if episode.find(class_="fas fa-play-circle play"):
			continue
		title = episode.find('div', {'class': 'title'}).text.encode('ascii','ignore').strip()
		url = episode.find('a')['href']
		if not 'https:' in url:
			url = 'https:' + episode.find('a')['href']
		image = re.compile('src="(.+?)"').findall(str(episode))[0].replace('&amp;','&')#.replace('https','http')
		if episode.find('i'):
			#If it has metadata, add it to the episode info
			plot = episode.find('div', {'class':'description'}).text.encode('ascii','ignore').strip()
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip().split(',')
			season = season_info[0].split(' ')[1]
			episode = season_info[1].split(' ')[2]
			infolabels = {'plot': plot, 'season': season, 'episode':episode}
			addDir(title, url, 20, image, defaultfanart, infolabels);e=e+1
		else:
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip()
			title = title + ' - ' + str(season_info)
			addDir(title, url, 15, image, defaultfanart);e=e+1
		xbmcplugin.setContent(addon_handle, 'episodes')
	#xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	#addDir('More Episodes', murl, 25, defaultimage, defaultfanart)
	#Fix the sort to be proper episode number order
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#15
def BUILD(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode'});e=0
	for episode in soup:
		#If it's a "coming soon" show, skip it
		if episode.find(class_="coming_soon"):
			continue
		#If it's a "subscription" show, skip it
		if episode.find(class_="pnplus-episode-logo"):
			continue
		title = episode.find('div', {'class': 'title'}).text.encode('ascii','ignore').strip()
		url = episode.find('a')['href']
		if not 'https:' in url:
			url = 'https:' + episode.find('a')['href']
		image = re.compile('src="(.+?)"').findall(str(episode))[0].replace('&amp;','&')
		if not episode.find('div', {'class':'season'}):
			continue
		if episode.find('i'):
			#If it has metadata, add it to the episode info
			plot = episode.find('div', {'class':'description'}).text.encode('ascii','ignore').strip()
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip().split(',')
			season = season_info[0].split(' ')[1]
			episode = season_info[1].split(' ')[2]
			infolabels = {'plot': plot, 'season': season, 'episode':episode}
			surl = 'plugin://plugin.video.powernationtv?mode=20&url=' + urllib.quote_plus(url)
			li = xbmcgui.ListItem(title)
			li.setProperty('IsPlayable', 'true')
			li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"Sports",'plot': plot, 'season': season, 'episode':episode})
			li.setArt({'thumb':image,'fanart':defaultfanart})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=surl, listitem=li, isFolder=False)
		xbmcplugin.setContent(addon_handle, 'episodes')
	#Fix the sort to be proper episode number order
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#20
def IFRAME(name,url):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_cookiejar(CookieJar)
	xbmc.log('URL: ' + str(url),level=log_level)
	urls = url.split('/')
	key = urls[4]
	params = {'id': str(key)}
	params = urllib.urlencode(params)
	xbmc.log('PARAMS: ' + str(params),level=log_level)
	s = br.open(url).read()
	X_CSRF_TOKEN = re.compile('name="csrf-token" content="(.+?)"').findall(s)
	xbmc.log('X_CSRF_TOKEN: ' + str(X_CSRF_TOKEN),level=log_level)

	br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'),
				('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
				('Accept', 'application/json, text/javascript, */*; q=0.01'),
				('X-Requested-With', 'XMLHttpRequest'),
				('X-CSRF-TOKEN', X_CSRF_TOKEN[0]),
				('Host', 'Host: www.powernationtv.com'),
				('Referer', url)]
	page = br.open('https://www.powernationtv.com/episode/meta', params).read()
	xbmc.log('PAGE:' + str(page[:100]),level=log_level)

	stream = re.compile('hls_url":"(.+?)"').findall(page)[0].replace('\\','').replace('https','http')
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.log('STREAM: ' + str(stream),level=log_level)
	#xbmc.Player().play( stream, listitem )
	#sys.exit()
	PLAY(name,stream)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#25
def SEASONS(url):
	html = get_html(url)
	seasons = BeautifulSoup(html,'html5lib').find_all('div',{'class':'season-dropdown'})
	soup = BeautifulSoup(str(seasons),'html5lib').find_all('li')
	for season in soup:
		title = season.find('a').text.encode('ascii','ignore').strip()
		if not 'Season' in title:
			continue
		value = re.compile('season="(.+?)"').findall(str(season))[0]
		addDir(title, url + '?' + value, 30, defaultimage, defaultfanart)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#30
def GET_SEASON(name,url):
	value = url.split('?')[-1]
	url = url.split('?')[0]
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_cookiejar(CookieJar)
	xbmc.log('URL: ' + str(url),level=log_level)
	params = {'season': str(value)}
	params = urllib.urlencode(params)
	xbmc.log('PARAMS: ' + str(params),level=log_level)
	s = br.open(url).read()
	X_CSRF_TOKEN = re.compile('name="csrf-token" content="(.+?)"').findall(s)
	xbmc.log('X_CSRF_TOKEN: ' + str(X_CSRF_TOKEN),level=log_level)
	br.addheaders = [('Host', 'Host: www.powernationtv.com'),
				('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'),
				('Accept', 'application/json, text/javascript, */*; q=0.01'),
				('Referer', url),
				('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
				('X-CSRF-TOKEN', X_CSRF_TOKEN[0]),
				('X-Requested-With', 'XMLHttpRequest')]
	br.set_handle_robots(False)
	br.set_cookiejar(CookieJar)
	page = br.open('https://www.powernationtv.com/episode/filter', params).read()
	html = re.compile('{"html":"(.+?)"}').findall(page)
	html = html[0].replace('\\n','').replace('\\','')
	#xbmc.log('Page: ' + str(html),level=log_level)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode'});e=0
	for episode in soup:
		#If it's a "coming soon" show, skip it
		if episode.find(class_="coming_soon"):
			continue
		title = episode.find('div', {'class': 'title'}).text.encode('ascii','ignore').strip()
		url = episode.find('a')['href']
		if not 'https:' in url:
			url = 'https:' + episode.find('a')['href']
		image = re.compile('src="(.+?)"').findall(str(episode))[0].replace('&amp;','&')
		if episode.find('i'):
			#If it has metadata, add it to the episode info
			plot = episode.find('div', {'class':'description'}).text.encode('ascii','ignore').strip()
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip().split(',')
			season = season_info[0].split(' ')[1]
			episode = season_info[1].split(' ')[2]
			infolabels = {'plot': plot, 'season': season, 'episode':episode}
			addDir(title, url, 20, image, defaultfanart, infolabels);e=e+1
		else:
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip()
			title = title + ' - ' + str(season_info)
			addDir(title, url, 15, image, defaultfanart);e=e+1
		xbmcplugin.setContent(addon_handle, 'episodes')
	#xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	#Fix the sort to be proper episode number order
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#35
def YMM(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('a',{'class':'lighttype'})
	xbmc.log(str(len(soup)),level=log_level)
	for makes in soup:
		title = makes.get('title')
		url = makes.get('href')
		if not 'http:' in url:
			url = 'http:' + url
		addDir(title, url, 40, defaultimage)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#40
def MODELS(name,url):
	html = get_html(url)
	group = BeautifulSoup(html,'html5lib').find_all('div',{'class':'tab-pane fade in active topspacing'})
	soup = BeautifulSoup(str(group),'html5lib').find_all('div',{'class':'pndaily_thumbnail col-xs-12'})
	xbmc.log(str(len(soup)),level=log_level)
	for models in soup:
		title = models.find('a')['title']
		url = models.find('a')['href']
		if not 'http:' in url:
			url = 'http:' + models.find('a')['href']
		image = models.find('img')['src']
		addDir(title, url, 50, image)
	xbmcplugin.setContent(addon_handle, 'episodes')
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
	xbmc.log(str(len(soup)),level=log_level)
	for makes in soup:
		title = makes.find('p').text
		url = makes.find('a')['href']
		if not 'http:' in url:
			url = 'http:' + url
		addDir(title, url, 20, defaultimage)
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(path=url)
	xbmc.log('### SETRESOLVEDURL ###',level=log_level)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	xbmc.log('URL: ' + str(url), level=log_level)
	xbmcplugin.endOfDirectory(addon_handle)


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
		liz.setInfo(type="Video", infoLabels={"Title": name, "plot": infoLabels['plot'], "episode": infoLabels['episode'], "season": infoLabels['season']})
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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("PowerNation TV Menu",level=log_level)
	CATEGORIES()
elif mode == 10:
	xbmc.log("PowerNation TV Videos",level=log_level)
	INDEX(url)
elif mode == 15:
	xbmc.log("PowerNation TV Build Videos",level=log_level)
	BUILD(url)
elif mode == 20:
	xbmc.log("PowerNation TV Play Video",level=log_level)
	IFRAME(name,url)
elif mode == 25:
	xbmc.log("PowerNation TV Seasons",level=log_level)
	SEASONS(url)
elif mode == 30:
	xbmc.log("PowerNation TV Get Season",level=log_level)
	GET_SEASON(name,url)
elif mode == 35:
	xbmc.log("PowerNation TV YMM Makes",level=log_level)
	YMM(name,url)
elif mode == 40:
	xbmc.log("PowerNation TV YMM Models",level=log_level)
	MODELS(name,url)
elif mode == 50:
	xbmc.log("PowerNation TV YMM Videos",level=log_level)
	YMM_VIDEOS(name,url)
elif mode == 60:
	xbmc.log("PowerNation TV 2 Minute Tech Videos",level=log_level)
	TECH(name,url)
elif mode == 99:
	xbmc.log("Play PowerNation Stream",level=log_level)
	PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
