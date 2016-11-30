#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for Python3 print function
from __future__ import print_function

# PyEZ
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# JSNAPy
from jnpr.jsnapy import SnapAdmin


class Router:
    def __init__(self, ipaddress, username, password):
        self.username = username
        self.password = password
        self.ipaddress = ipaddress
        self.device = Device(
                        host = ipaddress,
                        user =  username,
                        password = password)
        self.snap = SnapAdmin()

    def open(self):
        self.device.open()
        self.device.bind(cu=Config)
    
    def lock(self):
        self.device.cu.lock()

    def unlock(self):
        self.device.cu.unlock()

    def close(self):
        self.device.close()