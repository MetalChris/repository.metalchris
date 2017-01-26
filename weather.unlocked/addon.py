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

import os, sys, socket, urllib2
import xbmc, xbmcgui, xbmcaddon
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson
import time

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

LOC_URL          = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s'
#LOC_QUERY        = 'http://maps.googleapis.com/maps/api/geocode/json?address="%s"'
API_URL          = 'http://api.weatherunlocked.com/api/current/'
APP_ID		= __addon__.getSetting(id="APP_ID")
API_KEY	= __addon__.getSetting(id="API_KEY")
#xbmc.log(str(APP_ID))
#xbmc.log(str(API_KEY))
WEATHER_ICON     = xbmc.translatePath('special://temp/weather/%s.png').decode("utf-8")
WEATHER_WINDOW   = xbmcgui.Window(12600)
NOW = time.time()
LOCAL_TIME = time.localtime(NOW)
HOUR = time.strftime("%H", LOCAL_TIME)
TODAY = time.strftime("%A", LOCAL_TIME)
##xbmc.log('LOCAL TIME: ' + str(LOCAL_TIME))
#xbmc.log('HOUR: ' + str(HOUR))

socket.setdefaulttimeout(10)

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    #xbmc.log(msg=message.encode("utf-8"), level=#xbmc.logDEBUG)

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
    log('available locations: %s' % str(locations))

def location(loc):
    items  = []
    locs   = []
    locids = []
    query = find_location(loc)
    data = parse_data(query)
    listitem   = data['results'][0]['formatted_address']
    location = listitem
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    locationid = str(lat) + ',' + str(lng)
    items.append(listitem)
    locs.append(location)
    locids.append(locationid)
    return items, locs, locids

def find_location(loc):
    query = urllib2.quote(loc)
    url = LOC_URL % query
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response

def parse_data(reply):
    try:
        data = simplejson.loads(reply)
    except:
        log('failed to parse weather data')
        data = ''
    return data

def forecast(loc,locid):
    log('weather location: %s' % locid)
    retry = 0
    while (retry < 6) and (not xbmc.abortRequested):
        query = get_weather(locid)
        if query != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('weather download failed')
    log('forecast data: %s' % query)
    retry = 0
    while (retry < 6) and (not xbmc.abortRequested):
        fquery = get_forecast(locid)
        if fquery != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('forecast download failed')
    log('forecast data: %s' % fquery)
    if fquery != '':
        properties(query,fquery,loc,locid)
    else:
        clear()

def get_weather(locid):
    xbmc.log('GET WEATHER')
    url = API_URL + str(locid) + '?app_id=' + APP_ID + '&app_key=' + API_KEY
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
    xbmc.log('GET FORECAST')
    url = API_URL.replace('current','forecast') + str(locid) + '?app_id=' + APP_ID + '&app_key=' + API_KEY
    #xbmc.log('GET FORECAST URL:' + str(url))
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0')
        req.add_header('Accept','application/json')
        response = urllib2.urlopen(req)
        fdata = response.read()
        req.close()
    except:
        xbmc.log('EXCEPTION!')
        response = ''
        #get_forecast(locid)
    return fdata

def clear():
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
    for count in range (0, 5):
        set_property('Day%i.Title'       % count, 'N/A')
        set_property('Day%i.HighTemp'    % count, '0')
        set_property('Day%i.LowTemp'     % count, '0')
        set_property('Day%i.Outlook'     % count, 'N/A')
        set_property('Day%i.OutlookIcon' % count, 'na.png')
        set_property('Day%i.FanartCode'  % count, 'na')

def properties(data,fdata,loc,locid):
    xbmc.log('PROPERTIES')
    wdata = parse_data(data)
    weathercode = WEATHER_CODES[(wdata['wx_icon']).lower().replace('.gif','')]
    set_property('Current.Location'      , loc)
    set_property('Current.Condition'     , wdata['wx_desc'])
    set_property('Current.Temperature'   , str(wdata['temp_c']))
    set_property('Current.Wind'          , str(wdata['windspd_mph']))
    set_property('Current.WindDirection' , str(wdata['winddir_compass']))
    set_property('Current.WindChill'     , str(wdata['feelslike_c']))
    set_property('Current.Humidity'      , str(wdata['humid_pct']))
    set_property('Current.Visibility'    , str(wdata['vis_mi']))
    set_property('Current.Pressure'      , str(wdata['slp_in']))
    set_property('Current.FeelsLike'     , str(wdata['feelslike_c']))
    set_property('Current.DewPoint'      , str(wdata['dewpoint_c']))
    set_property('Current.UVIndex'       , 'N/A')
    set_property('Current.OutlookIcon'   , '%s.png' % weathercode)
    forecast = parse_data(fdata)
    set_property('Today.Sunrise'         , str(forecast['Days'][0]['sunrise_time']))
    set_property('Today.Sunset'          , str(forecast['Days'][0]['sunset_time']))
    #xbmc.log('HOUR: ' + str(HOUR))
    if HOUR < 12:
	count = 1
    else:
        count = 0
    for count in range(0,5):
	#xbmc.log(str(count))
	#xbmc.log(str(TODAY))
        set_property('Day%i.HighTemp'    % count, str(forecast['Days'][count+1]['temp_max_c']))
        set_property('Day%i.LowTemp'     % count, str(forecast['Days'][count+1]['temp_min_c']))
       # set_property('Day%i.Title'       % count, str(forecast['Days'][count+1]['date']))
	fdate = str(forecast['Days'][count+1]['date'])
	fday = time.strptime(fdate, "%d/%m/%Y")#.strftime("%m/%d/%Y")
	fdaynew = time.strftime("%A", fday)
	#xbmc.log(str(fdaynew))
	if str(fdaynew) != str(TODAY):
            set_property('Day%i.Title'       % count, str(fdaynew))
	else:
	    set_property('Day%i.Title'       % count, 'Today')
        set_property('Day%i.Outlook'     % count, str(forecast['Days'][count+1]['Timeframes'][3]['wx_desc']))
        ##set_property('Day%i.FanartCode'  , '20')
        weathercode = WEATHER_CODES[str(forecast['Days'][count+1]['Timeframes'][3]['wx_icon']).lower().replace('.gif','')]
        set_property('Day%i.OutlookIcon' % count, '%s.png' % weathercode)
	#'special://home/addons/weather.unlocked/resources/media/'
	count = count + 1
	##xbmc.log(str(count))
#log('version %s started: %s' % (__version__, sys.argv))

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
                log('selected location: %s' % locs[selected])
        else:
            dialog.ok(__addonname__, xbmc.getLocalizedString(284))
else:
    location = __addon__.getSetting('Location%s' % sys.argv[1])
    locationid = __addon__.getSetting('Location%sid' % sys.argv[1])
    if (locationid == '') and (sys.argv[1] != '1'):
        location = __addon__.getSetting('Location1')
        locationid = __addon__.getSetting('Location1id')
        log('trying location 1 instead')
    if not locationid == '':
        forecast(location, locationid)
    else:
        log('no location found')
        clear()
    refresh_locations()

log('finished')
