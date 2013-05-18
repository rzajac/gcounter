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


class TestDependentCounters(TestCountersMain):

    def _createDC1(self, co=None, reg=None, ci=None):

        model = helper_models.TestDC1()
        model.co = co
        model.reg = reg
        model.ci = ci
        model.put()
        return model

    def testNone(self):

        model = self._createDC1()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testCountry(self):

        model = self._createDC1(co='us')
        ca = model.get_counter_actions()
        self.assertEqual({'loc:us': 1}, ca)

    def testCountryRegion(self):

        model = self._createDC1(co='us', reg='ca')
        ca = model.get_counter_actions()
        self.assertEqual({'loc:us': 1, 'loc:us:ca': 1}, ca)

    def testCountryRegionCity(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        ca = model.get_counter_actions()
        self.assertEqual({'loc:us': 1, 'loc:us:ca': 1, 'loc:us:ca:costa-mesa': 1}, ca)

    def testChangeCity(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.ci = 'Newport Beach'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca:costa-mesa': -1, 'loc:us:ca:newport-beach': 1}, ca)

    def testChangeRegion(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.reg = 'nv'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca': -1, 'loc:us:nv': 1, 'loc:us:ca:costa-mesa': -1, 'loc:us:nv:costa-mesa': 1}, ca)

    def testChangeCountry(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = 'pl'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl': 1, 'loc:pl:ca:costa-mesa': 1, 'loc:pl:ca': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1, 'loc:us:ca': -1}, ca)

    def testChangeCountryRegion(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = 'pl'
        model.reg = 'nv'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl': 1, 'loc:us:ca:costa-mesa': -1, 'loc:us': -1, 'loc:pl:nv:costa-mesa': 1, 'loc:us:ca': -1, 'loc:pl:nv': 1}, ca)

    def testChangeCountryRegionCity(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = 'pl'
        model.reg = 'nv'
        model.ci = 'Berlin'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl': 1, 'loc:pl:nv:berlin': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1, 'loc:us:ca': -1, 'loc:pl:nv': 1}, ca)

    # Test partials

    def testPartialNoCity(self):

        model = self._createDC1(co='us', reg='ca', ci=None)

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us': 1, 'loc:us:ca': 1}, ca)

    def testPartialNoRegion(self):

        model = self._createDC1(co='us', reg=None, ci='Costa Mesa')

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us': 1, 'loc:us::costa-mesa': 1}, ca)

    def testPartialNoCountry(self):

        model = self._createDC1(co=None, reg='ca', ci='Costa Mesa')

        ca = model.get_counter_actions()
        self.assertEqual({'loc::ca:costa-mesa': 1, 'loc::ca': 1}, ca)

    def testPartialChangeNoRegion(self):

        model = self._createDC1(co='us', reg=None, ci='Costa Mesa')
        model.co = 'pl'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl': 1, 'loc:pl::costa-mesa': 1, 'loc:us': -1, 'loc:us::costa-mesa': -1}, ca)

    def testPartialChangeNoRegion2(self):

        model = self._createDC1(co='us', reg=None, ci='Costa Mesa')
        model.ci = 'New York'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us::new-york': 1, 'loc:us::costa-mesa': -1}, ca)

    def testPartialChangeNoRegion3(self):

        model = self._createDC1(co='us', reg=None, ci='Costa Mesa')
        model.co = 'pl'
        model.ci = 'New York'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl': 1, 'loc:pl::new-york': 1, 'loc:us::costa-mesa': -1, 'loc:us': -1}, ca)

    def testPartialChangeNoCity(self):

        model = self._createDC1(co='us', reg='ca', ci=None)
        model.co = 'pl'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl:ca': 1, 'loc:pl': 1, 'loc:us': -1, 'loc:us:ca': -1}, ca)

    def testPartialChangeNoCity2(self):

        model = self._createDC1(co='us', reg='ca', ci=None)
        model.reg = 'nv'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:nv': 1, 'loc:us:ca': -1}, ca)

    def testPartialChangeNoCity3(self):

        model = self._createDC1(co='us', reg='ca', ci=None)
        model.co = 'pl'
        model.reg = 'nv'
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:pl:nv': 1, 'loc:pl': 1, 'loc:us': -1, 'loc:us:ca': -1}, ca)

    def testToNoneCity(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.ci = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca:costa-mesa': -1}, ca)

    def testToNoneRegion(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.reg = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca': -1, 'loc:us::costa-mesa': 1, 'loc:us:ca:costa-mesa': -1}, ca)

    def testToNoneCountry(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc::ca': 1, 'loc:us:ca': -1, 'loc::ca:costa-mesa': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1}, ca)

    def testToNoneCountryCity(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = None
        model.ci = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca': -1, 'loc::ca': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1}, ca)

    def testToNoneCountryRegion(self):

        model = self._createDC1(co='us', reg='ca', ci='Costa Mesa')
        model.co = None
        model.reg = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({'loc:us:ca': -1, 'loc:::costa-mesa': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1}, ca)
