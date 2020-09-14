# tb_server_defs.py

# please put the thingsboard server URL (IP) here
global tb_server_url
tb_server_url = 'https://iot.sglux.com'

# definition of authorization address
# this should not need modifikation!
global tb_server_api
tb_server_api = tb_server_url + '/api'

global tb_server_auth
tb_server_auth = tb_server_url + '/api/auth/login'
