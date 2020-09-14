# --------------------------------------------------------------------
# imports, some packages might need installation with pip
import json
import requests
import datetime
import time
import os
import pprint
import dateutil
from dateutil.parser import parse
from dateutil.tz import gettz

#import credentials from file: PLEASE UPDATE IN ANY CASE
from tb_credentials_ import username, password

# import server URLS to be used: PLEASE UPDATE IF REQUIRED
from tb_server_defs import tb_server_url, tb_server_api, tb_server_auth

from pylux_tb import *

# --------------------------------------------------------------------
#request session token
response = requests.post(tb_server_auth, headers=tb_auth_header(), data=tb_auth_data(username, password))
data=json.loads((str(response.content,"utf-8")))
# extract the access tokens
tb_token =(data['token'])
#tb_refresht = (data['refreshToken'])
#print(tb_req_header(tb_token))

# --------------------------------------------------------------------
# now start with requests
api_url = tb_server_api + '/device/types'
data = requests.get(api_url, headers=tb_req_header(tb_token))
dtps = json.loads((str(data.content,"utf-8")))
print(dtps)
print('\nIndex\tdeviceType')
for index, obj in enumerate(dtps, start=0):
    print(index,'\t',obj['type'],sep="")
if (index == 0) :
    print('Only one device type found, using this one!')
    deviceType = dtps[0]['type']
elif (index == None) :
    print('no devices / devicetypes found at all, exiting...')
    exit()
else:
    idx = get_num_input('Which device type:',0,index,0)
    deviceType = dtps[idx]['type']

# request list of avaliable devices of a specified type types
api_url = tb_server_api + '/tenant/devices?type=' + deviceType + '&limit=1000'

data = requests.get(api_url, headers=tb_req_header(tb_token))
types = json.loads((str(data.content,"utf-8")))
# list their name and id
print('\nIndex\tDevice-Name\tDevice-ID')
for index, obj in enumerate(types['data'], start=0):
    print(index,'\t',obj['name'],'\t\t',obj['id']['id'],sep="")
#ask user for the device
devn = get_num_input('Enter the device by index',0,index,0)
# set deviceID and deviceName for subsequent use
deviceID = types['data'][devn]['id']['id']
deviceName = types['data'][devn]['name']

# ... by building the url containing all request related parameters ...
controller='/plugins/telemetry/DEVICE/'
Val = '/values/timeseries?'
Limit='limit=1000&'
Keys ='&keys=uvi'

# Startzeitpuntk
date1 = dateutil.parser.isoparse(input('Enter start time (YYYY-MM-DD HH:MM): '))
ts1=str(int(date1.timestamp()))
Start_t='&startTs=' + ts1 + '000'
print(Start_t)

# Endzeitpunkt
date2 = dateutil.parser.isoparse(input('Enter start time (YYYY-MM-DD HH:MM): '))
ts2=str(int(date2.timestamp()))
End_t='&endTs=' + ts2 + '000'
print(End_t)

# construct complete url
api_url = tb_server_api + controller + deviceID + Val + Limit +Keys + Start_t + End_t
# request data
print('\nRequesting Data for time range',ts1,'to',ts2)
data = requests.get(api_url, headers=tb_req_header(tb_token))
# convert received data from jsonpath to json object
uvi_s=json.loads((str(data.content,"utf-8")))
print('Received Data Points:', len(uvi_s['uvi']))

# convert and save data as csv file
filename = os.path.expanduser("~") + '\\Desktop\\' + deviceName +'_data.csv'
datei = open(filename , 'w')
print('Timestamp','Time',str(deviceName), sep=';', file=datei)
for index, obj in reversed(list(enumerate(uvi_s['uvi'], start=1))):
    print((str(obj['ts'])[:-3]), datetime.datetime.fromtimestamp(obj['ts']/1000), obj['value'], sep=';', file=datei)
    #print((str(obj['ts'])[:-3]),obj['value'],sep=';')
datei.close()
print('\nWritten' , len(uvi_s['uvi']) ,'Data Points of device',deviceName,'from',date1,'to',date2,'into file',filename)
