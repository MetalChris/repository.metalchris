#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, platform, re, sys, os
import requests
import json
from bs4 import BeautifulSoup
import html5lib
import mechanize
import cookielib

artbase = 'special://home/addons/plugin.video.discovery-channels/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.discovery-channels')
translation = selfAddon.getLocalizedString
settings = xbmcaddon.Addon(id="plugin.video.discovery-channels")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
__resource__   = xbmc.translatePath( os.path.join( _addon_path, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

from uas import *

CookieJar = cookielib.LWPCookieJar(os.path.join(addon_path_profile, 'cookies.lwp'))
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', ua)]

plugin = "Discovery Channels"

defaultimage = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaulticon = 'special://home/addons/plugin.video.discovery-channels/icon.png'
defaultfanart = 'special://home/addons/plugin.video.discovery-channels/fanart.jpg'

local_string = xbmcaddon.Addon(id='plugin.video.discovery-channels').getLocalizedString
addon_handle = int(sys.argv[1])
p = settings.getSetting(id="parser")
xbmc.log('PARSER: ' + str(p))
player = settings.getSetting(id="player")
xbmc.log('PLAYER: ' + str(player))
confluence_views = [500,501,503,504,515]
force_views = settings.getSetting(id="force_views")

def channels():
	xbmc.log(str(platform.system()))
	xbmc.log(str(platform.release()))
	dsc = settings.getSetting(id="dsc")
	if dsc!='false':
		addDir2('Discovery Channel', 'https://www.discoverygo.com', 25, artbase + 'discovery.png')
	ap = settings.getSetting(id="ap")
	if ap!='false':
		addDir2('Animal Planet', 'https://www.animalplanetgo.com', 25, artbase + 'animalplanet.jpg')
	sci = settings.getSetting(id="sci")
	if sci!='false':
		addDir2('Discovery Science', 'https://www.sciencechannelgo.com', 25, artbase + 'sciencechannel.png')
	idsc = settings.getSetting(id="idsc")
	if idsc!='false':
		addDir2('Investigation Discovery', 'https://www.investigationdiscoverygo.com', 25, artbase + 'investigationdiscovery.jpg')
	dahn = settings.getSetting(id="dahn")
	if dahn!='false':
		addDir2('American Heroes', 'https://www.ahctvgo.com/', 25, artbase + 'ahctv.jpg')
	vel = settings.getSetting(id="vel")
	if vel!='false':
		addDir2('Velocity', 'https://www.velocitychannelgo.com', 25, artbase + 'velocity.png')
	dest = settings.getSetting(id="dest")
	if dest!='false':
		addDir2('Destination America', 'https://www.destinationamericago.com/', 25, artbase + 'destinationamerica.jpg')
	tlc = settings.getSetting(id="tlc")
	if tlc!='false':
		addDir2('TLC', 'https://www.discoverygo.com/tlc/', 25, artbase + 'tlc.jpg')
	dscl = settings.getSetting(id="dscl")
	if dscl!='false':
		addDir2('Discovery Life', 'https://www.discoverylifego.com', 25, artbase + 'discoverylife.jpg')
	dsck = settings.getSetting(id="dsck")
	if dsck!='false':
		addDir2('Discovery Kids', 'http://discoverykids.com/videos/', 535, artbase + 'discoverykids.jpg')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#25
def dsc_menu_new(url):
	site = 'https://www.' + (iconimage.rsplit('/', 1)[-1]).split('.')[0] + '.com'
	xbmc.log('SITE: ' + str(site), level=xbmc.LOGDEBUG)
	br.set_handle_robots( False )
	br.set_cookiejar(CookieJar)
	response = br.open(url)
	for cookie in CookieJar:
		#xbmc.log('COOKIE: ' + str(cookie))
		CookieJar.set_cookie(cookie)
	CookieJar.save(ignore_discard=True)
	page = response.get_data()
	if p == '2':
		xbmc.log('PARSER: ' + 'None', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page).find_all('div',{'class':'thumbnailTile__innerImage'})
	if p == '1':
		xbmc.log('PARSER: ' + 'html.parser', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page,'html.parser').find_all('div',{'class':'thumbnailTile__innerImage'})
	if p == '0':
		xbmc.log('PARSER: ' + 'html5lib', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'thumbnailTile__innerImage'})
	xbmc.log('SOUP Length: ' + str(len(soup)))
	#xbmc.log('SOUP: ' + str(soup[0]))
	titles = []
	for item in soup:
		if not item.find('div',{'class':'overlayInner overlayInner__overlayInner unlocked'}):
			continue
		txt = item.find_all('span',{'style':'display:block;overflow:hidden;height:0px;width:100%'})
		if len(txt) < 2:
			continue
		title = striphtml(str(txt[0])).replace("&amp;","&")
		if title in titles:
			continue
		titles.append(title)
		url = site + item.find('a')['href']
		image = item.find('img')['src']
		description = striphtml(str(txt[1])).replace('&amp;','&')
		add_directory3(title, url, 50, artbase + 'fanart2.jpg', image, plot=description)# + ' (' + runtime.replace('00:','') + ') ' + expiry)
		xbmcplugin.setContent(addon_handle, 'episodes')
		#i = i + 1
	if not 'tlc.com' in site:
		addDir('Find More Episodes From ' + name, url, 80, iconimage, artbase + 'fanart2.jpg')
		addDir(name +' Video Clips Sorted by Show', site, 533, iconimage, artbase + 'fanart2.jpg')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#50
def get_clips_new(name,url):
	site = url.split('/')[2]
	br.set_handle_robots( False )
	br.addheaders = [('Host', site)]
	br.addheaders = [('User-Agent', ua)]
	br.set_cookiejar(CookieJar)
	response = br.open(url)
	request = br.request
	xbmc.log('HEADERS: ' + str(request.header_items()), level=xbmc.LOGDEBUG)
	for cookie in CookieJar:
		xbmc.log('COOKIE: ' + str(cookie), level=xbmc.LOGDEBUG)
		CookieJar.set_cookie(cookie)
		if cookie.name == "eosAn":# and not cookie.is_expired():
			auth = 'Bearer ' +  re.compile('%2522%253A%2522(.+?)%2522%252C%2522').findall(str(cookie.value))[0]
			xbmc.log('AUTH: ' + str(auth), level=xbmc.LOGDEBUG)
			browser = mechanize.Browser()
			browser.addheaders = [('Host', 'api.discovery.com')]
			browser.addheaders = [('User-Agent', ua)]
			browser.addheaders = [('Referer', url)]
			browser.addheaders = [('Authorization', auth)]
			browser.set_handle_robots( False )
			#CookieJar.save(ignore_discard=True)
			response = browser.open(url)
			request = browser.request
			xbmc.log('HEADERS: ' + str(request.header_items()), level=xbmc.LOGDEBUG)
			page = response.get_data()
			video_id = re.compile('platform=desktop&video_id=(.+?)&networks').findall(str(page))[0]
			xbmc.log('VIDEO_ID: ' + str(video_id), level=xbmc.LOGDEBUG)
			video_url = 'http://api.discovery.com/v1/streaming/video/' + video_id + '?platform=desktop'
			response = browser.open(video_url)
			jsob = json.load(response)
			stream = jsob['streamUrl']
			xbmc.log('STREAM: ' + str(stream), level=xbmc.LOGDEBUG)
			play_episode(stream)
		elif auth == None:
			xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
			xbmc.log('CURRENTLY UNAVAILABLE')
			return
	xbmcplugin.endOfDirectory(addon_handle)


#80
def find_more(url):
	site = url.split('/')[2]
	br.set_handle_robots( False )
	response = br.open(url)
	page = response.get_data()
	if p == '2':
		xbmc.log('PARSER: ' + 'None', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page).find_all('div',{'class':'carousel-tile-wrapper carousel__tileWrapper'})
	if p == '1':
		xbmc.log('PARSER: ' + 'html.parser', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page,'html.parser').find_all('div',{'class':'carousel-tile-wrapper carousel__tileWrapper'})
	if p == '0':
		xbmc.log('PARSER: ' + 'html5lib', level=xbmc.LOGDEBUG)
		soup = BeautifulSoup(page,'html5lib').find_all('div',{'class':'carousel-tile-wrapper carousel__tileWrapper'})
	#soup4 = BeautifulSoup(html).find_all('div',{'class':'item small'})
	xbmc.log ('SOUP: ' + str(len(soup)), level=xbmc.LOGDEBUG)
	titles = []
	for item in soup:
		if not item.find('div',{'class':'overlayInner overlayInner__overlayInner unlocked'}):
			continue
		txt = item.find_all('span',{'style':'display:block;overflow:hidden;height:0px;width:100%'})
		#if len(txt) < 2:
			#continue
		title = striphtml(str(txt[0])).replace("&amp;","&")
		if title in titles:
			continue
		titles.append(title)
		url = 'https://' + site + item.find('a')['href']
		image = item.find('img')['src']
		description = striphtml(str(txt[1])).replace('&amp;','&')
		add_directory3(title, url, 50, artbase + 'fanart2.jpg', image, plot=description)# + ' (' + runtime.replace('00:','') + ') ' + expiry)
		xbmcplugin.setContent(addon_handle, 'episodes')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#532
def discovery_clips(url, iconimage):
	site = url.split('/tv')[0]
	try: html = urllib2.urlopen(url)
	except urllib2.HTTPError:
		xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
		return
	soup = BeautifulSoup(html,'html5lib').find_all("a",{"class":"thumbnailTile__link"})
	for item in soup:
		title = item.find('div',{'class':'thumbnailTile__lineTwo'}).text.encode('ascii', 'ignore')
		if 'Season' in title:
			continue
		link = site + item.get('href')
		add_directory2(title, link, 550, artbase + 'fanart2.jpg', iconimage,plot='')
	if force_views != 'false':
		xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#550
def get_clips(name,url):
	r = requests.get(url)
	video_id = re.compile('platform=desktop&video_id=(.+?)&networks').findall(str(r.content))[0]
	xbmc.log('VIDEO_ID: ' + str(video_id), level=xbmc.LOGDEBUG)
	video_url = 'http://api.discovery.com/v1/streaming/video/' + video_id + '?platform=desktop'
	opener = urllib2.build_opener()
	xbmc.log('COOKIES LENGTH: ' + str(len(r.cookies)))
	if len(str(r.cookies)) < 1:
		xbmcgui.Dialog().notification(name, 'Currently Unavailable.  Try Again Later', iconimage, 5000, False)
		xbmc.log('CURRENTLY UNAVAILABLE')
		return
	auth = 'Bearer ' + re.compile('%2522%253A%2522(.+?)%2522%252C%2522').findall(str(r.cookies))[0]
	opener.addheaders.append(('Host', 'api.discovery.com'))
	opener.addheaders.append(('User-Agent', ua))
	opener.addheaders.append(('Referer', url))
	opener.addheaders.append(('Authorization', auth))
	f = opener.open(video_url)
	page = f.read()
	jsob = json.loads(page)
	stream = jsob['streamUrl']
	xbmc.log('STREAM: ' + str(stream))
	PLAY(name,stream)
	xbmcplugin.endOfDirectory(addon_handle)


#533
def other_shows(url, iconimage):
	xbmc.log('ICONIMAGE: ' + str(iconimage), level=xbmc.LOGDEBUG)
	site = url.replace('/tv-shows/','')
	xbmc.log('SITE: ' + str(site), level=xbmc.LOGDEBUG)
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all("div",{"class":"headerMain__showDropDesktop"})[0]
	for show in soup.find_all("a")[1:]:
		tvshow = show.text.encode('utf-8').replace("&amp;","&")
		if not 'tlc.com' in url:
			link = site + show.get('href')#url.replace('videos', 'tv-shows') + show.get('data-ssid').split('/')[-1] + '?flat=1'
			mode = 532
		else:
			link = url.replace('videos', 'tv-shows') + show.get('data-ssid').split('/')[-1] + '?flat=2'
			mode = 534
		if 'aerospace' in link:
			continue
		add_directory2(tvshow, link, mode, artbase + 'fanart2.jpg', iconimage,plot='')
		if force_views != 'false':
			xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
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
		if force_views != 'false':
			xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
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
		if force_views != 'false':
			xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
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
		if force_views != 'false':
			xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[int(settings.getSetting(id="views"))])+")")
	xbmcplugin.endOfDirectory(addon_handle)


#537
def kids_stream(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib')
	try: url = soup.find('iframe')['src']
	except TypeError:
		xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
		return
	if 'facebook' in url:
		html = get_html(url)
		stream = (re.compile('hd_src_no_ratelimit":"(.+?)"').findall(str(html))[0]).replace('\\','')
		xbmc.log('STREAM: ' + str(stream))
	else:
		xbmcgui.Dialog().notification(name, ' No Streams Available', iconimage, 5000, False)
		return
	play(stream)
	xbmcplugin.endOfDirectory(addon_handle)


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


#99
def PLAY(name,url):
	listitem = xbmcgui.ListItem(name, thumbnailImage = defaultimage)
	listitem.setInfo(type="Video", infoLabels={"Title": name})
	listitem.setProperty('IsPlayable', 'true')
	#xbmc.Player().play( url + '&m3u8=yes', listitem )
	xbmc.Player().play( url, listitem )
	while xbmc.Player().isPlaying():
		continue
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#999
def play(url):
	xbmc.log('URL: ' + str(url))
	#item = xbmcgui.ListItem(path=url + '&m3u8=yes')
	item = xbmcgui.ListItem(path=url)
	item.setProperty('IsPlayable', 'true')
	return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


#999
def play_episode(url):
	xbmc.log('URL: ' + str(url))
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
	#commands = []
	#commands.append ----- THIS WORKS! -----
	#liz.addContextMenuItems([('Find More Like This', 'XBMC.RunPlugin(%s?mode=80&url=%s)' % (sys.argv[0], url))])
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
	xbmc.log("Discovery Channels")
	channels()
elif mode==80:
	xbmc.log("Find More")
	find_more(url)
elif mode==25:
	xbmc.log("DSC Menu")
	dsc_menu_new(url)
elif mode==31:
	xbmc.log("Discovery Shows")
	discovery_shows_new(name,url)
elif mode==50:
	xbmc.log("Discovery Episodes")
	get_clips_new(name,url)
elif mode==532:
	xbmc.log("Discovery Clips")
	discovery_clips(url, iconimage)
elif mode==533:
	xbmc.log("Other Clips")
	other_shows(url, iconimage)
elif mode==534:
	xbmc.log("Get TLC Clips")
	tlc_clips(url, iconimage)
elif mode==535:
	xbmc.log("Get DSC Kids")
	dsc_kids(url)
elif mode==536:
	xbmc.log("Get Kids Clips")
	kids_clips(url, iconimage)
elif mode==537:
	xbmc.log("Get Kids Stream")
	kids_stream(name,url)
elif mode==550:
	xbmc.log("Get Clips")
	get_clips(name,url)
elif mode == 99:
	xbmc.log("PLAY Video")
	PLAY(name,url)
elif mode==998:
	xbmc.log("Get JSON")
	dsc_json(name,url)
elif mode==999:
	xbmc.log("Play Video")
	play(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
