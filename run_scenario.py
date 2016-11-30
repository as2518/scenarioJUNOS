#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for Python3 print function
from __future__ import print_function

import sys
import yaml
from pprint import pprint, pformat
from argparse import ArgumentParser

# timestamp
from datetime import datetime

# clolor font
import colorama
from colorama import Fore, Back, Style

# PyEZ
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# JSNAPy
from jnpr.jsnapy import SnapAdmin

from router import Router

def main():
    """main function."""

    # Parse argment
    parser = ArgumentParser(description='run scenario_file')
    parser.add_argument('-f', '--file',
                        type=str,
                        help='scenario file',
                        required=True)
    args = parser.parse_args()

    #Set color font
    colorama.init(autoreset=True)
    
    # Read router infomation file
    try:
        with open(args.file, 'r') as f:
            param_yaml = f.read()
    except (IOError, IndexError):
        sys.stderr.write('Cannot open file : ' + args.file + '\n')
        sys.exit(1)

    # Convert yaml format to python_type
    try:
        param = yaml.load(param_yaml)
    except ValueError as error:
        sys.stderr.write('YAML format error : \n')
        sys.stderr.write(param_yaml)
        sys.stderr.write(str(error))
        sys.exit(1)


    router1 = Router(
                hostname    = param['hosts']['hostname'],
                model       = param['hosts']['model'],
                ipaddress   = param['hosts']['management_ipaddress'],
                username    = param['hosts']['username'],
                password    = param['hosts']['password'])

    print('########## Run Senario : ' + args.file + ' ##########')

    print('operator : %s'       % (param['operator']) )
    print('operation_date : %d' % (param['operation_date']) )
    print('hostname : %s'       % (param['hosts']['hostname']) )
    print('model : %s'          % (param['hosts']['model']) )
    print('purpose :')
    print(param['purpus'])
    
    print('Connect to ' + param['hosts']['hostname'] + ' : ', end='')
    router1.open()
    print(Fore.GREEN + 'OK')

    print('Lock configure mode : ', end='')
    router1.lock()
    print(Fore.GREEN + 'OK')

    for operation in param['scenario']:
  
        print('Test on "%s" : '%(operation), end='')
  
        if "test_" in operation:
            result, message = router1.snaptest(operation)
            
            if result : 
                print(Fore.GREEN + 'OK')
                print(Fore.GREEN + message)
            else:
                print(Fore.RED + 'NG')
                print(Fore.RED + message)

        elif "set_" in operation:
            pass
        else:
            print('Cannnot run operation : ' + operation)
 
    print('Unlock configure mode : ', end='')
    router1.unlock()
    print(Fore.GREEN + 'OK')

    print('Close the connection to ' + param['hosts']['hostname'] + ' : ', end='')
    router1.close()
    print(Fore.GREEN + 'OK')

    print('########## End Senario : ' + args.file + ' ##########')


if __name__ == '__main__':
    main()

