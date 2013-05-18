#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for repeated gcounter.StringProperty

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


class TestSimpleRepeatedCounter(TestCountersMain):
    """Simple global repeated counter works the same as simple global counter.
        Here we test only cases that are specific to arrays"""

    def _createSCR1(self, scr1=None):
        model = helper_models.TestSCR1()

        if scr1 is not None:
            model.scr1 = scr1

        model.put()
        return model

    def testNone(self):

        with self.assertRaises(BadValueError):
            helper_models.TestSCR1(scr1=None)

    def testEmptyToEmpty(self):
        model = self._createSCR1([])
        model.scr1 = []

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyToNone(self):
        model = self._createSCR1([])

        with self.assertRaises(BadValueError):
            model.scr1 = None

    def testDefaultToValue(self):

        model = self._createSCR1(['a'])

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

    def testDefaultToValue2(self):

        model = self._createSCR1(['a', 'b'])
        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

    def testValueToEmpty(self):

        model = self._createSCR1(['a', 'b'])
        model.scr1 = []
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': -1}, ca)

    def testValueToValue(self):

        model = self._createSCR1(['a', 'b'])
        model.scr1 = ['c', 'd']
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testListShorter(self):

        model = self._createSCR1(['a', 'b'])
        model.scr1 = ['a']
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testListShorterDifferent(self):

        model = self._createSCR1(['a', 'b'])
        model.scr1 = ['c']
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    # Append tests

    def testAppend(self):

        model = helper_models.TestSCR1()
        model.scr1.append('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

    def testAppendTwice(self):

        model = helper_models.TestSCR1()
        model.scr1.append('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

        model.scr1.append('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testAppendToNotEmpty(self):

        model = self._createSCR1(['a'])
        model.scr1.append('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    # Remove tests

    def testRemove(self):

        model = self._createSCR1(['a'])
        model.scr1.remove('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': -1}, ca)

    def testRemoveTwice(self):

        model = self._createSCR1(['a'])
        model.scr1.remove('a')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': -1}, ca)

        model.scr1 = []

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testRemoveAll(self):

        model = self._createSCR1(['a', 'b'])
        model.scr1.remove('a')
        model.scr1.remove('b')
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': -1}, ca)
