#!/usr/bin/env python3

import os
import sys

#cleandoc
from inspect import cleandoc

#looking up ip from icanhazip
import requests

#coloring output
from termcolor import colored

#subprocess to execute less command
import pydoc

#shodan library
import shodan
with open('api_key.txt') as api_key:
    SHODAN_API_KEY = api_key.readline().rstrip()
api = shodan.Shodan(SHODAN_API_KEY)

def options():
    OPTIONS_DICT = {
        '1':icanhazip,
        '2':shodan_query,
        '3':shodan_lookup_host,
        '0':cool_exit
    }
    
    while True:
        option = input('\n'+cleandoc(
            '''
            1.What's my ip?
            2.Query Shodan.
            3.Lookup shodan host.
            0.Exit

            Shodan> 
            '''
        ))

        if option in OPTIONS_DICT.keys():
            return OPTIONS_DICT[option]
        else:
            print('\nOption not found. Try again.')
                  

def icanhazip():
    os.system('clear')
    try : 
        myip = requests.get('https://icanhazip.com').text.rstrip()
    except requests.exceptions.RequestException as e:
        print(e)
        return
    
    print('Your IP is: \n')
    print(myip)
    #print('<My Ip-Addr>')
    
def shodan_query():
    os.system('clear')
    shodan_query = input('Enter Query : ')
    
    # load results
    try:
        results = api.search(shodan_query)
    except shodan.APIError as e:
        print(e)
        return

    #load the data in the form of
    #ip port organization hostnames...
    data = ''    
    for result in results['matches']:

        result_ip_str = result['ip_str'].ljust(15)
        result_port = str(result['port']).ljust(6)
        result_org = result['org']
        result_host = result['hostnames'][0] if len(result['hostnames'])> 0 else ''
        
        data+= \
        colored(result_ip_str,'green')+' '+ \
        colored(result_port,'red') +' '+ \
        colored(result_org,'cyan') +' '+ \
        colored(result_host,'magenta') +'\n'
    
    #pydoc pager does not color
    try:
        pydoc.pipepager(data,cmd='less -R')
    except KeyboardInterrupt:
        return
def shodan_lookup_host():

    #clear the console
    os.system('clear')
    print('')

    #get input and lookup host
    host = input('Input host IP address : ')
    
    try:
        result = api.host(host)
    except shodan.APIError as e:
        print(e)
        return

    #print IP in green
    print(colored(result['ip_str'],'green'))
    
    #print hostname data
    for (index ,hostname) in enumerate(result['hostnames']):
        if index == 0:
            print('Hostnames:'.ljust(25),end='')
        else:
            print(''.ljust(25),end='')
        print(str(hostname))
    #print City
    print('City : '.ljust(25)+str(result['city']))
    
    #print Country
    print('Country : '.ljust(25)+str(result['country_name']))
    
    #print number of open ports
    print('Number of open ports : '.ljust(25)+str(len(result['ports']))+'\n' )
    
    #print data for each port
    print('Ports : ')
    for port in result['data']:
        if 'port' in port:
            print('    ' +colored(port['port'],'cyan'),end='')
            
            if 'product' in port:
                print(' ' + port['product'],end='')
            
            print('')
    print('')

def cool_exit():
    print('Exiting.')
    sys.exit(0)
    
while True:
    options()()
