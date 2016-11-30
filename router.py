#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for Python3 print function
from __future__ import print_function

# Jinja2 Template Engine
from jinja2 import Template, Environment

# PyEZ
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# JSNAPy
from jnpr.jsnapy import SnapAdmin

# arranged print
from pprint import pprint, pformat

class Router:
    def __init__(self, hostname, model, ipaddress, username, password):
        self.hostname  = hostname
        self.model     = model
        self.username  = username
        self.password  = password
        self.ipaddress = ipaddress
        self.device    = Device(host=ipaddress, user=username, password=password)
        self.snap      = SnapAdmin()

    def open(self):
        self.device.open()
        self.device.bind(cu=Config)
    
    def lock(self):
        self.device.cu.lock()

    def unlock(self):
        self.device.cu.unlock()

    def close(self):
        self.device.close()

    def snaptest(self, operation):
        
        test_result = False
        message = ''

        if operation == 'test_hostname':
            template_filename = './test_templates/test_hostname.jinja2'
            tamplate_param = { 'hostname' : self.hostname }
            test_filename =  './tests/test_hostname_' + self.hostname + '.yml'
        elif operation == 'test_model':
            template_filename = './test_templates/test_model.jinja2'
            tamplate_param = { 'model' : self.model }
            test_filename =  './tests/test_model_' + self.hostname + '.yml'
        else:
            pass

        self.generate_testfile(
            template_filename   = template_filename,
            template_param      = tamplate_param,
            test_filename       = test_filename)

        jsnapy_conf = 'tests:' + '\n' +\
                      '  - %s' % (test_filename)
        
        snapcheck_dict = self.snap.snapcheck(data=jsnapy_conf, dev=self.device)

        for snapcheck in snapcheck_dict:

            if snapcheck.result == 'Passed':
                expected_value = snapcheck.test_details.values()[0][0]['expected_node_value']
                acutual_value  = snapcheck.test_details.values()[0][0]['passed'][0]['actual_node_value']

                test_result = True
                message =   'expected value : %s\n' % (expected_value) +\
                            'acutual  value : %s'   % (acutual_value)
            elif snapcheck.result == 'Failed':
                expected_value = snapcheck.test_details.values()[0][0]['expected_node_value']
                acutual_value  = snapcheck.test_details.values()[0][0]['failed'][0]['actual_node_value']


                test_result = False
                message =   'expected value : %s\n' % (expected_value) +\
                            'acutual  value : %s'   % (acutual_value)                
        return test_result, message
        
        # for debug
        ''''
        for snapcheck in snapcheck_dict:
            print("Final result : ", snapcheck.result)
            print("Total passed : ",   snapcheck.no_passed)
            print("Total failed : ",   snapcheck.no_failed)
            print('snapcheck test_details : ')
            print('-'*30)
            pprint(dict(snapcheck.test_details)) 
            print('-'*30)
        '''

    

    def generate_testfile(self, template_filename, template_param, test_filename):
        # read template file (jinja2 format)
        with open(template_filename, 'r') as conf:
            template_jinja2 = conf.read()

        # generate test file from template file
        test_yml = Environment().from_string(template_jinja2).render(template_param)
        
        # write test file (YAML format)
        with open(test_filename, 'w') as f:
            f.write(test_yml)
