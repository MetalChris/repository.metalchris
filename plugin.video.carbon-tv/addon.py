#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later
# 2018.12.01

import urllib, urllib2, xbmcplugin, xbmcaddon, xbmcgui, htmllib, re, sys, os
from urllib import urlopen
from bs4 import BeautifulSoup
import html5lib
import cookielib
import requests, pickle
import json

artbase = 'special://home/addons/plugin.video.carbon-tv/resources/media/'
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
addon_path_profile = xbmc.translatePath(_addon.getAddonInfo('profile'))
selfAddon = xbmcaddon.Addon(id='plugin.video.carbon-tv')
self = xbmcaddon.Addon(id='plugin.video.carbon-tv')
translation = selfAddon.getLocalizedString
usexbmc = selfAddon.getSetting('watchinxbmc')
settings = xbmcaddon.Addon(id="plugin.video.carbon-tv")
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
xbmc_monitor = xbmc.Monitor()
__resource__   = xbmc.translatePath( os.path.join( _addon_path, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

from uas import *

plugin = "CarbonTV"

defaultimage = 'special://home/addons/plugin.video.carbon-tv/resources/media/icon.png'
defaultfanart = 'special://home/addons/plugin.video.carbon-tv/resources/media/fanart.jpg'
defaulticon = 'special://home/addons/plugin.video.carbon-tv/resources/media/icon.png'

local_string = xbmcaddon.Addon(id='plugin.video.carbon-tv').getLocalizedString
addon_handle = int(sys.argv[1])
download = settings.getSetting(id="download")
username = settings.getSetting(id="username")
password = settings.getSetting(id="password")
log_notice = settings.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

login_url = 'https://www.carbontv.com/users/login'
shows_url = 'https://www.carbontv.com/shows'

s = requests.Session()
headers = {'User-Agent': ua, 'origin': 'https://www.carbontv.com'
}

xbmc.log('CarbonTV Version: 2018.12.01',level=log_level)

#5
def login(shows_url):
	r = s.get('https://www.carbontv.com', headers=headers)
	xbmc.log('RESPONSE_CODE: ' + str(r.status_code),level=log_level)
	#xbmc.log(str(r.text.encode('utf-8')[:7500]),level=log_level)
	#xbmc.log('SESSION_COOKIES: ' + str((s.cookies.get_dict())),level=log_level)
	cookie_file = os.path.join(addon_path_profile, 'cookies.txt')
	with open(cookie_file, 'wb') as f:
		pickle.dump(s.cookies.get_dict(), f)
	csrfToken = re.compile("csrfToken': '(.+?)'").findall(str((s.cookies.get_dict())))[0]
	payload = {
		'_method': 'POST',
		'_csrfToken': csrfToken,
		'email' : username,
		'password' : password,
		'remember_me' : '0'
		}
	p = s.post('https://www.carbontv.com/users/login', data=payload, cookies=s.cookies.get_dict(), headers=headers)
	xbmc.log('RESPONSE_CODE: ' + str(r.status_code),level=log_level)
	r = s.get('https://www.carbontv.com', cookies=s.cookies.get_dict())
	xbmc.log('RESPONSE_CODE: ' + str(r.status_code),level=log_level)
	#xbmc.log(str(r.text.encode('utf-8')[:10000]),level=log_level)
	if 'Signup/Login' in str(r.text.encode('utf-8')):
	    xbmcgui.Dialog().notification(plugin, 'Login Failed', defaultimage, 5000, False)
	else:
		xbmcgui.Dialog().notification(plugin, 'Login Successful', defaultimage, 2500, False)
		cats(shows_url)


#10
def cats(url):
	r = s.get(shows_url, cookies=s.cookies.get_dict())
	html = r.text.encode('utf-8')
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'id':'navbar-item-login-signup'})
	#xbmc.log('SOUP: ' + str(soup),level=log_level)
	#check = soup[0].find('span').text.strip()
	#xbmc.log('CHECK: ' + str(check),level=log_level)
	#if 'Signup/Login' in str(soup):
		#xbmc.log('STATUS: ' + 'Logged Out',level=log_level)
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'menu'})
	for item in soup:
		title = item.get('data-menu-name')
		if title == 'All' or title == 'Sort':
			continue
		key = item.get('data-menu-id')
		url = 'https://www.carbontv.com/shows/more?type=channel&id=' + str(key) + '&sort=asc&limit=100&offset=0'
		if key == '9' or  key == '10':
			url = url.replace('channel','network')
		if 'cams' in url:
			continue
		add_directory2(title,url,15,defaultfanart,defaultimage,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#15
def shows(url):
	r = s.get(url, cookies=s.cookies.get_dict())
	html = r.text.encode('utf-8')
	soup = BeautifulSoup(html,'html5lib').find_all('div',{'class':'show'})
	for item in soup:
		title = item.find('div',{'class':'show-name truncate'}).string.encode('utf-8').strip()
		image = item.find('img',{'class':'show-thumb'})['src']
		url = 'http://www.carbontv.com' + item.find('a')['href']
		add_directory2(title,url,20,defaultfanart,image,plot='')
	xbmcplugin.endOfDirectory(addon_handle)


#20
def seasons(url):
	r = s.get(url, cookies=s.cookies.get_dict())
	response = r.text.encode('utf-8')
	url = url.split('?')[0]
	season_number = BeautifulSoup(response,'html5lib')
	if season_number.find('span',{'class':'season-number'}):
		xbmc.log('FOUND', level=log_level)
		soup = BeautifulSoup(response,'html5lib').find_all('div',{'tabindex':'0'})
		seasons = BeautifulSoup(str(soup),'html5lib').find_all('li')
		for season in seasons:
			season = season.text
			title = 'Season ' + season
			xbmc.log('SEASON: ' + str(season),level=log_level)
			surl = url + 'seasons/' + season + '/episodes/?limit=100&offset=0'
			xbmc.log('URL: ' + str(surl),level=log_level)
			add_directory2(title,surl,25,defaultfanart,defaultimage,plot='')
	else:
		xbmc.log('EPISODES ONLY', level=log_level)
		surl = url + 'episodes/?limit=100&offset=0'
		xbmc.log('URL: ' + str(surl),level=log_level)
		videos(surl)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#25
def videos(url):
	r = s.get(url, cookies=s.cookies.get_dict())
	response = r.text.encode('utf-8')
	jsob = re.compile('"content">\n(.+?)</').findall(response)[0]
	data = json.loads(str(jsob))
	total = (data['currentCount']); titles = []
	xbmc.log('TOTAL: ' + str(total),level=log_level)
	for i in range(total):
		title = (data['items'][i]['name']).encode('utf-8')
		if title in titles:
			continue
		titles.append(title)
		dtitle = re.sub('[^0-9a-zA-Z]+', '_', title)
		embed_code = data['items'][i]['embed_code']
		downloadUrl = 'http://cdnapi.kaltura.com/p/1897241/sp/189724100/playManifest/entryId/' + embed_code + '/format/download/protocol/http/flavorParamIds/0'
		url = 'http://www.carbontv.com' + data['items'][i]['path']
		duration = data['items'][i]['duration']
		runtime = (duration/1000)
		thumbnail = data['items'][i]['preview_image_url']
		season = data['items'][i]['season_number']
		episode = data['items'][i]['video_number']
		purl = 'plugin://plugin.video.carbon-tv?mode=30&url=' + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(title) + "&iconimage=" + urllib.quote_plus(thumbnail)
		li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
		li.addStreamInfo('video', { 'duration': runtime })
		li.setProperty('fanart_image', defaultfanart)
		li.setProperty('mimetype', 'video/mp4')
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type="video", infoLabels={ 'Title': title, 'Plot': '', 'season': season, 'episode': episode })
		li.addContextMenuItems([('Download File', 'XBMC.RunPlugin(%s?mode=80&url=%s&name=%s)' % (sys.argv[0], downloadUrl,dtitle))])
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=purl, listitem=li, isFolder=False)
		xbmcplugin.setContent(addon_handle, 'episodes')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_EPISODE)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)


#30
def streams(name,url,iconimage):
	r = s.get(url, cookies=s.cookies.get_dict())
	html = r.text.encode('utf-8')
	soup = BeautifulSoup(html,'html5lib')
	link = soup.find("meta",  property="og:video:url")['content']
	xbmc.log('LINK: ' + str(link),level=log_level)
	key = link.split('=')[-1]
	xbmc.log('KEY: ' + str(key),level=log_level)
	r = s.get(link, cookies=s.cookies.get_dict())
	response = r.text.encode('utf-8')
	response = get_html(link)
	jsob = re.compile('window.kalturaIframePackageData =(.+?);\n').findall(response)[0]
	data = json.loads(str(jsob))
	item_dict = json.loads(str(jsob))
	dataUrl = ((data['entryResult']['meta']['dataUrl']).split('format')[0])
	xbmc.log('DATAURL: ' + str(dataUrl),level=log_level)
	flavorParamsIds = data['entryResult']['meta']['flavorParamsIds']
	xbmc.log('FLAVORID: ' + str(flavorParamsIds),level=log_level)
	stream = dataUrl + 'flavorIds/' + flavorParamsIds + '/format/applehttp/protocol/https/a.m3u8'
	xbmc.log('STREAM: ' + str(stream),level=log_level)
	listitem = xbmcgui.ListItem(name, path=stream, thumbnailImage=iconimage)
	listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


#80
def downloader(url,name):
	path = addon.getSetting('download')
	if path == "":
		xbmc.executebuiltin("XBMC.Notification(%s,%s,10000,%s)"
				%(translation(30001), translation(30010), defaulticon))
		addon.openSettings(label="Download")
		path = addon.getSetting('download')
	if path == "":
		return
	file_name = name + '.mp4'
	dlsn = settings.getSetting(id="status")
	bsize = settings.getSetting(id="bsize")
	try: u = urllib2.urlopen(url)
	except urllib2.HTTPError:
		xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)"
				%(translation(30000), translation(30015), defaulticon))
		return
	meta = u.info()
	file_size = float(meta.getheaders("Content-Length")[0])
	file_sizeMB = float(file_size/(1024*1024))
	ret = xbmcgui.Dialog().yesno('Download Selected File?', str(file_name), '', str("%.2f" % file_sizeMB) + ' MB')
	if ret == False:
		return videos
	else:
		xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)"
				%(translation(30000), translation(30014), defaulticon))
	xbmc.log('URL: ' + str(url),level=log_level)
	xbmc.log('Filename: ' + str(file_name),level=log_level)
	xbmc.log('Download Location: ' + str(download),level=log_level)
	f = open(download+file_name, 'wb')
	xbmc.log("Downloading: %s %s MB" % (file_name, "%.2f" % file_sizeMB),level=log_level)
	file_size_dl = 0
	block_sz = int(bsize)
	progress = xbmcgui.DialogProgress()
	if dlsn!='false':
		progress.create('CarbonTV')
	while True:
		bfr = u.read(block_sz)
		if not bfr:
			break
		file_size_dl += float(len(bfr))
		file_size_dlMB = float(file_size_dl/(1024*1024))
		status = float(file_size_dl * 100. / file_size)
		message = "%.2f  [%3.2f%%]" % (file_size_dlMB, file_size_dl * 100. / file_size)
		message = message + chr(8)*(len(message)+1)
		if dlsn!='false':
			progress.update(int(status),'Download in Progress...','',str(file_size_dlMB) + ' MB of ' + ("%.2f" % float(file_sizeMB)) + ' MB')
		xbmc.sleep(500)
		f.write(bfr)
		if dlsn!='false':
			if progress.iscanceled():
				os.remove(download+file_name)
				return
	f.close()
	if dlsn!='false':
		progress.close()
	xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)"
			%(translation(30000), translation(30016), defaulticon))
	xbmc.log('Download Completed',level=log_level)


def get_sec(time_str):
	try: h, m, s = time_str.split(':')
	except ValueError:
		m, s = time_str.split(':')
		return int(m) * 60 + int(s)
	return int(h) * 3600 + int(m) * 60 + int(s)


def striphtml(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)


def add_directory2(name,url,mode,fanart,thumbnail,plot):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) + "&thumbnail=" + urllib.quote_plus(thumbnail)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	liz.setInfo( type="Video", infoLabels={ "Title": name,
												"plot": plot} )
	if not fanart:
		fanart=''
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=40)
	return ok


def get_html(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0')

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

xbmc.log("Mode: " + str(mode),level=log_level)
xbmc.log("URL: " + str(url),level=log_level)
xbmc.log("Name: " + str(name),level=log_level)

if mode == None or url == None or len(url) < 1:
	xbmc.log("Generate Main Menu",level=log_level)
	cats(url)
elif mode == 4:
	xbmc.log("Play Video",level=log_level)
elif mode==10:
	xbmc.log('CarbonTV Categories',level=log_level)
	cats(url)
elif mode==15:
	xbmc.log('CarbonTV Shows',level=log_level)
	shows(url)
elif mode==20:
	xbmc.log("CarbonTV Seasons",level=log_level)
	seasons(url)
elif mode==25:
	xbmc.log("CarbonTV Videos",level=log_level)
	videos(url)
elif mode==30:
	xbmc.log("CarbonTV Streams",level=log_level)
	streams(name,url,iconimage)
elif mode == 80:
	xbmc.log("CarbonTV Download File",level=log_level)
	downloader(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
