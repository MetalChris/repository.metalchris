# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html

# DarkSky Weather 12/25/2018

import os, sys, socket, urllib2
import xbmc, xbmcgui, xbmcaddon
import time
import json

# This is a throwaway variable to deal with a python bug
throwaway = time.strptime('20110101','%Y%m%d')

__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')
__version__    = __addon__.getAddonInfo('version')
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)

from utilities import *

log_notice = __addon__.getSetting(id="log_notice")
if log_notice != 'false':
	log_level = 2
else:
	log_level = 1
xbmc.log('LOG_NOTICE: ' + str(log_notice),level=log_level)

LOC_URL          = 'https://devru-latitude-longitude-find-v1.p.mashape.com/latlon.php?location=%s'
#LOC_QUERY        = 'http://maps.googleapis.com/maps/api/geocode/json?address="%s"'
API_URL          = 'https://api.darksky.net/forecast/'
#APP_ID		= __addon__.getSetting(id="APP_ID")
API_KEY	= __addon__.getSetting(id="API_KEY")
WEATHER_ICON     = xbmc.translatePath('special://temp/weather/%s.png').decode("utf-8")
WEATHER_WINDOW   = xbmcgui.Window(12600)
NOW = time.time()
LOCAL_TIME = time.localtime(NOW)
HOUR = time.strftime("%H", LOCAL_TIME)
TODAY = time.strftime("%A", LOCAL_TIME)

socket.setdefaulttimeout(10)

def log(txt):
	if isinstance (txt,str):
		txt = txt.decode("utf-8")
	message = u'%s: %s' % (__addonid__, txt)

def set_property(name, value):
	WEATHER_WINDOW.setProperty(name, value)

def refresh_locations():
	locations = 0
	for count in range(1, 4):
		loc_name = __addon__.getSetting('Location%s' % count)
		if loc_name != '':
			locations += 1
		set_property('Location%s' % count, loc_name)
	set_property('Locations', str(locations))
	xbmc.log('Available Locations: %s' % str(locations),level=log_level)

def location(loc):
	items  = []
	locs   = []
	locids = []
	query = find_location(loc)
	data = json.loads(query)
	total = len(data['Results'])
	if total == 0:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Kodi', 'No results found.')
		pass
	xbmc.log('TOTAL: ' + str(total),level=log_level)
	cities = []; lls = []
	for i in range(total):
		location = data['Results'][i]['name']
		lat = data['Results'][i]['lat']
		lng = data['Results'][i]['lon']
		locationid = str(lat) + ',' + str(lng)
		items.append(location)
		locs.append(location)
		locids.append(locationid)
	return items, locs, locids

def find_location(loc):
	query = urllib2.quote(loc)
	xbmc.log('QUERY: ' + str(query),level=log_level)
	url = LOC_URL % query
	req = urllib2.Request(url)
	req.add_header('User-Agent','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/50.0')
	req.add_header('X-Mashape-Key','Qy1sTKFh52mshmLUd5de5hAzIhscp1313exjsnkRPm7LeH25sf')
	req.add_header('X-Mashape-Host','devru-latitude-longitude-find-v1.p.mashape.com')

	try:
		response = urllib2.urlopen(req)
		html = response.read()
		response.close()
	except urllib2.HTTPError:
		response = False
		html = False
	return html

def parse_data(reply):
	try:
		data = json.loads(reply)
	except:
		xbmc.log('Failed to Parse Weather Data',level=log_level)
		data = ''
	return data

def forecast(loc,locid):
	xbmc.log('weather location: %s' % locid,level=log_level)
	retry = 0
	while (retry < 6) and (not xbmc.abortRequested):
		query = get_weather(locid)
		if query != '':
			retry = 6
		else:
			retry += 1
			xbmc.sleep(10000)
			xbmc.log('Weather Download Failed',level=log_level)
	#xbmc.log('forecast data: %s' % query,level=log_level)
	retry = 0
	while (retry < 6) and (not xbmc.abortRequested):
		fquery = get_forecast(locid)
		if fquery != '':
			retry = 6
		else:
			retry += 1
			xbmc.sleep(10000)
			xbmc.log('Forecast Download Failed',level=log_level)
	#xbmc.log('forecast data: %s' % fquery,level=log_level)
	if fquery != '':
		properties(query,fquery,loc,locid)
	else:
		clear()

def get_weather(locid):
	xbmc.log('GET WEATHER',level=log_level)
	url = API_URL + API_KEY + '/' + str(locid) + '?units=si'
	xbmc.log('GET WEATHER URL:' + str(url),level=log_level)
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')
		req.add_header('Accept','application/json')
		response = urllib2.urlopen(req)
		data = response.read()
		req.close()
	except:
		response = ''
	return data

def get_forecast(locid):
	xbmc.log('GET FORECAST',level=log_level)
	url = API_URL + API_KEY + '/' + str(locid) + '?units=si'
	xbmc.log('GET FORECAST URL:' + str(url),level=log_level)
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')
		req.add_header('Accept','application/json')
		response = urllib2.urlopen(req)
		fdata = response.read()
		#xbmc.log(str(fdata))
		req.close()
	except:
		xbmc.log('EXCEPTION!',level=log_level)
		response = ''
		#get_forecast(locid)
	return fdata

def degToCompass(num):
	val=int((int(num)/22.5)+.5)
	arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
	print arr[(val % 16)]
	winddir = arr[(val % 16)]
	return(winddir)

def clear():
	xbmc.log('CLEAR',level=log_level)
	set_property('Current.Condition'     , 'N/A')
	set_property('Current.Temperature'   , '0')
	set_property('Current.Wind'          , '0')
	set_property('Current.WindDirection' , 'N/A')
	set_property('Current.Humidity'      , '0')
	set_property('Current.FeelsLike'     , '0')
	set_property('Current.UVIndex'       , '0')
	set_property('Current.DewPoint'      , '0')
	set_property('Current.OutlookIcon'   , 'na.png')
	set_property('Current.FanartCode'    , 'na')
	for count in range (0, 6):
		set_property('Day%i.Title'       % count, 'N/A')
		set_property('Day%i.HighTemp'    % count, '0')
		set_property('Day%i.LowTemp'     % count, '0')
		set_property('Day%i.Outlook'     % count, 'N/A')
		set_property('Day%i.OutlookIcon' % count, 'na.png')
		set_property('Day%i.FanartCode'  % count, 'na')

def properties(data,fdata,loc,locid):
	xbmc.log('PROPERTIES',level=log_level)
	wdata = parse_data(data)
	weathercode = WEATHER_CODES[(wdata['currently']['icon'])]
	xbmc.log('LOC: ' + str(loc),level=log_level)
	xbmc.log('LOCATION: ' + str(location),level=log_level)
	xbmc.log('LOCATIONID: ' + str(locationid),level=log_level)
	set_property('Current.Location'      , loc)
	set_property('Current.Condition'     , wdata['currently']['summary'])
	set_property('Current.Temperature'   , str(wdata['currently']['temperature']))
	speed=float((wdata['currently']['windSpeed'])*1.60934)*2.5
	set_property('Current.Wind'          , str(speed))
	#set_property('Current.Wind'          , str(wdata['currently']['windSpeed']))
	windBearing = str(wdata['currently']['windBearing'])
	bearing = degToCompass(windBearing)
	set_property('Current.WindDirection' , bearing)
	set_property('Current.WindChill'     , str(wdata['currently']['apparentTemperature']))
	set_property('Current.Humidity'      , str(wdata['currently']['humidity']).replace('0.',''))
	set_property('Current.Visibility'    , str(wdata['currently']['visibility']))
	set_property('Current.Pressure'      , str(wdata['currently']['pressure']))
	set_property('Current.FeelsLike'     , str(wdata['currently']['apparentTemperature']))
	set_property('Current.DewPoint'      , str(wdata['currently']['dewPoint']))
	set_property('Current.UVIndex'       , str(wdata['currently']['uvIndex']))
	set_property('Current.OutlookIcon'   , '%s.png' % weathercode)
	set_property('Current.Pressure'     , str(round(wdata['currently']['pressure'] / 33.86 ,2)) + ' in')
	forecast = parse_data(data)
	sunrise = (forecast['daily']['data'][0]['sunriseTime'])
	sunset = (forecast['daily']['data'][0]['sunsetTime'])
	set_property('Today.Sunrise'         , str(time.strftime("%H:%M", time.localtime(int(sunrise)))))
	set_property('Today.Sunset'          , str(time.strftime("%H:%M", time.localtime(int(sunset)))))
	c=0
	for item in wdata['daily']['data']:
		c=c+1
	xbmc.log('ITEMS: ' + str(c),level=log_level)
	for count in range(c):
		set_property('Day%i.HighTemp'    % count, str(forecast['daily']['data'][count]['temperatureHigh']))
		set_property('Day%i.LowTemp'     % count, str(forecast['daily']['data'][count]['temperatureLow']))
		fdate = str(forecast['daily']['data'][count]['time'])
		fday = time.strftime("%A", time.localtime(int(fdate)))
		set_property('Day%i.Title'       % count, str(fday))
		#outlook = forecast['daily']['data'][count]['summary']
		set_property('Day%i.Outlook'     % count, unicode(forecast['daily']['data'][count]['summary']))
		weathercode = WEATHER_CODES[str(forecast['daily']['data'][count]['icon']).lower().replace('.gif','')]
		set_property('Day%i.OutlookIcon' % count, '%s.png' % weathercode)
		set_property('Day%i.FanartCode'         % count, weathercode)
		count = count + 1
xbmc.log('Version %s Started: %s' % (__version__, sys.argv),level=log_level)

set_property('WeatherProvider', __addonname__)
set_property('WeatherProviderLogo', xbmc.translatePath(os.path.join(__cwd__, 'resources', 'banner.png')))


if sys.argv[1].startswith('Location'):
	keyboard = xbmc.Keyboard('', xbmc.getLocalizedString(14024), False)
	keyboard.doModal()
	if (keyboard.isConfirmed() and keyboard.getText() != ''):
		text = keyboard.getText()
		items, locs, locids = location(text)
		dialog = xbmcgui.Dialog()
		if locs != []:
			selected = dialog.select(xbmc.getLocalizedString(396), items)
			if selected != -1:
				__addon__.setSetting(sys.argv[1], locs[selected])
				__addon__.setSetting(sys.argv[1] + 'id', locids[selected])
				xbmc.log('Selected Location: %s' % locs[selected],level=log_level)
		else:
			dialog.ok(__addonname__, xbmc.getLocalizedString(284))
else:
	location = __addon__.getSetting('Location%s' % sys.argv[1])
	locationid = __addon__.getSetting('Location%sid' % sys.argv[1])
	if (locationid == '') and (sys.argv[1] != '1'):
		location = __addon__.getSetting('Location1')
		locationid = __addon__.getSetting('Location1id')
		xbmc.log('Trying Location 1 Instead',level=log_level)
		xbmc.log(str(location),level=log_level)
		xbmc.log(str(locationid),level=log_level)
	if not locationid == '':
		forecast(location, locationid)
	else:
		xbmc.log('No Location Found',level=log_level)
		clear()
	refresh_locations()

xbmc.log('DarkSky Finished',level=log_level)
