#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for gcounter.py

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports

# GAE imports

# Global Counter imports
import gcounter

# Global Counter tests imports
from tests.base_test import TestCountersMain


class TestCounter(TestCountersMain):

    def testAggregate(self):

        aggr = [
            {'c1': 1},
            {'c1': 2},
            {'c2': 3},
            {'c3': 1}
        ]

        ca = gcounter.Counter.aggregate_counters(aggr)

        self.assertEqual({'c3': 1, 'c2': 3, 'c1': 3}, ca)

    def testAggregateZero(self):

        aggr = [
            {'c1': 1},
            {'c1': -1},
        ]

        ca = gcounter.Counter.aggregate_counters(aggr)
        self.assertEqual({}, ca)

    def testAddDelta(self):

        c = {'c1': 1}
        gcounter.Counter.add_delta(c, 'c1', 1)
        self.assertEqual({'c1': 2}, c)

    def testAddDeltaNew(self):

        c = {}
        gcounter.Counter.add_delta(c, 'c1', 1)
        self.assertEqual({'c1': 1}, c)

    def testAddDeltaMinus(self):

        c = {'c1': 1}
        gcounter.Counter.add_delta(c, 'c1', -2)
        self.assertEqual({'c1': -1}, c)

    def testGetCounterEmpty(self):

        c = gcounter.Counter.get_count('test')
        self.assertEqual(0, c)

    def testGetCounterIncr(self):

        gcounter.Counter.incr('test')
        c = gcounter.Counter.get_count('test')
        self.assertEqual(1, c)

    def testGetCounterDecr(self):

        gcounter.Counter.decr('test')
        c = gcounter.Counter.get_count('test')
        self.assertEqual(-1, c)

    def testGetCounterChange(self):

        gcounter.Counter.incr('test')
        gcounter.Counter.change_counter('test', 10)
        c = gcounter.Counter.get_count('test')
        self.assertEqual(11, c)

    def testGetCounterChangeMinus(self):

        gcounter.Counter.incr('test')
        gcounter.Counter.change_counter('test', -10)
        c = gcounter.Counter.get_count('test')
        self.assertEqual(-9, c)
