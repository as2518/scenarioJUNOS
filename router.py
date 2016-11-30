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

    def commit(self):
        return self.device.cu.commit()

    def rollback(self):
        return self.device.cu.rollback()

    def diff_config(self):
        if self.device.cu.diff():
            message = self.device.cu.diff()
        else:
            message = ''
        return message
    
    def commit_check(self):
        return self.device.cu.commit_check()
        
    def load_config(self, operation_name, operation_param=None):
        set_result = False
        message = ''
        if operation_name == 'set_add_interface':
            template_filename = './set_templates/add_interface.jinja2'
            tamplate_param = operation_param

        config_txt = self.generate_from_jinja2(template_filename, tamplate_param)
        
        self.device.cu.load(
            template_path   = template_filename, 
            template_vars   = tamplate_param, 
            format          = "text",
            merge           = True )
        
        message = config_txt
        set_result = True
        
        return set_result, message
    
        

    def snaptest(self, operation_name, operation_param=None):
        
        test_result = False
        message = ''

        if operation_name == 'test_hostname':
            template_filename = './test_templates/test_hostname.jinja2'
            tamplate_param = { 'hostname' : self.hostname }
            test_filename =  './tests/test_hostname_' + self.hostname + '.yml'
        elif operation_name == 'test_model':
            template_filename = './test_templates/test_model.jinja2'
            tamplate_param = { 'model' : self.model }
            test_filename =  './tests/test_model_' + self.hostname + '.yml'


        elif operation_name == 'test_interface':
            template_filename = './test_templates/test_interface.jinja2'
            tamplate_param = operation_param
            test_filename =  './tests/test_interface_' +\
                             operation_param['interface_name'].replace('/','-') + '_' +\
                             operation_param['interface_status'] + '.yml'

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
                test_result = True

                expected_value = snapcheck.test_details.values()[0][0]['expected_node_value']
                acutual_value  = snapcheck.test_details.values()[0][0]['passed'][0]['actual_node_value']

                message =   'test file      : %s\n' % test_filename +\
                            'expected value : %s\n' % (expected_value) +\
                            'acutual  value : %s'   % (acutual_value)
            elif snapcheck.result == 'Failed':
                test_result = False

                expected_value = snapcheck.test_details.values()[0][0]['expected_node_value']
                acutual_value  = snapcheck.test_details.values()[0][0]['failed'][0]['actual_node_value']

                message =   'test file      : %s\n' % test_filename +\
                            'expected value : %s\n' % (expected_value) +\
                            'acutual  value : %s'   % (acutual_value)                
        
            # for debug
            '''
            for snapcheck in snapcheck_dict:
                print(test_filename )
                print("Final result : ", snapcheck.result)
                print("Total passed : ",   snapcheck.no_passed)
                print("Total failed : ",   snapcheck.no_failed)
                print('snapcheck test_details : ')
                print('-'*30)
                pprint(dict(snapcheck.test_details)) 
                print('-'*30)
            '''
            
            
        return test_result, message
        
     
        


    def generate_testfile(self, template_filename, template_param, test_filename):  
        test_yml = self.generate_from_jinja2(template_filename, template_param)
       
        # write test file (YAML format)
        with open(test_filename, 'w') as f:
            f.write(test_yml)

    def generate_from_jinja2(self, template_filename, template_param):
        # read template file (jinja2 format)
        with open(template_filename, 'r') as f:
            template_jinja2 = f.read()

        # generate test file from template file
        output_txt = Environment().from_string(template_jinja2).render(template_param)

        return output_txt