#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys
from bs4 import BeautifulSoup
import html5lib
import simplejson as json
import datetime
from pytz import timezone
from requests import Session

artbase = 'special://home/addons/plugin.video.hunt-channel/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
selfAddon = xbmcaddon.Addon(id='plugin.video.hunt-channel')
self = xbmcaddon.Addon(id='plugin.video.hunt-channel')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
confluence_views = [500,501,502,503,504,508]

plugin = "Hunt Channel"

defaultimage = 'special://home/addons/plugin.video.hunt-channel/icon.png'
defaultfanart = 'special://home/addons/plugin.video.hunt-channel/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.hunt-channel/icon.png'
baseurl = 'http://www.huntchannel.tv'
schedule = 'special://home/addons/plugin.video.hunt-channel/resources/media/schedule.json'

local_string = xbmcaddon.Addon(id='plugin.video.hunt-channel').getLocalizedString
addon_handle = int(sys.argv[1])
confluence_views = [500,501,502,503,504,508,515]

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:51.0) Gecko/20100101 Firefox/51.0',
	'Referer': 'http://www.huntchannel.tv/shows/'
}

now = datetime.datetime.now(timezone('US/Eastern'))
now_minus_30 = now + datetime.timedelta(minutes = -30)
if now.hour >12:
	hour = now.hour - 12
elif now.hour < 1:
	hour = '12'
else:
	hour = now.hour
if now.minute < 29:
	minute = '00'
else:
	minute = '30'
showday = now.strftime("%A")
#xbmc.log(str(showday))
today = int(now.strftime("%w"))
if today <1:
	today = 7
#xbmc.log(str(today))
nowstring = str(hour) + ':' + minute + ' ' + now.strftime("%p")
#xbmc.log(str(nowstring))
program = 'No Info Currently Available'


def prog():
	html = get_html('http://www.huntchannel.tv/schedule')
	rows = BeautifulSoup(html,'html5lib').find_all('tr')
	match = 0
	for row in rows[1:45]:
		row_split = (str(row)).split('</td>')
		row_list = striphtml(str(row_split)).replace('\'','').replace('[','').replace(']','').split(',')
		if nowstring == row_list[0]:
			match = 1
			xbmc.log('==========================MATCH')
			program = str(row_list[today]).replace("\\","'")
			#xbmc.log(str(program))
			#xbmc.log(str(row_list))
			break

		elif match <1:
			program = 'No Info Currently Available'
	#xbmc.log(str(match))
	cats(program)


#10
def cats(program):
	addDir2('Live Stream' + ': ' + program,'http://www.huntchannel.tv/live/',12,defaultimage)
	addDir('On Demand','http://www.huntchannel.tv',11,defaultimage)
	xbmcplugin.endOfDirectory(addon_handle)


#11
def vod(url):
	addDir('Featured','http://www.huntchannel.tv',13,defaulticon)
	#addDir('Recently Added','http://huntchannel.tv/feed/',14,defaulticon)
	addDir('All Shows','http://www.huntchannel.tv/wp-admin/admin-ajax.php',100,defaulticon)
	xbmcplugin.endOfDirectory(addon_handle)


#12
def get_live(name,url,iconimage):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'id':'player-embed'})
	iframe = str(re.compile('src="(.+?)"').findall(str(soup)))[2:-2].replace('html','js')
	if 'http' not in iframe:
		iframe = 'http' + iframe
	xbmc.log('IFRAME: ' + str(iframe))
	html = get_html(iframe)
	m3u8 = str(re.compile('file": "(.+?)"').findall(str(html)))[2:-2]#[0])
	listitem = xbmcgui.ListItem('Hunt Channel' + ' ' + name, thumbnailImage=defaulticon)
	listitem.setProperty('mimetype', 'video/x-mpegurl')
	xbmc.Player().play( m3u8, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#13
def get_vod(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'scroll-text'})
	titles = re.compile('<li>(.+?)</li>').findall(str(soup))
	for title in titles:
		url = str(re.compile('href=(.+?)>').findall(str(title)))[3:-3]
		title = striphtml(title).replace('&amp;','&')
		add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#14
def recent(url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('item')
	for item in soup:
		title = item.find('title').string.encode('utf-8').title()
		url = item.find('comments').string.split('#')[0]
		add_directory2(title,url,30,defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#21
def sc_videos(name,url):
	html = get_html(url)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'entry-content'})
	for item in reversed(soup):
		title = (item.find('a')['title']).encode('utf-8').strip()
		if item.find('img'):
			image = item.find('img')['src']
		else:
			continue
		url = item.find('a')['href']
		add_directory2(title,url,31,defaultfanart,image,plot='')
	xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.endOfDirectory(addon_handle)


#30
def hstreams(name,url):
	response = get_html(url)
	soup = BeautifulSoup(response,'html5lib').find_all('iframe')[0]
	iframe = re.compile('src="(.+?)"').findall(str(soup))[0]
	source = get_iframe(iframe)
	#thumbnail = re.compile('base":"(.+?)"').findall(str(source))[-1]
	best(source)


#31
def s_streams(name,url):
	response = get_html(url)
	#xbmc.log(str(url))
	vsoup = BeautifulSoup(response,'html5lib').find_all('input',{'name':'main_video_url'})
	vkey = str(re.compile('value="(.+?)"').findall(str(vsoup)))[2:-2]
	vurl = 'https://player.vimeo.com/video/' + vkey
	#xbmc.log('VURL: ' + str(vurl))
	source = get_iframe(vurl)
	best(source)


def best(data):
	vjson = re.compile('progressive":(.+?)},"lang').findall(str(data))
	mp4 = (re.compile('"url":"(.+?)"').findall(str(vjson)));i = 0
	#xbmc.log('MP4: ' + str(len(mp4)))
	if len(mp4) < 1:
		xbmcgui.Dialog().notification(name, 'No Stream Available', defaultimage, 5000, False)
		sys.exit()
	data = json.loads(vjson[0])
	elements = [];links = []
	for stream in data:
		stream = data[i]['url']
		#xbmc.log('STREAM: ' + str(stream))
		quality = data[i]['quality'];i = i + 1
		#xbmc.log('QUALITY: ' + str(quality))
		elements.append(quality)
		links.append(stream)
	hi = max(elements)
	i = elements.index(hi)
	#ret = xbmcgui.Dialog().select('Select Quality',elements)
	#xbmc.log(str(ret))
	stream = links[i]
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( stream, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


#100
def more(url):
	for i in range(0,3):
		data = {'action':'load_more','page':i,'template':'cactus-channel/content-listing','vars[post_type]':'ct_channel','vars[orderby]':'title','vars[order]':'ASC'}
		session = Session()
		session.head('http://www.huntchannel.tv')
		response = session.post(
		url ='http://www.huntchannel.tv/wp-admin/admin-ajax.php',
		data=data,
		headers=headers)
		soup = BeautifulSoup(response.text,'html5lib').find_all('div',{'class':'entry-content'})
		for item in soup:
			title = (item.find('a')['title']).encode('utf-8').strip()
			if item.find('img'):
				image = item.find('img')['src']
			else:
				image = defaultimage
			url = item.find('a')['href']
			add_directory2(title,url,21,defaultfanart,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)



def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def play(name,url,iconimage):
	xbmc.log(str(url))
	listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def hplay(name,url,iconimage):
	xbmc.log(str(url))
	listitem = xbmcgui.ListItem(name, thumbnailImage=defaultimage)
	xbmc.Player().play( url, listitem )
	sys.exit()
	xbmcplugin.endOfDirectory(addon_handle)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
		liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
		if not fanart:
			fanart=''
		liz.setProperty('fanart_image',fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=100)
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

def get_iframe(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'player.vimeo.com')
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')
	req.add_header('Referer', 'http://huntchannel.tv/')

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

def addDir(name, url, mode, iconimage, fanart=False, infoLabels=True):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	if not fanart:
		fanart=defaultfanart
	liz.setProperty('fanart_image',fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok


def addDir2(name,url,mode,iconimage, fanart=True, infoLabels=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		if not fanart:
			fanart=defaultfanart
		liz.setProperty('fanart_image',defaultfanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
	xbmc.log("Generate Main Menu")
	prog()
elif mode == 4:
	xbmc.log("Play Video")
elif mode==10:
	xbmc.log('Hunt Channel Categories')
	cats(program)
elif mode==11:
	xbmc.log('Hunt Channel VOD')
	vod(url)
elif mode==12:
	xbmc.log('Hunt Channel Live')
	get_live(name,url,iconimage)
elif mode==13:
	xbmc.log('Hunt Channel Featured')
	get_vod(url)
elif mode==14:
	xbmc.log('Hunt Channel Recent')
	recent(url)
elif mode==30:
	xbmc.log("Hunt Channel Streams")
	hstreams(name,url)
elif mode==21:
	xbmc.log("Hunt Channel Videos")
	sc_videos(name,url)
elif mode==31:
	xbmc.log("Hunt Channel Streams")
	s_streams(name,url)
elif mode==40:
	xbmc.log("Hunt Channel Live")
	play(name,url,iconimage)
elif mode==50:
	xbmc.log("Hunt Channel Program")
	prog()
elif mode==100:
	xbmc.log("Hunt Channel Shows")
	more(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
