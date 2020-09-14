# Example 1
## Requesting data from iot.sglux.com (a [Thingsboard](https://thingsboard.io/))
### Requirements
* in any case it is required to edit the username and password in [tb_credentials.py](tb_credentials.py) with user credentials of a thingsboard tenant admin user
* you may need to change the `tb_server_url` in [tb_server_defs.py](tb_server_defs.py) in order to use another thingsboard instance 

### What it does
1) it presents a list of known device types, in out case we are interested in devices of type sg-iot-gen* to choose from.
2) it presents a list of devices of the selected type to choose from
3) it presents a list of avalable timeseries of this device to choose from
4) it exports the requested data into an CSV file on your desktop, containing all device attributes in the header and the timeseries in the data sections
