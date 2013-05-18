#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for gcounter.StringProperty with complex counter

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports

# GAE imports
from google.appengine.api import datastore_errors

# Global Counter imports

# Global Counter tests imports
from tests import helper_models
from tests.base_test import TestCountersMain

BadValueError = datastore_errors.BadValueError


class TestComplexCounters(TestCountersMain):
    """Complex global counters work the same as simple counters. The only difference is
        the counter name is constructed in a different way. We test counter name creation.
    """

    def _createCC1(self, cc1):

        model = helper_models.TestCC1()
        model.cc1 = cc1
        model.put()
        return model

    def _createCC2(self, cc2):

        model = helper_models.TestCC2()
        model.cc2 = cc2
        model.put()
        return model

    def testDefaultToDefaultCC1(self):

        model = self._createCC1('test')
        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test': 1}, ca)

    def testDefaultToDefaultCC2(self):

        model = self._createCC2(None)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultToNoneCC1(self):

        model = self._createCC1(None)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultToValueCC1(self):

        model = self._createCC1('test1')
        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test1': 1}, ca)

    def testDefaultToValueCC2(self):

        model = self._createCC2('test1')
        ca = model.get_counter_actions()
        self.assertEqual({'cc2n:test1': 1}, ca)

    def testNoneToDefaultCC1(self):

        model = self._createCC1(None)
        model.cc1 = 'test'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test': 1}, ca)

    def testNoneToDefaultCC2(self):

        model = self._createCC2(None)
        model.cc2 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToNoneCC1(self):

        model = self._createCC1(None)
        model.cc1 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToNoneCC2(self):

        model = self._createCC2(None)
        model.cc2 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToValueCC1(self):

        model = self._createCC1(None)
        model.cc1 = 'test1'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test1': 1}, ca)

    def testNoneToValueCC2(self):

        model = self._createCC2(None)
        model.cc2 = 'test1'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc2n:test1': 1}, ca)

    def testValueToDefaultCC1(self):

        model = self._createCC1('test1')
        model.cc1 = 'test'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test1': -1, 'cc1n:test': 1}, ca)

    def testValueToDefaultCC2(self):

        model = self._createCC2('test1')
        model.cc2 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc2n:test1': -1}, ca)

    def testValueToNoneCC1(self):

        model = self._createCC1('test1')
        model.cc1 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test1': -1}, ca)

    def testValueToNoneCC2(self):

        model = self._createCC2('test1')
        model.cc2 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc2n:test1': -1}, ca)

    def testValue1ToValue2CC1(self):

        model = self._createCC1('test1')
        model.cc1 = 'test2'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc1n:test1': -1, 'cc1n:test2': 1}, ca)

    def testValue1ToValue2CC2(self):

        model = self._createCC2('test1')
        model.cc2 = 'test2'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'cc2n:test2': 1, 'cc2n:test1': -1}, ca)

    def testCounterNameCreationCC1(self):

        values = {
            'aaa': 'aaa',
            'A a a': 'a-a-a',
            'aa aa': 'aa-aa',
            'a^*a A': 'aa-a',
            'a/-@a': 'a-a'
        }

        for val, exp in values.items():
            model = helper_models.TestCC1()
            model.cc1 = val
            model.put()

            ca = model.get_counter_actions()
            self.assertEqual(1, ca.get('cc1n:' + exp, None))

    def testCounterNameCreationCC2(self):

        values = {
            'aaa': 'aaa',
            'A a a': 'a-a-a',
            'aa aa': 'aa-aa',
            'a^*a A': 'aa-a',
            'a/-@a': 'a-a'
        }

        for val, exp in values.items():
            model = helper_models.TestCC2()
            model.cc2 = val
            model.put()

            ca = model.get_counter_actions()
            self.assertEqual(1, ca.get('cc2n:' + exp, None))
