#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for gcounter.BooleanProperty

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


class TestBooleanCounters(TestCountersMain):
    """Global counters tracking boolean properties should behave in the
        following way:

        For new models:
         - generate +1 counter action only when persisted with tracked value set to True
         - models persisted with tracked value set to False or None should not generate
           any counter actions.

        For models that are retrieved from the Datastore:
         - changing tracked value to the same value should not generate any counter actions.
         - changing tracked value from True to False or None should generate counter action -1.
         - changing tracked value from False or None to True should generate counter action +1.

        Also:
         - Counter actions can be retrieved only when model is persisted and in pristine state.
         - Accessing counter actions when model is not in pristine state should
           throw gcounter.ModelTrackingNotSaved exception.
    """

    def _createBC1(self, bc1=None):
        """Create and persist model with BooleanProperty
            with simple counter and default value set to None"""

        model = helper_models.TestBC1()
        model.bc1 = bc1
        model.put()
        return model

    def _createBC2(self, bc2=False):
        """Create and persist model with BooleanProperty
            with simple counter and default value set to False"""
        model = helper_models.TestBC2()
        model.bc2 = bc2
        model.put()
        return model

    def _createBC3(self, bc3=True):
        """Create and persist model with BooleanProperty
            with simple counter and default value set to True"""
        model = helper_models.TestBC3()
        model.bc3 = bc3
        model.put()
        return model

    def testDefaultBC1(self):

        model = self._createBC1()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultBC2(self):

        model = self._createBC2()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultBC3(self):

        model = self._createBC3()
        ca = model.get_counter_actions()
        self.assertEqual({'bc3n': 1}, ca)

    def testFalseBC1(self):

        model = self._createBC1(bc1=False)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testFalseBC2(self):

        model = self._createBC2(bc2=False)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testFalseBC3(self):

        model = self._createBC3(bc3=False)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testTrueBC1(self):

        model = self._createBC1(bc1=True)
        ca = model.get_counter_actions()
        self.assertEqual({'bc1n': 1}, ca)

    def testTrueBC2(self):

        model = self._createBC2(bc2=True)
        ca = model.get_counter_actions()
        self.assertEqual({'bc2n': 1}, ca)

    def testTrueBC3(self):

        model = self._createBC3(bc3=True)
        ca = model.get_counter_actions()
        self.assertEqual({'bc3n': 1}, ca)

    def testChangeDefaultToTrueBC1(self):

        model = self._createBC1()
        model.bc1 = True
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'bc1n': 1}, ca)

    def testChangeDefaultToTrueBC2(self):

        model = self._createBC2()
        model.bc2 = True
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'bc2n': 1}, ca)

    def testChangeDefaultToTrueBC3(self):

        model = self._createBC3()
        model.bc3 = True
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToFalseBC1(self):

        model = self._createBC1()
        model.bc1 = False
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToFalseBC2(self):

        model = self._createBC2()
        model.bc2 = False
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToFalseBC3(self):

        model = self._createBC3()
        model.bc3 = False
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'bc3n': -1}, ca)

    def testChangeDefaultToNoneBC1(self):

        model = self._createBC1()
        model.bc1 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToNoneBC2(self):

        model = self._createBC2()
        model.bc2 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testChangeDefaultToNoneBC3(self):

        model = self._createBC3()
        model.bc3 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'bc3n': -1}, ca)

    def testGettingCounterActionsBeforePutBC1(self):

        model = self._createBC1()
        model.bc1 = None
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Changing tracked value from None to False
        model.bc1 = False

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutBC2(self):

        model = self._createBC2()
        model.bc2 = False
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Changing tracked value from False to True
        model.bc2 = True

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutBC3(self):

        model = self._createBC3()
        model.bc3 = True
        ca = model.get_counter_actions()
        self.assertEqual({'bc3n': 1}, ca)

        # Changing tracked value from True to False
        model.bc3 = False

        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testPutMulti(self):

        key1 = ndb.Key(helper_models.TestBC1, 1)
        model1 = helper_models.TestBC1(key=key1)

        key2 = ndb.Key(helper_models.TestBC2, 2)
        model2 = helper_models.TestBC2(key=key2)

        key3 = ndb.Key(helper_models.TestBC3, 3)
        model3 = helper_models.TestBC3(key=key3)

        ndb.put_multi([model1, model2, model3])

        self.assertEqual({}, model1.get_counter_actions())
        self.assertEqual({}, model2.get_counter_actions())
        self.assertEqual({'bc3n': 1}, model3.get_counter_actions())

    def testPutAsync(self):

        key1 = ndb.Key(helper_models.TestBC1, 1)
        model1 = helper_models.TestBC1(key=key1)

        key2 = ndb.Key(helper_models.TestBC2, 2)
        model2 = helper_models.TestBC2(key=key2)

        key3 = ndb.Key(helper_models.TestBC3, 3)
        model3 = helper_models.TestBC3(key=key3)

        self.removeNDBCache(key1)
        self.removeNDBCache(key2)
        self.removeNDBCache(key3)
        self.clearContext()

        futures = ndb.put_multi_async([model1, model2, model3])

        for future in futures:
            key = future.get_result()
            model = key.get()

            if key.id() in [1, 2]:
                self.assertEqual({}, model.get_counter_actions())
            if key.id() == 3:
                self.assertEqual({'bc3n': 1}, model.get_counter_actions())

    def testMultipleGetCounterActions(self):

        model = self._createBC3()

        # We should get counter actions only first call after put()
        self.assertEqual({'bc3n': 1}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())

    def testMultipleGetCounterActionsAfterOnOpPut(self):

        model = self._createBC3()
        self.assertEqual({'bc3n': 1}, model.get_counter_actions())

        # NoOp put
        model.put()
        # Call to get_counter_actions after no op put() should return empty dictionary
        self.assertEqual({}, model.get_counter_actions())

        # NoOp put
        # Call to get_counter_actions after no op put() should return empty dictionary
        model.put()
        self.assertEqual({}, model.get_counter_actions())
