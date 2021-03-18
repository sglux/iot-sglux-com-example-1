# tb_functions.py
import requests
import json

# --------------------------------------------------------------------
# function waiting for input of an integer between min/max for selection
# of something
def get_num_input(prompt, min, max, default):
    while True:
        try:
            value = int(input(prompt + ' [' + str(min) + '...' + str(max) + ' | default: ' + str(default) + '] : '))
        except ValueError:
            print('\nError, input was not a valid number, try again')
            continue
        except KeyboardInterrupt:
            print('\nInput exited with Ctrl+C, using default ' + str(default))
            return default
        if value < min or value > max:
            print("\nValue was not in requested range, try again!")
            continue
        else:
            break
    return value

#define header used for authentication
def tb_auth_header():
    xd = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    return xd

# header for data requests
def tb_req_header(tb_token):
    xd = {
        'Accept': 'application/json',
        'X-Authorization': 'Bearer ' + tb_token,
    }
    return xd

def tb_auth_data(tb_user, tb_pass):
    xd = '{"username":"' + str(tb_user)+'","password":"' + str(tb_pass) + '"}'
    return xd
