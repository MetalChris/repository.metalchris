#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2 or Later)

#2019.02.01

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
__resource__   = xbmc.translatePath( os.path.join( _addon_path, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

#from uas import *

br = mechanize.Browser()
br.set_cookiejar(CookieJar)
br.set_handle_robots(False)
br.set_handle_equiv(False)

defaultimage = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaultfanart = 'special://home/addons/plugin.video.powernationtv/fanart.jpg'
defaultvideo = 'special://home/addons/plugin.video.powernationtv/icon.png'
defaulticon = 'special://home/addons/plugin.video.powernationtv/icon.png'
baseurl = 'https://www.powernationtv.com/'
login_url = 'https://www.powernationtv.com/user/login?redir=/'

free = settings.getSetting(id="free")
username = settings.getSetting(id="username")
password = settings.getSetting(id="password")
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

#headers = {'Host': 'www.powernationtv.com', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', 'Referer': 'https://www.powernationtv.com/'
#}


def CATEGORIES():
	html = get_html(baseurl)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'show_card'})
	xbmc.log('SOUP: ' + str(len(soup)),level=log_level)
	for show in soup:
		url = show.find('a')['href']
		if len(str(url)) < 1:
			continue
		if not 'shows' in url:
			continue
		title = show.find('img')['alt'].strip()
		#image = show.find('img')['data-pagespeed-lazy-src']
		image = 'special://home/addons/plugin.video.powernationtv/resources/media/' + title + '.jpg'
		if ('Shorts' in title) or ('Daily' in title):
			continue
		addDir(title, url, 10, image)
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#10
def INDEX(url):
	xbmc.log('GET SHOWS',level=log_level)
	html = br.open(url).read(); murl = url
	xbmc.log('MURL: ' + str(murl),level=log_level)
	if 'powernation-' in murl:
		xbmc.log('POWERNATION SHOW',level=log_level)
		PN_SHOW(url)
		sys.exit()
	surl = BeautifulSoup(html,'html5lib').find_all('link',{'rel':'alternate'})[1]
	s_url = re.compile('href="(.+?)"').findall(str(surl))[0].rpartition('/')[0]
	html = get_html(s_url)
	seasons = BeautifulSoup(html,'html5lib').find_all('li',{'class':'sublink'})
	xbmc.log('SEASONS: ' + str(len(seasons)),level=log_level)
	if free != 'false':
		x = 0
	else:
		x = 2
	for s in seasons[x:]:
		season = s_url + s.find('a')['href']
		title = s.find('a').text
		addDir(title, season, 15, defaultimage, defaultfanart)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode'})#;e=0
	for episode in soup:
		#If it's a "coming soon" show, skip it
		if episode.find(class_="coming_soon"):
			continue
		if episode.find(class_='pnplus-episode-logo'):
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
			addDir2(title, url, 20, image, defaultfanart, infolabels)#;e=e+1
		else:
			season_info = episode.find('div', {'class':'season'}).text.encode('ascii','ignore').strip()
			title = title + ' - ' + str(season_info)
			plot = episode.find('div',{'class':'description'}).text
			infolabels = {'plot': plot, 'season': '99', 'episode': '99'}
			addDir(title, url, 15, image, defaultfanart, infolabels)#;e=e+1
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)

def PN_SHOW(url):
	xbmc.log('PN_SHOW',level=log_level)
	html = br.open(url).read(); murl = url
	xbmc.log('MURL: ' + str(murl),level=log_level)
	soup = BeautifulSoup(html,'html5lib').find_all('li',{'class':'sublink'})#[1]
	for sublink in soup:
		url = murl + sublink.find('a')['href']
		if not '-garage' in murl:
			link = PN_LINK(url)
			mode = 20
		else:
			link = url
			mode = 25 #something else
		image = defaultimage
		year = sublink.find('a')['data-year']
		title = sublink.find('a').text + ' ' + year
		infolabels = {'plot': title, 'season': year, 'episode': '1'}
		if mode == 20:
			addDir2(title, link, mode, image, defaultfanart, infolabels)
		else:
			addDir3(title, link, mode, defaultfanart, image, title)
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)

def PN_LINK(url):
	xbmc.log('PN_LINK',level=log_level)
	html = br.open(url).read(); murl = url
	xbmc.log('MURL: ' + str(murl),level=log_level)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'id':'episodes'})
	for video in soup:
		link = video.find('a')['href']
		return link

#25
def PNG(name,url):
	xbmc.log('PNG',level=log_level)
	html = br.open(url).read()
	code = url.split('?')[-1]
	year = re.compile('year=(.+?)&').findall(code)[0]
	month = re.compile('month=(.+?)#').findall(code)[0]
	soup = BeautifulSoup(html,'html5lib')
	xbmc.log('SOUP: ' + str(len(soup)),level=log_level)
	divTag = soup.find_all('div',{'id':'episodes' +year + month})
	for tag in divTag:
		tdTags = tag.find_all("div", {"class": "episode"})
	xbmc.log('divTag: ' + str(len(divTag)),level=log_level)
	xbmc.log('tdTags: ' + str(len(tdTags)),level=log_level)
	for episode in tdTags:
		title = episode.find('div',{'class':'title'}).text.encode('ascii','ignore').strip()
		image = episode.find('img')['src']
		url = episode.find('a')['href']
		surl = 'plugin://plugin.video.powernationtv?mode=20&url=' + urllib.quote_plus(url)
		plot = episode.find('div',{'class':'description'}).text.encode('ascii','ignore').strip()
		#infolabels = {'plot': title, 'season': year, 'episode': '1'}
		#addDir3(title, url, 20, defaultfanart, image, title)
		li = xbmcgui.ListItem(title)
		li.setInfo(type="Video", infoLabels={"mediatype":"video","label":title,"title":title,"genre":"Sports",'plot': plot})#, 'season': season, 'episode':episode})
		li.setProperty('IsPlayable', 'True')
		li.setArt({'thumb':image,'fanart':defaultfanart})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=surl, listitem=li, isFolder=False)
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#15
def BUILD(url):
	s_num = name.split(' ')[-1]
	xbmc.log('S_NUM: ' + str(s_num),level=log_level)
	if s_num == 'Episodes':
		builds(url,s_num)
		sys.exit()
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib')
	divTag = soup.find_all("div", {"id": "episodes"})
	for tag in divTag:
		tdTags = tag.find_all("div", {"class": "episode"})
	xbmc.log('divTag: ' + str(len(divTag)),level=log_level)
	xbmc.log('tdTags: ' + str(len(tdTags)),level=log_level)
	episodes = tdTags
	EPISODES(episodes,s_num)


def builds(url,s_num):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'episode'})#;e=0#;titles = []
	episodes = soup
	EPISODES(episodes,s_num)


def EPISODES(episodes,s_num):
	for episode in episodes:
		#If it's a "coming soon" show, skip it
		if episode.find(class_="coming_soon"):
			continue
		#If it's a "subscription" show, skip it
		if free == 'false':
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
			if (s_num == 'Episodes'):
				pass
			elif (season != s_num):
				continue
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
	if free != 'false':
		br = mechanize.Browser()
		br.set_cookiejar(CookieJar)
		br.set_handle_robots(False)
		br.set_handle_equiv(False)
		br.open(url)
		for cookie in CookieJar:
			#xbmc.log('===== LOGOUT =====',level=log_level)
			#xbmc.log('COOKIE: ' + str(cookie),level=log_level)
			CookieJar.set_cookie(cookie)
		CookieJar.save(ignore_discard=True)
		xbmc.log('COOKIEJAR: ' + str(CookieJar),level=log_level)
		br.addheaders = [('Cookie', cookie)]
		xbmc.log('COOKIE: ' + str(cookie),level=log_level)
		br.addheaders = [('Referer', url)]
		sign_in = br.open(login_url)
		br.select_form(nr=0)
		br.form['email'] = username
		br.form['password'] = password
		logged_in = br.submit()
		br.set_handle_redirect(mechanize.HTTPRedirectHandler)
		check = logged_in.read()
		if 'span class="caret"' in str(check):
			xbmc.log('LOGGED IN',level=log_level)
			xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
		else:
			xbmc.log('NOT LOGGED IN',level=log_level)
			xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 2500, False)
			sys.exit()
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_cookiejar(CookieJar)
	xbmc.log('URL: ' + str(url),level=log_level)
	urls = url.split('/')
	key = urls[4]
	params = {'id': str(key)}
	#params = {'id': 'PNG-0072'}
	params = urllib.urlencode(params)
	xbmc.log('PARAMS: ' + str(params),level=log_level)
	ss = br.open(url).read()
	X_CSRF_TOKEN = re.compile('name="csrf-token" content="(.+?)"').findall(ss)
	xbmc.log('X_CSRF_TOKEN: ' + str(X_CSRF_TOKEN),level=log_level)
	soup = BeautifulSoup(ss,'html5lib').find_all('div',{'class':'embargo'})
	if len(soup) > 0:
		embargo = striphtml(str(soup[0])).replace('\n',' ')
		xbmcgui.Dialog().notification(plugin, embargo, defaultimage, 7500, False)
		sys.exit()
		pass

	br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'),
				('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
				('Accept', 'application/json, text/javascript, */*; q=0.01'),
				('X-Requested-With', 'XMLHttpRequest'),
				('X-CSRF-TOKEN', X_CSRF_TOKEN[0]),
				('Host', 'Host: www.powernationtv.com'),
				('Referer', url)]
	page = br.open('https://www.powernationtv.com/episode/meta', params).read()
	#page = br.open('https://www.powernationtv.com/episode/meta?id=PNG-0072').read()
	xbmc.log('PAGE:' + str(page[:100]),level=log_level)
	canview = re.compile('canView":(.+?),').findall(page)[0]
	if canview == 'false':
		xbmc.log('NOT FREE',level=log_level)
		xbmcgui.Dialog().notification(plugin, 'Subsription Required for This Episode', defaultimage, 2500, False)
		sys.exit()
		pass
	stream = re.compile('hls_url":"(.+?)"').findall(page)[0].replace('\\','').replace('https','http')
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	xbmc.log('STREAM: ' + str(stream),level=log_level)
	PLAY(name,stream)
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
		liz.setInfo( type="Video", infoLabels={"Title": name, "plot": infoLabels['plot'], "episode": infoLabels['episode'], "season": infoLabels['season']} )
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
	xbmc.log("PowerNation Garage",level=log_level)
	PNG(name,url)
elif mode == 99:
	xbmc.log("Play PowerNation Stream",level=log_level)
	PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
