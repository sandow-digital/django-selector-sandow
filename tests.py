#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for django-selector."""

import unittest
import re
import calendar

import dselector

class DselectorTest(unittest.TestCase):
    def test_default_patterns(self):
        """Test the default {foo} parser."""
        parser = dselector.Parser()
        pat = re.compile(parser.parse_pattern('/archives/{year}/{month}'))
        match = pat.match('/archives/2005/04')
        self.failUnless(match)
        self.failUnless(match.groupdict()['year'] == '2005')
        self.failUnless(match.groupdict()['month'] == '04')
        match = pat.match('/archives/twothousandfive/ohfour')
        self.failUnless(match)
        self.failUnless(match.groupdict()['year'] == 'twothousandfive')
        self.failUnless(match.groupdict()['month'] == 'ohfour')
        match = pat.match('/archives/foo.bar/baz.bif!@#$%')
        self.failUnless(match)
        self.failUnless(match.groupdict()['year'] == 'foo.bar')
        self.failUnless(match.groupdict()['month'] == 'baz.bif!@#$%')

    def test_pattern_parser(self):
        """Some simple tests that show the parsers will match the expected
        URLs and fail on the unexpected ones."""
        parser = dselector.Parser()
        pat = re.compile(parser.parse_pattern('/archives/{year:digits}/{month:digits}'))
        match = pat.match('/archives/2005/04')
        self.failUnless(match)
        self.failUnless(match.groupdict()['year'] == '2005')
        self.failUnless(match.groupdict()['month'] == '04')
        pat = re.compile(parser.parse_pattern('/archives/{year:year}/{month:month}'))
        match = pat.match('/archives/2005/04')
        self.failUnless(not match) # month is 
        match = pat.match('/archives/2005/%s' % calendar.month_abbr[3])
        self.failUnless(match)
        self.failUnless(match.groupdict()['year'] == '2005')
        self.failUnless(match.groupdict()['month'] == calendar.month_abbr[3])




