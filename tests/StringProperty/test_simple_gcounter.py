#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for gcounter.StringProperty with simple counter

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports

# GAE imports
from google.appengine.ext import ndb
from google.appengine.api import datastore_errors

# Global Counter imports
import gcounter

# Global Counter tests imports
from tests import helper_models
from tests.base_test import TestCountersMain

BadValueError = datastore_errors.BadValueError


class TestStringPropertySimpleCounters(TestCountersMain):
    """Simple global counters tracking string properties should behave in the
        following way:

        For new models:
         - generate +1 counter action only when persisted with tracked value equal to not empty string
         - models persisted with tracked value set to None should not generate any counter actions

        For models that are retrieved from the Datastore:
         - changing tracked value to the same value should not generate any counter actions.
         - changing tracked value from not empty string to any other not empty string should not generate
            counter action.
         - changing tracked value from not empty string to None should generate counter action -1.
         - changing tracked value from None or empty string to not empty string should generate counter action +1.

        Also:
         - Counter actions can be retrieved only when model is persisted and in pristine state.
    """

    def _createSC1(self, sc1='test'):
        """Create and persist model with StringProperty
            with simple counter and default value set to sc1
        """

        model = helper_models.TestSC1(sc1=sc1)
        model.put()
        return model

    def _createSC2(self, sc2=None):
        """Create and persist model with StringProperty
            with simple counter and default value set to None
        """

        model = helper_models.TestSC2(sc2=sc2)
        model.put()
        return model

    def _createSCR1(self, scr1=None):
        """Create and persist model with repeated StringProperty
            with simple counter and default value set to None
        """

        if not scr1:
            scr1 = []

        model = helper_models.TestSCR1(scr1=scr1)
        model.put()
        return model

    def testDefaultSC1(self):

        model = self._createSC1()
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': 1}, ca)

    def testDefaultSC2(self):

        model = self._createSC2()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultSCR1(self):

        model = helper_models.TestSCR1()
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptySCR1(self):

        model = self._createSCR1()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testDefaultToDifferentValueSC1(self):

        model = self._createSC1('test1')
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': 1}, ca)

    def testDefaultToDifferentValueSC2(self):

        model = self._createSC2('test1')
        ca = model.get_counter_actions()
        self.assertEqual({'sc2n': 1}, ca)

    def testDefaultToDifferentValueSCR1(self):

        model = self._createSCR1(['test1', 'test2'])
        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

    def testNoneToDefaultSC1(self):

        model = self._createSC1(None)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        # Change value to default one and persist
        model.sc1 = 'test'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': 1}, ca)

    def testNoneToDefaultSC2(self):

        model = self._createSC2(None)
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        model.sc2 = None
        model.put()

        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyStringSC1(self):

        with self.assertRaises(BadValueError):
            self._createSC1('')

    def testEmptyStringSC2(self):

        with self.assertRaises(BadValueError):
            self._createSC2('')

    def testEmptyArraySCR1(self):

        model = self._createSCR1([])
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToNoneSC1(self):

        model = self._createSC1(None)
        model.sc1 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToNoneSC2(self):

        model = self._createSC2(None)
        model.sc2 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testEmptyToEmptySCR1(self):

        model = self._createSCR1([])
        model.scr1 = []
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testNoneToValueSC1(self):

        model = self._createSC1(None)
        model.sc1 = 'test1'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': 1}, ca)

    def testNoneToValueSC2(self):

        model = self._createSC2(None)
        model.sc2 = 'test1'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc2n': 1}, ca)

    def testEmptyToValueSCR1(self):

        model = self._createSCR1([])
        model.scr1 = ['string']
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

    def testValueToDefaultSC1(self):

        model = self._createSC1('test1')
        model.sc1 = 'test'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testValueToDefaultSC2(self):

        model = self._createSC2('test1')
        model.sc2 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc2n': -1}, ca)

    def testValueToNoneSC1(self):

        model = self._createSC1('test1')
        model.sc1 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': -1}, ca)

    def testValueToNoneSC2(self):

        model = self._createSC2('test1')
        model.sc2 = None
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'sc2n': -1}, ca)

    def testValueToEmptySCR1(self):

        model = self._createSCR1(['string'])
        model.scr1 = []
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': -1}, ca)

    def testValue1ToValue2CS1(self):

        model = self._createSC1('test1')
        model.sc1 = 'test2'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testValue1ToValue2CS2(self):

        model = self._createSC2('test1')
        model.sc2 = 'test2'
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testValueToValueSCR1(self):

        model = self._createSCR1(['string'])
        model.scr1 = ['string', 'string1']
        model.put()
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

    def testGettingCounterActionsBeforePutCS1(self):

        model = self._createSC1()
        model.sc1 = 'test'
        ca = model.get_counter_actions()
        self.assertEqual({'sc1n': 1}, ca)

        model.sc1 = 'test1'
        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutCS2(self):

        model = self._createSC2()
        model.sc2 = None
        ca = model.get_counter_actions()
        self.assertEqual({}, ca)

        model.sc2 = 'test'
        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testGettingCounterActionsBeforePutCSR1(self):

        model = self._createSCR1(['string'])
        model.scr1 = ['string']
        ca = model.get_counter_actions()
        self.assertEqual({'scr1n': 1}, ca)

        model.scr1 = ['test']
        with self.assertRaises(gcounter.ModelTrackingNotSaved):
            model.get_counter_actions()

    def testPutMulti(self):

        key1 = ndb.Key(helper_models.TestSCR1, 1)
        model1 = helper_models.TestSCR1(key=key1)

        key2 = ndb.Key(helper_models.TestSC1, 2)
        model2 = helper_models.TestSC1(key=key2)

        key3 = ndb.Key(helper_models.TestSC2, 3)
        model3 = helper_models.TestSC2(key=key3)

        ndb.put_multi([model1, model2, model3])

        self.assertEqual({}, model1.get_counter_actions())
        self.assertEqual({'sc1n': 1}, model2.get_counter_actions())
        self.assertEqual({}, model3.get_counter_actions())

    def testPutMultiAsync(self):

        key1 = ndb.Key(helper_models.TestSCR1, 1)
        model1 = helper_models.TestSCR1(key=key1)

        key2 = ndb.Key(helper_models.TestSC1, 2)
        model2 = helper_models.TestSC1(key=key2)

        key3 = ndb.Key(helper_models.TestSC2, 3)
        model3 = helper_models.TestSC2(key=key3)

        self.removeNDBCache(key1)
        self.removeNDBCache(key2)
        self.removeNDBCache(key3)
        self.clearContext()

        futures = ndb.put_multi_async([model1, model2, model3])

        for future in futures:
            key = future.get_result()
            model = key.get()

            if key.id() in [1, 3]:
                self.assertEqual({}, model.get_counter_actions())
            if key.id() == 2:
                self.assertEqual({'sc1n': 1}, model.get_counter_actions())

    def testMultipleGetCounterActionsSC1(self):

        model = self._createSC1()

        # We should get counter actions only first call after put()
        self.assertEqual({'sc1n': 1}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())

    def testMultipleGetCounterActionsSCR1(self):

        model = self._createSCR1(['string'])

        # We should get counter actions only first call after put()
        self.assertEqual({'scr1n': 1}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())
        self.assertEqual({}, model.get_counter_actions())

    def testMultipleGetCounterActionsAfterNoOpPutSC1(self):

        model = self._createSC1()
        self.assertEqual({'sc1n': 1}, model.get_counter_actions())

        # NoOp put
        model.put()
        # Call to get_counter_actions after no op put() should return empty dictionary
        self.assertEqual({}, model.get_counter_actions())

        # NoOp put
        # Call to get_counter_actions after no op put() should return empty dictionary
        model.put()
        self.assertEqual({}, model.get_counter_actions())

    def testMultipleGetCounterActionsAfterNoOpPutSCR1(self):

        model = self._createSCR1(['string', 'test'])
        self.assertEqual({'scr1n': 1}, model.get_counter_actions())

        # NoOp put
        model.put()
        # Call to get_counter_actions after no op put() should return empty dictionary
        self.assertEqual({}, model.get_counter_actions())

        # NoOp put
        # Call to get_counter_actions after no op put() should return empty dictionary
        model.put()
        self.assertEqual({}, model.get_counter_actions())
