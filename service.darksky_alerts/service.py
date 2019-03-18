#!/usr/bin/python
#
#
# Written by MetalChris
# Released under GPL(v2) or Later

#Version 2019.03.18

import urllib2, xbmcaddon, xbmcgui, re, os, sys, json

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')
_addonname  = _addon.getAddonInfo('name')
_addonid    = _addon.getAddonInfo('id')
_version    = _addon.getAddonInfo('version')
_cwd       = _addon.getAddonInfo('path').decode("utf-8")
_resource   = xbmc.translatePath( os.path.join( _cwd, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
settings = xbmcaddon.Addon(id="service.darksky_alerts")
darksky_settings = xbmcaddon.Addon(id='weather.darksky')
darksky_api = darksky_settings.getSetting(id="API_KEY")
alert_textbox = _addon.getSetting(id="alert_textbox")
alert_notification = _addon.getSetting(id="alert_notification")
alert_dialog = _addon.getSetting(id="alert_dialog")
alert_sound = _addon.getSetting(id="alert_sound")
log_notice = settings.getSetting(id="log_notice")
local_string = xbmcaddon.Addon(id='service.darksky_alerts').getLocalizedString
window_id = xbmcgui.getCurrentWindowId()

defaultimage = 'special://home/addons/service.darksky_alerts/icon.png'
defaulticon = 'special://home/addons/service.darksky_alerts/icon.png'
ip_url = 'https://ifconfig.me'

if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

if darksky_api != '':
	xbmc.log('DARKSKY API KEY FOUND',level=log_level)
else:
	xbmcgui.Dialog().notification('DarkSky Weather Alerts', 'DarkSky API Key Not Found', defaultimage, 5000, False)
	sys.exit()

xbmc.log('DarkSky Alerts Version %s Started: %s' % (_version, sys.argv),level=log_level)

local_string = xbmcaddon.Addon(id='service.darksky_alerts').getLocalizedString
window_id = xbmcgui.getCurrentWindowId()


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

monitor = xbmc.Monitor()

while not monitor.abortRequested():
	if monitor.waitForAbort(1800):
		xbmc.log('Abort Requested - Shutting Down DarkSky Alerts', level=xbmc.LOGNOTICE)
		break
	html = get_html(ip_url)
	ip = re.compile('ip_address">(.+?)</').findall(html)[0]
	response = get_html('https://ipinfo.io/' + ip + '/json')
	data = json.loads(response)
	coords = data['loc']
	#uncomment the line below and insert coordinates where there is an active alert to test
	#coords = '41.259998,-95.940002'
	xbmc.log('COORDS: ' + str(coords),level=log_level)
	alert_url = 'https://api.darksky.net/forecast/' + darksky_api + '/' + coords
	response = get_html(alert_url)
	forecast = json.loads(response)
	if 'alerts' not in forecast:
		xbmc.log('NO ALERTS',level=log_level)
	else:
		xbmc.log('ALERTS',level=log_level)
		alert_txt = str(forecast['alerts'][0]['description'])
		#if xbmc.Player().isPlaying():
			#xbmc.Player().pause()
		if alert_sound != 'false':
			xbmc.playSFX('special://home/addons/service.darksky_alerts/resources/alert.wav')
		if alert_dialog != 'false':
			xbmcgui.Dialog().ok('DarkSky Weather Alert', alert_txt)
		if alert_textbox != 'false':
			xbmcgui.Dialog().textviewer('DarkSky Weather Alert', alert_txt)
		if alert_notification != 'false':
			xbmcgui.Dialog().notification('DarkSky Weather Alert', alert_txt, defaultimage, 30000, False)
		if monitor.waitForAbort(1800):
			xbmc.log('Abort Requested - Shutting Down DarkSky Alerts', level=xbmc.LOGNOTICE)
			break
