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

def run_test(device, jsnapy, menue, param=None):
    print('Run %s : ' % menue, end='')

    #jsnapy = SnapAdmin()
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    snap_name = 'snap' + timestamp

    # 知見: snapcheck関数でDeviceクラスを利用するときはhost部は不要 
    #jsnapy_config = jsnapy_config_host +\
    jsnapy_config =\
        'tests:\n' +\
        ' - ./tests/%s.yml' % (menue)
    #print(jsnapy.snapcheck(data=jsnapy_config, file_name=snap_name, dev=dev1))
    
    snapcheck_list = jsnapy.snapcheck(
                        data=jsnapy_config,
                        file_name=snap_name,
                        dev=device)
    
    pprint(snapcheck_list)
    
    print('start check')
    for snapcheck in snapcheck_list:
        #pprint(dict(snapcheck.test_details))
        #pprint(dict(snapcheck.log_detail))
        pprint(snapcheck.logger_testop)
        pprint(dict(snapcheck.result_dict))

        if snapcheck.result == 'Passed':
            print(Fore.GREEN + 'OK')
        elif snapcheck.result == 'Failed':
            print(Fore.RED + 'NG')
            #print(Fore.RED + dict(snapcheck.test_details))
            print(Fore.RED, end='')
            print(Fore.RED + pformat(dict(snapcheck.test_details)))
        else:
            print('else2')
    print('finish check')
        
    


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

    #pprint(param)

    print('########## Run Senario : ' + args.file + ' ##########')

    print('operator : ' + param['operator'])
    print('operation_date : ' + str(param['operation_date']))
    print('hostname : ' + param['hosts']['hostname'])
    print('purpose :')
    print(param['purpus'])
    #print(param['scenario'])

    #print(param['scenario'][0])

    print('Operation Start : ', end='')
    print(Fore.GREEN + 'OK')

    print('Connecting to ' + param['hosts']['hostname'] + ' : ', end='')
    dev1 = Device(
            host = param['hosts']['device'],
            user = param['hosts']['username'],
            password = param['hosts']['password'],
            port = 22)
    dev1.open()
    dev1.bind(cu=Config)
    dev1.cu.lock()
    print(Fore.GREEN + 'OK')


    

    
    # 知見: snapcheck関数でDeviceクラスを利用するときはhost部は不要
    #jsnapy_config_host =\
    #    'hosts:\n' +\
    #    '- device: %s\n'    % (param['hosts']['device']) +\
    #    '  username : %s\n' % (param['hosts']['username']) +\
    #    '  passwd: %s\n'    % (param['hosts']['password'])
    
    jsnapy = SnapAdmin()

    for menue in param['scenario']:
        pprint(menue)
        if 'test_' in menue:
            if menue ==  'test_hostname':
                run_test(device=dev1,jsnapy=jsnapy, menue=menue)
            elif menue == 'test_cpu':
                run_test(device=dev1,jsnapy=jsnapy, menue=menue)
        elif 'set_' in menue:
            #pass
            print(Fore.GREEN + 'set_')
        else:
            pass
            print(Fore.GREEN + 'else')
    
       
            
            

    print('Closing conection to ' + param['hosts']['hostname'] + ' : ', end='')

    dev1.cu.unlock()
    dev1.close()
    print(Fore.GREEN + 'OK')
    

if __name__ == '__main__':
    main()

