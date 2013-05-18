#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for repeated gcounter.StringProperty with complex counter

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


class TestRepeatedComplexCounters(TestCountersMain):
    """Repeated complex global counter works the same as simple global counter.
        Here we test only cases that are specific to arrays"""

    def _createCCR1(self, ccr1):

        model = helper_models.TestCCR1()
        model.ccr1 = ccr1
        model.put()
        return model

    def testNoneCCR1(self):

        with self.assertRaises(BadValueError):
            self._createCCR1(None)

    def testEmptyCCR1(self):

        model = self._createCCR1([])
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyToEmptyCCR1(self):

        self._createCCR1([])

        model = helper_models.TestCCR1()
        model.ccr1 = []
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyToNoneCCR1(self):

        model = self._createCCR1([])

        with self.assertRaises(BadValueError):
            model.ccr1 = None

    def testNoneToValueCCR1(self):

        model = self._createCCR1(['a'])

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': 1}, ca)

    def testDefaultToValue2CCR1(self):

        model = self._createCCR1(['a', 'b'])

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': 1, 'ccr1n:b': 1}, ca)

    def testValueToEmptyCCR1(self):

        model = self._createCCR1(['a', 'b'])
        model.ccr1 = []
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': -1, 'ccr1n:b': -1}, ca)

    def testValueToValueCCR1(self):

        model = self._createCCR1(['a', 'b'])
        model.ccr1 = ['c', 'd']
        model.put()

        ca = model.get_counter_actions()

        self.assertEqual({'ccr1n:c': 1, 'ccr1n:b': -1, 'ccr1n:a': -1, 'ccr1n:d': 1}, ca)

    def testListShorterCCR1(self):

        model = self._createCCR1(['a', 'b'])
        model.ccr1 = ['a']
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:b': -1}, ca)

    def testListShorterDifferentCCR1(self):

        model = self._createCCR1(['a', 'b'])
        model.ccr1 = ['c']
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:c': 1, 'ccr1n:b': -1, 'ccr1n:a': -1}, ca)

    def testAddMultipleSameValuesCCR1(self):

        model = self._createCCR1(['a', 'a'])

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': 1}, ca)

    # Append tests

    def testAppendCCR1(self):

        model = helper_models.TestCCR1()
        model.ccr1.append('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': 1}, ca)

    def testAppendTwiceCCR1(self):

        model = helper_models.TestCCR1()
        model.ccr1.append('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': 1}, ca)

        model.ccr1.append('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:b': 1}, ca)

    def testAppendToNotEmptyCCR1(self):

        model = self._createCCR1(['a'])
        model.ccr1.append('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:b': 1}, ca)

    def testAppendSameValueCCR1(self):

        model = self._createCCR1(['a'])
        model.ccr1.append('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    # Remove tests

    def testRemoveCCR1(self):

        model = self._createCCR1(['a'])
        model.ccr1.remove('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': -1}, ca)

    def testRemoveTwiceCCR1(self):

        model = self._createCCR1(['a'])
        model.ccr1.remove('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:a': -1}, ca)

        model.ccr1 = []

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testRemoveAllCCR1(self):

        model = self._createCCR1(['a', 'b'])
        model.ccr1.remove('a')
        model.ccr1.remove('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'ccr1n:b': -1, 'ccr1n:a': -1}, ca)
