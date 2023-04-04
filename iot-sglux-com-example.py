# --------------------------------------------------------------------
# imports, some packages might need installation with pip
import json
import requests
import datetime
import os, sys
import dateutil
from dateutil.parser import *
from prettytable import PrettyTable

# try to import credentials from your private my_tb_credentials.py file
try:
    from my_tb_credentials import username, password
except ImportError:
    # if that file does not exist, try to import the credential template
    try:
        from tb_credentials import username, password
    except ImportError:
        print("You should copy tb_credentials.py to my_tb_credentials.py and fill it with your actual data!")
        print(sys.exc_info())
        exit()

            
# try to import credentials from your private my_tb_server_defs.py file
try:
    from my_tb_server_defs import tb_server_url, tb_server_api, tb_server_auth
except ImportError:
    # if that file does not exist, try to import the credential template
    try:
        from tb_server_defs import tb_server_url, tb_server_api, tb_server_auth
    except ImportError:
        print("You should copy tb_server_defs.py to my_tb_server_defs.py and fill it with your actual data!")
        print(sys.exc_info())
        exit()


from pylux_tb import *

# --------------------------------------------------------------------
#request session token
response = requests.post(tb_server_auth, headers=tb_auth_header(), data=tb_auth_data(username, password))
data=json.loads((str(response.content,"utf-8")))
# extract the access tokens
tb_token =(data['token'])

# If you want to use SwaggerUI enable the below print statement. 
# Copy everything printed out including "Bearer " to the value field
# (api_key) in the "Authorize" dialog within SwaggerUI which you can
# access under {your-server-url}/swagger-ui.html 
#print('\nBearer '+ tb_token)

# --------------------------------------------------------------------
# now start with requests
api_url = tb_server_api + '/device/types'
data = requests.get(api_url, headers=tb_req_header(tb_token))
dtps = json.loads((str(data.content,"utf-8")))
print('\nList of available device types in your account')
t=PrettyTable(['Index','deviceType'])
for index, obj in enumerate(dtps, start=0):
    t.add_row([index,obj['type']])
print(t)
if (index == 0) :
    print('Only one device type found, using this one!')
    deviceType = dtps[0]['type']
elif (index == None) :
    print('no devices / devicetypes found at all, exiting...')
    exit()
else:
    idx = get_num_input('Which device type',0,index,0)
    deviceType = dtps[idx]['type']

# request list of avaliable devices of a specified type
api_url = tb_server_api + '/tenant/devices?type=' + deviceType + '&limit=1000'
data = requests.get(api_url, headers=tb_req_header(tb_token))
types = json.loads((str(data.content,"utf-8")))
print('\nList of the devices of the specified type')
t=PrettyTable(['Index','deviceName','deviceID'])
for index, obj in enumerate(types['data'], start=0):
    t.add_row([index, obj['name'], obj['id']['id']])
print(t)

#ask user for the device
devn = get_num_input('Enter the device by index',0,index,0)
# set deviceID and deviceName for subsequent use
deviceID = types['data'][devn]['id']['id']
deviceName = types['data'][devn]['name']

# get the list of attributes of that device
api_url = tb_server_api + '/plugins/telemetry/DEVICE/' + deviceID + '/values/attributes'
data = requests.get(api_url, headers=tb_req_header(tb_token))
atts = json.loads((str(data.content,"utf-8")))
print('\nList of the attributes of the selected device')
t=PrettyTable(['Index','Attribute','Value'])
for index, obj in enumerate(atts, start=0):
    t.add_row([index, str(obj['key']), str(obj['value'])])
print(t)

# get the list of available time series of that device
api_url = tb_server_api + '/plugins/telemetry/DEVICE/' + deviceID + '/keys/timeseries'
data = requests.get(api_url, headers=tb_req_header(tb_token))
keys = json.loads((str(data.content,"utf-8")))
print('\nList of the available time series of the selected device')
t=PrettyTable(['Index','timeseries Key'])
for index, obj in enumerate(keys, start=0):
    t.add_row([index,obj])
print(t)
# ask user for telemetry type to pull
keyn = get_num_input('Select the telemetry type by index',0,index,11)
key_req = str(keys[keyn])
print('Ok, pulling telemetry of type',key_req)
Keys ='&keys='+key_req

# ... by building the url containing all request related parameters ...
controller='/plugins/telemetry/DEVICE/'
Val = '/values/timeseries?'
Limit='limit=1000000&'

# Startzeitpuntk
date1 = dateutil.parser.isoparse(input('\nEnter start time (YYYY-MM-DD HH:MM): '))
ts1=str(int(date1.timestamp()))
Start_t='&startTs=' + ts1 + '000'

# Endzeitpunkt
date2 = dateutil.parser.isoparse(input('\nEnter start time (YYYY-MM-DD HH:MM): '))
ts2=str(int(date2.timestamp()))
End_t='&endTs=' + ts2 + '000'

# construct complete url
api_url = tb_server_api + controller + deviceID + Val + Limit + Keys + Start_t + End_t
# request data
print('\nRequesting Data for time range',ts1,'to',ts2)
data = requests.get(api_url, headers=tb_req_header(tb_token))
# convert received data from jsonpath to json object
uvi_s=json.loads((str(data.content,"utf-8")))
print('Received Data Points:', len(uvi_s[key_req]))

# convert and save data as csv file
filename = os.path.expanduser("~") + '\\Desktop\\' + deviceName +'_data_'+key_req+'.csv'
datei = open(filename , 'w')
print('Timestamp','Time',str(deviceName) + '/'+key_req, sep=';', file=datei)
for index, obj in reversed(list(enumerate(uvi_s[key_req], start=1))):
    # export epoch in seconds, time and date, selected telemetry
    print((str(obj['ts'])[:-3]), datetime.datetime.fromtimestamp(obj['ts']/1000), obj['value'], sep=';', file=datei)
datei.close()
print('\nWritten' , len(uvi_s[key_req]) ,'Data Points of device',deviceName,'from',date1,'to',date2,'into file',filename)
