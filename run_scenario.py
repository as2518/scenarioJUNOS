#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for Python3 print function
from __future__ import print_function

import sys
import yaml
from pprint import pprint 
from argparse import ArgumentParser

# for clolor font
import colorama
from colorama import Fore, Back, Style

# for PyEZ
from jnpr.junos import Device
from jnpr.junos.utils.config import Config


def run_pyez(option, device):
    output = ''
    if option == 'show_hostname':
        output = "hostname : %s" % ( device.facts['hostname'])
    elif option == 'show_model':
        output = "model : %s"    % ( device.facts['model'])
    elif option == 'show_version':
        output == "version: %s"   % ( device.facts['version'])
    else:
        output = 'Error option'

    return output

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
            scenario_param_yaml = f.read()
    except (IOError, IndexError):
        sys.stderr.write('Cannot open file : ' + args.file + '\n')
        sys.exit(1)

    # Convert yaml format to python_type
    try:
        scenario_param = yaml.load(scenario_param_yaml)
    except ValueError as error:
        sys.stderr.write('YAML format error : \n')
        sys.stderr.write(scenario_param_yaml)
        sys.stderr.write(str(error))
        sys.exit(1)

    #pprint(scenario_param)

    print('########## Run Senario : ' + args.file + ' ##########')

    print('operator : ' + scenario_param['operator'])
    print('operation_date : ' + str(scenario_param['operation_date']))
    
    print('hostname : ', end='')
    for host in scenario_param['hosts']:
        print(host['hostname'])
    
    print('purpose :')
    print(scenario_param['purpus'])
    
    for key,value in scenario_param['operation_param'].items():
        print(str(key) + ' : ' + str(value))
    
    print('Operation Start : ', end='')
    print(Fore.GREEN + 'OK')



if __name__ == '__main__':
    main()
    print(Fore.YELLOW + "Do you start to operation? y/n")
    choice = raw_input().lower()
    if choice != 'y':
        print('This operation is aborted') 
        sys.exit(0)

    print('Connect to ' + scenario_param['hosts'][0]['hostname'] + ' : ', end='')
    dev1 = Device(
            host = scenario_param['hosts'][0]['device'],
            user = scenario_param['hosts'][0]['username'],
            password = scenario_param['hosts'][0]['password'] )
    dev1.open()
    dev1.bind(cu=Config)
    dev1.cu.lock()
    print(Fore.GREEN + 'OK')

    #print("hostname : %s" % ( dev1.facts['hostname']))
    #print("model : %s"    % ( dev1.facts['model']))
    #print("version: %s"   % ( dev1.facts['version']))

    print(run_pyez(option='show_hostname', device = dev1))
    print(run_pyez(option='show_model', device = dev1))
    print(run_pyez(option='show_version', device = dev1))



    dev1.cu.unlock()
    dev1.close()
