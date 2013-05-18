#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base test class that all other test cases extend

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

from __future__ import with_statement

# Python imports

# GAE imports
from google.appengine.ext import ndb
from google.appengine.api import memcache

# Global Counter imports
import gcounter

# Global Counter tests imports
from tests.teststarter import BaseTestCase


class TestCountersMain(BaseTestCase):

    def setUp(self):
        self.setup_testbed()
        self.init_datastore_stub()
        self.init_memcache_stub()

    def tearDown(self):
        self.teardown_testbed()

    def clearContext(self):
        context = ndb.get_context()
        context.clear_cache()
        context.flush()
        memcache.flush_all()

    def run_aggr_counters(self):
        """Run aggregate counters task"""

        response = self.get('/admin/scr/aggregate-counters')
        self.assertOK(response)

        # There should be only one task in the queue
        self.assertEqual(1, len(self.get_tasks()))

        # Execute all counter tasks
        self.execute_tasks_until_empty()

    def get_db_counters(self):
        """Get all the counters from the datasore, sum them and return as dictionary"""

        # Get all counters
        counters = gcounter.GeneralCounterShard.query()
        counters_db = {}

        # Sum all counters
        for counter in counters:
            self.inc_counter(counters_db, counter.name, counter.count)

        return counters_db

    def inc_counter(self, counters, name, delta):
        """Increase counter value with name by delta"""
        counters[name] = counters.get(name, 0) + delta

    def compare_counters(self, counters1, counters2):
        """Compare counter values between the ones calculated in tests and the ones from RadioDB"""

        for counter_name in counters1.keys():
            test_counter = counters1[counter_name]
            rdb_counter = counters2[counter_name]
            self.assertEqual(test_counter, rdb_counter, 'Error for counter %s %s != %s' % (counter_name, str(test_counter), str(rdb_counter)))

        # Make sure counters have the same keys
        self.assertEqual([], list(set(counters1.keys()) - set(counters2.keys())))
        self.assertEqual([], list(set(counters2.keys()) - set(counters1.keys())))
