#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for PyEZ
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

class Router:
    def __init__(self, host_ipaddr, username, password):
        self.username = username
        self.password = password
        self.host_ipaddress = host_ipaddress
        self.dev = 
    def login(self):
              

    def logout(self):
        if self.session:
            self.session.send('exit\r')
            self.session.close()
        else:
            raise AttributeError('cannot find a living session.')
