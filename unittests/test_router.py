#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import router

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = router.Router(
            hostname='test_host',
            model='test_model',
            ipaddress='192.168.0.1',
            username='test_username',
            password='test_passoword')

        self.interface_name = 'xe-0/0/0'
        self.interface_description = 'test_desc'
        self.interface_address_ipv4 = '10.10.0.1'
        self.interface_subnet_ipv4 = '24'

    def test_generate_from_jinja2(self):
        template_filename =\
            './unittests/templates/set_add_interface.jinja2'
        template_param = {
            'interface_name': self.interface_name,
            'interface_description': self.interface_description,
            'interface_address_ipv4': self.interface_address_ipv4,
            'interface_subnet_ipv4': self.interface_subnet_ipv4}
        actual = self.router.generate_from_jinja2(template_filename, template_param)

        with open('./unittests/expected/set_add_interface.conf', 'r') as file:
            expected = file.read()

        self.assertEqual(actual, expected)

    def test_generate_nwtestfile(self):
        template_filename =\
            './unittests/templates/nwtest_hostname.jinja2'
        template_param = {'hostname': 'test_router'}
        nwtest_filename = './unittests/actual/nwtest_hostname.yml'

        actual_filename = nwtest_filename
        expected_filename = './unittests/expected/nwtest_hostname.yml'

        self.router.generate_nwtestfile(
            template_filename,
            template_param,
            nwtest_filename)

        with open(actual_filename, 'r') as file:
            actual = file.read()

        with open(expected_filename, 'r') as file:
            expected = file.read()

        self.assertEqual(actual, expected)

        os.remove(actual_filename)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()