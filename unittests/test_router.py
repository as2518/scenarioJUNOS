#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import router

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = router.Router(
            hostname = 'test_host',
            model = 'test_model',
            ipaddress = '192.168.0.1',
            username = 'test_username',
            password = 'test_passoword')
    
    def test_generate_testfile(self):
        pass

    def test_generate_from_jinja2(self):
        pass

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()