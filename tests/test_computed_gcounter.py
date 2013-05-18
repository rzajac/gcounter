#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for dependent counters

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


class TestComputedCounters(TestCountersMain):

    def _createCP1(self, name=None):

        model = helper_models.TestCP1()
        model.name = name
        model.put()
        return model

    def _createCP2(self, my_value=None):

        model = helper_models.TestCP2()
        model.my_value = my_value
        model.put()
        return model

    def testDefaultCP1(self):

        model = self._createCP1()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultCP2(self):

        model = self._createCP2()

        ca = model.get_counter_actions()
        self.assertEqual({'cp2n': 1}, ca)

    def testStringCP1(self):

        model = self._createCP1(name='Rafal')

        ca = model.get_counter_actions()
        self.assertEqual({'cp1n': 1}, ca)

    def testStringCP2(self):

        model = self._createCP2(my_value='Rafal')

        ca = model.get_counter_actions()
        self.assertEqual({'cp2n': 1}, ca)

    def testEmptyStringCP1(self):

        model = self._createCP1(name='')

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyStringCP2(self):

        model = self._createCP2(my_value='')

        ca = model.get_counter_actions()
        self.assertEqual({'cp2n': 1}, ca)

    def testEditStringCP2(self):

        model = self._createCP2()

        model.my_value = 'string'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)
