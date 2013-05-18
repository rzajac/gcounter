#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for gcounter.IntegerProperty

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports

# GAE imports
from google.appengine.ext import ndb

# Global Counter imports
import gcounter

# Global Counter tests imports
from tests import helper_models
from tests.base_test import TestCountersMain


class TestIntegerCounters(TestCountersMain):
    """Global counters tracking integer properties should behave in the following way:

        For new models:
         - generate +1 counter action only when persisted with tracked value greater then 0
         - models persisted with tracked value set to 0 or less should not generate
           any counter actions.

        For models that are retrieved from the Datastore:
         - changing tracked value to the same value should not generate any counter actions.
         - changing tracked value from positive value to 0 or less should generate counter action -1.
         - changing tracked value from 0 or less to positive value should generate counter action +1.

        Also:
         - Counter actions can be retrieved only when model is persisted and in pristine state.
         - Accessing counter actions when model is not in pristine state should
           throw gcounter.ModelTrackingNotSaved exception.
    """

    def _createIC1(self, ic1=None):
        """Create and persist model with IntegerProperty
            with simple counter and default value set to None
        """
        model = helper_models.TestIC1()
        model.ic1 = ic1
        model.put()
        return model

    def _createIC2(self, ic2=-1):
        """Create and persist model with IntegerProperty
            with simple counter and default value set to -1
        """
        model = helper_models.TestIC2()
        model.ic2 = ic2
        model.put()
        return model

    def _createIC3(self, ic3=1):
        """Create and persist model with IntegerProperty
            with simple counter and default value set to 1
        """
        model = helper_models.TestIC3()
        model.ic3 = ic3
        model.put()
        return model

    def _createIC4(self, ic4=0):
        """Create and persist model with IntegerProperty
            with simple counter and default value set to 0
        """
        model = helper_models.TestIC4()
        model.ic4 = ic4
        model.put()
        return model

    def testDefaultIC1(self):

        # IntegerProperty with default value set to None should not count
        model = self._createIC1()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultIC2(self):

        # IntegerProperty with default value set to -1 should not count
        model = self._createIC2()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultIC3(self):

        # IntegerProperty with default value set to 1 should count
        model = self._createIC3()
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': 1}, ca)

    def testDefaultIC4(self):

        # IntegerProperty with default value set to 0 should not count
        model = self._createIC4()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testMinusOneIC1(self):

        model = self._createIC1(ic1=-1)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testMinusOneIC2(self):

        model = self._createIC2(ic2=-1)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testMinusOneIC3(self):

        model = self._createIC3(ic3=-1)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testMinusOneIC4(self):

        model = self._createIC4(ic4=-1)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testZeroIC1(self):

        model = self._createIC1(ic1=0)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testZeroIC2(self):

        model = self._createIC2(ic2=0)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testZeroIC3(self):

        model = self._createIC3(ic3=0)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testZeroIC4(self):

        model = self._createIC4(ic4=0)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testPlusOneIC1(self):

        model = self._createIC1(ic1=1)
        ca = model.get_counter_actions()
        self.assertEqual({'ic1n': 1}, ca)

    def testPlusOneIC2(self):

        model = self._createIC2(ic2=1)
        ca = model.get_counter_actions()
        self.assertEqual({'ic2n': 1}, ca)

    def testPlusOneIC3(self):

        model = self._createIC3(ic3=1)
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': 1}, ca)

    def testPlusOneIC4(self):

        model = self._createIC4(ic4=1)
        ca = model.get_counter_actions()
        self.assertEqual({'ic4n': 1}, ca)

    def testChangeDefaultToOneIC1(self):

        model = self._createIC1()
        model.ic1 = 1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic1n': 1}, ca)

    def testChangeDefaultToOneIC2(self):

        model = self._createIC2()
        model.ic2 = 1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic2n': 1}, ca)

    def testChangeDefaultToOneIC3(self):

        model = self._createIC3()
        model.ic3 = 1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToOneIC4(self):

        model = self._createIC4()
        model.ic4 = 1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic4n': 1}, ca)

    def testChangeDefaultToMoreThenOneIC1(self):

        model = self._createIC1()
        model.ic1 = 345
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic1n': 1}, ca)

    def testChangeDefaultToMoreThenOneIC2(self):

        model = self._createIC2()
        model.ic2 = 345
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic2n': 1}, ca)

    def testChangeDefaultToMoreThenOneIC3(self):

        model = self._createIC3()
        model.ic3 = 345
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToMoreThenOneIC4(self):
        model = self._createIC4()
        model.ic4 = 345
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic4n': 1}, ca)

    def testChangeDefaultToMinusOneIC1(self):

        model = self._createIC1()
        model.ic1 = -1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToMinusOneIC2(self):

        model = self._createIC2()
        model.ic2 = -1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToMinusOneIC3(self):

        model = self._createIC3()
        model.ic3 = -1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': -1}, ca)

    def testChangeDefaultToMinusOneIC4(self):

        model = self._createIC4()
        model.ic4 = -1
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToZeroIC1(self):

        model = self._createIC1()
        model.ic1 = 0
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToZeroIC2(self):

        model = self._createIC2()
        model.ic2 = 0
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToZeroIC3(self):

        model = self._createIC3()
        model.ic3 = 0
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': -1}, ca)

    def testChangeDefaultToZeroIC4(self):

        model = self._createIC4()
        model.ic4 = 0
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToNoneIC1(self):

        model = self._createIC1()
        model.ic1 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToNoneIC2(self):

        model = self._createIC2()
        model.ic2 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToNoneIC3(self):

        model = self._createIC3()
        model.ic3 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': -1}, ca)

    def testChangeDefaultToNoneIC4(self):

        model = self._createIC4()
        model.ic4 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testGettingCounterActionsBeforePutIC1(self):

        model = self._createIC1()
        model.ic1 = None
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Changing tracked value from None to 1
        model.ic1 = 1

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutIC2(self):

        model = self._createIC2()
        model.ic2 = -1
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Changing tracked value from -1 to 1
        model.ic2 = 1

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutIC3(self):

        model = self._createIC3()
        model.ic3 = 1
        ca = model.get_counter_actions()
        self.assertEqual({'ic3n': 1}, ca)

        # Changing tracked value from 1 to something else
        model.ic3 = 23

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutIC4(self):

        model = self._createIC4()
        model.ic4 = 0
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Changing tracked value from 0 to something else
        model.ic4 = 23

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testPutMulti(self):

        key1 = ndb.Key(helper_models.TestIC1, 1)
        model1 = helper_models.TestIC1(key=key1)

        key2 = ndb.Key(helper_models.TestIC2, 2)
        model2 = helper_models.TestIC2(key=key2)

        key3 = ndb.Key(helper_models.TestIC3, 3)
        model3 = helper_models.TestIC3(key=key3)

        key4 = ndb.Key(helper_models.TestIC4, 4)
        model4 = helper_models.TestIC4(key=key4)

        ndb.put_multi([model1, model2, model3, model4])

        self.assertEqual({}, model1.get_counter_actions())
        self.assertEqual({}, model2.get_counter_actions())
        self.assertEqual({'ic3n': 1}, model3.get_counter_actions())
        self.assertEqual({}, model4.get_counter_actions())

    def testPutAsync(self):

        key1 = ndb.Key(helper_models.TestIC1, 1)
        model1 = helper_models.TestIC1(key=key1)

        key2 = ndb.Key(helper_models.TestIC2, 2)
        model2 = helper_models.TestIC2(key=key2)

        key3 = ndb.Key(helper_models.TestIC3, 3)
        model3 = helper_models.TestIC3(key=key3)

        key4 = ndb.Key(helper_models.TestIC4, 4)
        model4 = helper_models.TestIC4(key=key4)

        self.removeNDBCache(key1)
        self.removeNDBCache(key2)
        self.removeNDBCache(key3)
        self.removeNDBCache(key4)
        self.clearContext()

        futures = ndb.put_multi_async([model1, model2, model3, model4])

        for future in futures:
            key = future.get_result()
            model = key.get()

            if key.id() in [1, 2, 4]:
                self.assertEqual({}, model.get_counter_actions())
            if key.id() == 3:
                self.assertEqual({'ic3n': 1}, model.get_counter_actions())

    def testMultipleGetCounterActions(self):

        model = self._createIC3()

        # We should get counter actions only first call after put()
        self.assertEqual({'ic3n': 1}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())

    def testMultipleGetCounterActionsAfterNoOpPut(self):

        model = self._createIC3()
        self.assertEqual({'ic3n': 1}, model.get_counter_actions())

        # NoOp put
        model.put()
        # Call to get_counter_actions after no op put() should return empty dictionary
        self.assertEqual({}, model.get_counter_actions())

        # NoOp put
        # Call to get_counter_actions after no op put() should return empty dictionary
        model.put()
        self.assertEqual({}, model.get_counter_actions())
