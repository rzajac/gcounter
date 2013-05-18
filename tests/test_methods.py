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
from google.appengine.ext import ndb

# Global Counter imports
import gcounter

# Global Counter tests imports
from tests import helper_models
from tests.base_test import TestCountersMain


class TestMethods(TestCountersMain):

    def setUp(self):
        super(TestMethods, self).setUp()
        gcounter.DEBUG = False

    def dtestInit(self):

        print '\n------------------------------------------------------1'
        gcounter.DEBUG = True
        helper_models.TestModel()
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False

    def dtestInitWithParams(self):

        print '\n------------------------------------------------------2'
        gcounter.DEBUG = True
        helper_models.TestModel(ic1=123)
        # m __setattr__ _values {}
        # __init__ () {'ic1': 123}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False

    def dtestPutNewModel(self):

        model = helper_models.TestModel()
        print '\n------------------------------------------------------3'
        gcounter.DEBUG = True
        model.put()
        # put
        # m __setattr__ _key Key('TestModel', None)
        # m __setattr__ _entity_key Key('TestModel', None)
        # _pre_put_hook
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # _post_put_hook
        # m __setattr__ _is_new False
        # m __setattr__ _is_dirty False

    def dtestPutNewModelWithKey(self):

        gcounter.DEBUG = True
        print '\n------------------------------------------------------4'
        key = ndb.Key(helper_models.TestModel, 1)
        print '\n------------------------------------------------------5'
        model = helper_models.TestModel(key=key)
        print '\n------------------------------------------------------6'
        model.put()
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _values {}
        # __init__ () {'key': Key('TestModel', 1)}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # put
        # _pre_put_hook
        # _post_put_hook
        # m __setattr__ _is_new False
        # m __setattr__ _is_dirty False

    def dtestPutNotNewModel(self):

        model = helper_models.TestModel()
        model.put()
        self.removeNDBCache(model.key)
        self.clearContext()

        gcounter.DEBUG = True
        print '\n------------------------------------------------------7'
        model.ic1 = 345
        print '\n------------------------------------------------------8'
        model.put()
        # put
        # _pre_put_hook
        # _post_put_hook
        # m __setattr__ _is_new False
        # m __setattr__ _is_dirty False

    def dtestPutNotNewModelWithContext(self):
        model = helper_models.TestModel()
        model.put()

        gcounter.DEBUG = True
        print '\n------------------------------------------------------9'
        model.ic1 = 345
        print '\n------------------------------------------------------10'
        model.put()
        # put
        # _pre_put_hook
        # _post_put_hook
        # m __setattr__ _is_new False
        # m __setattr__ _is_dirty False

    def dtestGetByKey(self):

        key = ndb.Key(helper_models.TestModel, 1)
        model = helper_models.TestModel(key=key)
        model.put()
        self.removeNDBCache(model.key)
        self.clearContext()
        del model

        gcounter.DEBUG = True
        print '\n------------------------------------------------------11'
        ndb.Key(helper_models.TestModel, 1).get()
        # _pre_get_hook Key('TestModel', 1)
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _projection ()
        # _post_get_hook
        # m __setattr__ _is_new False

    def dtestGetByKeyWithContext(self):

        key = ndb.Key(helper_models.TestModel, 1)
        model = helper_models.TestModel(key=key)
        model.put()
        del model

        gcounter.DEBUG = True
        print '\n------------------------------------------------------12'
        ndb.Key(helper_models.TestModel, 1).get()
        # _pre_get_hook Key('TestModel', 1)
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _projection ()
        # _post_get_hook
        # m __setattr__ _is_new False

    def dtestGetByQuery(self):

        key = ndb.Key(helper_models.TestModel, 1)
        model = helper_models.TestModel(key=key)
        model.put()
        self.removeNDBCache(model.key)
        self.clearContext()
        del model

        gcounter.DEBUG = True
        print '\n------------------------------------------------------13'
        helper_models.TestModel.query().fetch(100)
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _projection ()

    def dtestGetByQuery2(self):

        key = ndb.Key(helper_models.TestModel, 1)
        model = helper_models.TestModel(key=key, ic1=1)
        model.put()
        self.removeNDBCache(model.key)
        self.clearContext()
        del model

        gcounter.DEBUG = True
        print '\n------------------------------------------------------14'
        helper_models.TestModel.query(helper_models.TestModel.ic1 == 1).fetch(100)
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _projection ()

    def dtestGetByQueryWithContext(self):

        key = ndb.Key(helper_models.TestModel, 1)
        model = helper_models.TestModel(key=key)
        model.put()
        del model

        gcounter.DEBUG = True
        print '\n------------------------------------------------------15'
        helper_models.TestModel.query().fetch(100)
        # m __setattr__ _values {}
        # __init__ () {}
        # m __setattr__ _is_new True
        # m __setattr__ _is_dirty False
        # m __setattr__ _key Key('TestModel', 1)
        # m __setattr__ _entity_key Key('TestModel', 1)
        # m __setattr__ _projection ()

    def dtestChangeNotDefinedProperty(self):

        model = helper_models.TestModel()
        model.put()

        print '\n------------------------------------------------------16'
        # model.not_existing = 'aaaa'

    def dtestAppendRepeated(self):

        model = helper_models.TestModel()

        gcounter.DEBUG = True
        print '\n------------------------------------------------------17'
        model.scr1
        # print dir(model.scr1)
        model.scr1.append('test')
        # print model.scr1
