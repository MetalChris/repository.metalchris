#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import simplejson as json
import requests
#from urllib2 import Request, HTTPCookieProcessor
import urlparse
import httplib
import html5lib

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
}


_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.nhl-rewind')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
#settings = xbmcaddon.Addon(id="plugin.video.nhl-rewind")
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
#QUALITY = settings.getSetting(id="quality")
confluence_views = [500,501,502,503,504,508]


def CATEGORIES():
	addDir('NHL.tv', 'https://www.nhl.com/video/', 16, defaultimage)
	addDir('FOX Sports', 'http://www.foxsports.com/nhl/video', 51, defaultimage)
	addDir('NBC Sports', 'http://www.nbcsports.com/video/league/nhl', 89, defaultimage)
	addDir('MSG Network', 'http://www.msgnetworks.com/teams/rangers.html', 80, defaultimage)
	addDir('SportsNet.ca', 'http://www.sportsnet.ca/videos/leagues/nhl-video/', 20, defaultimage)
	addDir('ESPN', 'http://espn.go.com/video/format/libraryPlaylist?categoryid=2459791', 90, defaultimage)
	addDir('Comcast SportsNet', 'http://www.comcastsportsnet.com/', 95, defaultimage)
	addDir('All Teams', 'https://www.nhl.com/info/teams', 30, defaultimage)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#30
def teams(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	for item in soup.find_all(attrs={'class': 'ticket-team_name h3'}):
		city = item.find('span',{'class':'team-city'}).text.encode('utf-8')
		team = item.find('span',{'class':'team-name'}).text.encode('utf-8')
		title = city + ' ' + team
		url = 'http://www.nhl.com/' + team.lower() + '/video'
		add_directory2(title, url, 31, defaultfanart, defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#31
def team_sub(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	for item in soup.find_all(attrs={'class': 'section-banner__tray-item'}):
		title = item.find('a').text.encode('utf-8')
		url = 'http://www.nhl.com' + item.find('a')['href']
		add_directory2(title, url, 32, defaultfanart, defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#32
def team_sub2(url):
	html = get_html(url)
	keys = re.compile('data-asset-id="(.+?)"').findall(str(html))
	for key in keys:
		url = 'http://nhl.bamcontent.com/nhl/id/v1/' + key + '/details/web-v1.json'
		response = urllib2.urlopen(url)
		nhldata = json.load(response)
		title = str(nhldata["title"])
		add_directory3(title, url, 12, defaultfanart, defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def fox_sports2(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	for title in soup.find_all(attrs={'class': 'media-grid-link'}):
		url = (re.compile('href="(.+?)"').findall(str(title))[0])
		image = (re.compile('src="(.+?)"').findall(str(title))[0]).replace('480.270','960.540')
		title = title.find('h3').text.encode('utf-8')
		add_directory3(title, url, 52, image, image, plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#52
def get_fox_page(name,url):
	html = get_html(url)
	redirect = re.compile('video_url": "(.+?)"').findall(str(html))[0]
	url = resolve_http_redirect(redirect)
	xbmc.log('FOX URL: ' + str(url))
	play_url(name,url)
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#89
def nbcsn_nhl(url):
	html = get_html(url)
	titles = re.compile('\\{"title":"(.+?)"').findall(str(html))
	keys = re.compile('pid":"(.+?)"').findall(str(html))
	for title, key in zip(titles, keys):
		title = title.replace("\u0027", "'")
		smil = 'http://link.theplatform.com/s/BxmELC/media/' + str(key)
		add_directory3(title, smil, 91, defaultfanart, defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#91
def nbcsn_smil(name,url):
	html = get_html(url)
	link = (re.compile('\\n(.+?)\\?').findall(str(html))[0]).split('index')[0] + 'master.m3u8'
	listItem = xbmcgui.ListItem(path=str(link))
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#80
def msg_cat():
	addDir('MSG: Rangers', 'http://www.msgnetworks.com/teams/rangers/', 84, artbase + 'msgnyr.jpg')
	addDir('MSG: Islanders', 'http://www.msgnetworks.com/teams/islanders/', 84, artbase + 'msg.jpg')
	addDir('MSG: Sabres', 'http://www.msgnetworks.com/teams/sabres/', 84, artbase + 'msg.jpg')
	addDir('MSG: Devils', 'http://www.msgnetworks.com/teams/devils/', 84, artbase + 'msgnjd.jpg')


#84
def msg_network(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser').find_all('article',{'class':'video-post'})
	nxt = BeautifulSoup(html,'html.parser').find_all('div',{'class':'load-more'})
	for link in nxt:
		next_page = link.find('a')['href']
	for item in soup:
		title = item.find('h2').text.encode('utf-8').strip()
		url = item.find('a',{'class':'title_link'})['href'] + 'embed/?'
		image = str(re.compile("url\\(\\'(.+?)\\'\\)").findall(str(item)))[2:-2]
		add_directory3(title, url, 85, image, image, plot='')
		addDir('Next Page', next_page, 86, image)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#85
def msg_smil(name,url):
	html = get_html(url)
	videoId = re.compile('data-video-id="(.+?)"').findall(html)[0]
	pubId = re.compile('data-account="(.+?)"').findall(html)[0]
	url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + videoId + '&pubId=' + pubId
	listItem = xbmcgui.ListItem(path=str(url), thumbnailImage=defaulticon)
	listItem.setInfo('video', name)
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#86
def msg_pages(url):
	page = int(url.split('=')[-1])
	next_page = (url.split('='))[0] + '=' + str(page +1)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4')
	response = urllib2.urlopen(req, timeout=60)
	html = response.read()
	response.close()
	soup = BeautifulSoup(html,'html.parser').find_all('article',{'class':'video-post'})
	for item in soup:
		title = item.find('h2').text.encode('utf-8').strip()
		url = item.find('a',{'class':'title_link'})['href'] + 'embed/?'
		image = str(re.compile("url\\(\\'(.+?)\\'\\)").findall(str(item)))[2:-2]
		add_directory3(title, url, 85, image, image, plot='')
		addDir('Next Page', next_page, 86, image)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)




# Recursively follow redirects until there isn't a location header
def resolve_http_redirect(url, depth=0):
	if depth > 10:
		raise Exception("Redirected "+depth+" times, giving up.")
	o = urlparse.urlparse(url,allow_fragments=True)
	conn = httplib.HTTPConnection(o.netloc)
	path = o.path
	if o.query:
		path +='?'+o.query
	conn.request('HEAD', path, headers={"User-Agent": "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; .NET CLR 1.1.4322)"})
	res = conn.getresponse()
	headers = dict(res.getheaders())
	if headers.has_key('location') and headers['location'] != url:
		return resolve_http_redirect(headers['location'], depth+1)
	else:
		return url


def play_url(name,url):
	listitem =xbmcgui.ListItem (name,thumbnailImage=defaultimage)
	print 'URL= ' + str(url)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#16
def nhl_all(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html.parser')
	for item in soup.find_all(attrs={'class': 'section-banner__tray-item'}):#[37:54]:
		link = item.find('a')['href']
		if len(link) < 1:
			continue
		title = item.find('a').text.encode('utf-8')
		key = ((item.find('a')['href']).split('-'))[-1]
		url = 'https://search-api.svc.nhl.com/svc/search/v2/nhl_global_en/topic/' + key + '?page=1&sort=new&type=video&hl=true&expand=image.cuts.640x360%2Cimage.cuts.1136x640'
		add_directory2(title,url,11, defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#11
def nhl_video(url):
	nextlink = (url.split('?'))[0]
	page = (url.split('=')[1])
	page = int(page.split('&')[0]) + 1
	response = urllib2.urlopen(url)
	nhldata = json.load(response);i=0
	for video in nhldata["docs"]:
		title = str(nhldata["docs"][i]["title"])
		asset_id = str(nhldata["docs"][i]["asset_id"])
		url = 'http://nhl.bamcontent.com/nhl/id/v1/' + asset_id +'/details/web-v1.json'
		image = (nhldata["docs"][i]["image"]["cuts"]["1136x640"]["src"])
		i = i + 1
		add_directory3(title,url,12, image ,image,plot='')
	nextpage = nextlink + '?page=' + str(page)# + '/new/video///false/'
	add_directory2('Next 10 Videos', nextpage, 11, defaultfanart, defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#12
def nhl_stream(name,url):
	response = urllib2.urlopen(url)
	vid_data = json.load(response)
	url = (vid_data["playbacks"][4]["url"])#.replace('master_wired60.m3u8','asset_5600k.m3u8')
	listItem = xbmcgui.ListItem(path=str(url))
	#listItem.setInfo('video', name)
	xbmcplugin.setResolvedUrl(addon_handle, True, listItem)
	return


#90
def espn_nhl(url):
	html = get_html(url)
	match=re.compile('<img src="(.+?)" width="134" height="75" /></a><h5>(.+?)</h5>').findall(html)
	for image,title in match:
		video = image.replace('a.espncdn.com/media', 'media.video-cdn.espn.com')
		video = video.replace('.jpg', '_nolbr.m3u8')
		li = xbmcgui.ListItem(title, iconImage= image, thumbnailImage= image)
		li.setProperty('fanart_image',  defaultfanart)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=video, listitem=li, totalItems=10)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[1])+")")


#20
def sportsnet(url):
	response = urllib2.urlopen(url)
	soup = BeautifulSoup(response,'html5lib').find_all('div',{'id':'video_strip_group_container'})
	videoIds = re.compile('bc_video_id":(.+?),').findall(str(soup))
	titles = re.compile('video_title":"(.+?)",').findall(str(soup))
	for title, videoId in zip(titles, videoIds):
		title = remove_crap(title)
		url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + videoId
		li = xbmcgui.ListItem(title, iconImage= defaultimage, thumbnailImage= defaultimage)
		li.setProperty('fanart_image',  defaultfanart)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, totalItems=10)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


def remove_crap(data):
	data = data.replace("&colon;",":").replace("&rsquo;","'").replace("&quest;","?").replace("&apos;","'").replace("&comma;",",").replace("&excl;","!").replace("&amp;","&").replace("&period;",".")
	return data


def csn_cat(url):
	addDir('Bay Area', 'http://www.csnbayarea.com/sharks', 97, defaultimage)
	addDir('Chicago', 'http://www.csnchicago.com/blackhawks', 97, defaultimage)
	addDir('Mid-Atlantic', 'http://www.csnmidatlantic.com/washington-capitals', 97, defaultimage)
	addDir('New England', 'http://www.csnne.com/boston-bruins', 97, defaultimage)
	addDir('Philadelphia', 'http://www.csnphilly.com/philadelphia-flyers', 97, defaultimage)


#97
def csn_phi(url):
	r = requests.get(url)
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', r.cookies))
	f = opener.open(url)
	page = f.read()
	soup = BeautifulSoup(page,'html5lib')
	for item in soup.find_all(attrs={'class': 'vod-content__event'}):
		title = item.find('span', {'class':'media-thumb__title'}).text.encode('utf-8')
		url = item.find('a')['href']
		##image = defaultimage
		addDir(title, url, 98,defaultimage)
		xbmcplugin.setContent(pluginhandle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#98
def csn_video(name,url):
	r = requests.get(url)
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', r.cookies))
	f = opener.open(url)
	page = f.read()
	soup = BeautifulSoup(page,'html5lib')
	url = (soup.find('meta', attrs={'name':'twitter:player:stream'})['content'])
	url = resolve_http_redirect(url)
	url = url.replace('WEBLOWVIDEO','WEBBESTVIDEO3').replace('WEBBESTVIDEO2','WEBBESTVIDEO3').replace('300k','2200k')
	play_url(name,url)
	sys.exit()


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
elif mode == 16:
	print "Get All NHL Video"
	nhl_all(url)
elif mode == 20:
	print "Get SN Categories"
	sportsnet(url)
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
elif mode == 30:
	print "Get NHL Teams"
	teams(url)
elif mode == 31:
	print "Get NHL Team SubMenu"
	team_sub(url)
elif mode == 32:
	print "Get NHL Team SubMenu2"
	team_sub2(url)
elif mode == 51:
	print "Get Fox Sports NHL Videos"
	fox_sports2(url)
elif mode == 52:
	print "Get Fox Page"
	get_fox_page(name,url)
elif mode == 80:
	print "Get MSG Teams"
	msg_cat()
elif mode == 84:
	print "Get MSG Network"
	msg_network(url)
elif mode == 85:
	print "Get MSG SMIL"
	msg_smil(name,url)
elif mode == 86:
	print "Get MSG Pages"
	msg_pages(url)
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
	print "Get CSN Philly Video"
	csn_phi(url)
elif mode == 98:
	print "Get CSN Video"
	csn_video(name,url)
elif mode==100:
	print "PlayURL"
	play_url(name,url)
elif mode==101:
	print "Get Cookies"
	get_cookies(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


