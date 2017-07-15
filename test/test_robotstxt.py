#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 by Łukasz Langa
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from requests import Session
from requests_robotstxt import RobotsAwareSession, RobotsTxtDisallowed


class TestRobotsAwareSession(unittest.TestCase):
    def setUp(self):
        self.baseline = Session()
        self.aware = RobotsAwareSession()

    def testRobotAllowed(self):
        self.skipUnless(self.baseline.get('http://www.robotstxt.org/').status_code == 200,
                "Could not connect to test site.")
        self.assertEqual(self.aware.get('http://www.robotstxt.org/'), 200)
        self.assertIn('http://www.robotstxt.org/robots.txt', self.aware.registry)

    def testRobotDisallowed(self):
        self.skipUnless(self.baseline.get('https://www.github.com/').status_code == 200,
                "Could not connect to test site.")
        with self.assertRaises(RobotsTxtDisallowed):
            self.aware.get('https://www.github.com/')
        self.assertIn('http://www.robotstxt.org/robots.txt', self.aware.registry)


if __name__ == '__main__':
    unittest.main()
