#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for is_new and is_dirty

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports

# GAE imports
from google.appengine.ext import ndb

# Global Counter imports

# Global Counter tests imports
from tests import helper_models
from tests.base_test import TestCountersMain


class TestNewAndDirty(TestCountersMain):
    """Test is_new and is_dirty

        NOTE: is_dirty does not work for repeated properties when they are used with"
            - append()
            - pop()
            - delete()
            ...
    """
    def _removeNDBCache(self, key):
        """Helper method to remove key from context cache"""
        # key.delete(use_datastore=False)
        ndb.get_context()._clear_memcache((key,)).get_result()

    def _createModel(self, id=None, put=False, **kwds):
        """Helper method to create TestModel"""

        if id is not None:
            key = ndb.Key(helper_models.TestModel, id)
            model = helper_models.TestModel(key=key, **kwds)
        else:
            model = helper_models.TestModel(**kwds)

        if not kwds:
            model.ic1 = id

        if put:
            model.put()

        return model

    def testInstantiating(self):
        """Test is_new and is_dirty after instantiating a model"""

        model = self._createModel()
        self.assertTrue(model.is_new)
        # None of the default property values changed
        self.assertFalse(model.is_dirty)

        model = self._createModel(ic1=1)
        self.assertTrue(model.is_new)
        self.assertTrue(model.is_dirty)

    def testAfterPut(self):
        """Test is_new and is_dirty after putting to the Datastore"""

        model = self._createModel(put=True)
        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

        model = self._createModel(id=123, put=True)
        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testAfterPut2(self):
        """Test is_new and is_dirty after putting to the Datastore"""

        model = self._createModel(ic1=1, put=True)
        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

        model = self._createModel(ic1=2, id=123, put=True)
        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testGetByKey(self):
        """Test is_new and is_dirty getting the model by Key"""

        # Create model in the Datastore
        model = self._createModel(id=1, put=True)

        # Remove model from cache
        self._removeNDBCache(model.key)
        del model

        # Get model from the Datastore
        key = ndb.Key(helper_models.TestModel, 1)
        model = key.get()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testGetByKeyWithContext(self):
        """Test is_new and is_dirty after getting the model by Key when model is in the context cache"""

        # Create model in the Datastore
        model = self._createModel(id=1, put=True)
        # Remove model from cache
        del model

        # Get model from the Datastore
        key = ndb.Key(helper_models.TestModel, 1)
        model = key.get()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testGetMulti(self):
        """Test is_new and is_dirty after getting models with ndb.get_multi"""

        # Create first model
        model1 = self._createModel(1, put=True)
        self._removeNDBCache(model1.key)
        del model1

        # Create second model
        model2 = self._createModel(2, put=True)
        self.assertFalse(model2.is_new)
        self.assertFalse(model2.is_dirty)
        self._removeNDBCache(model2.key)
        del model2

        key1 = ndb.Key(helper_models.TestModel, 1)
        key2 = ndb.Key(helper_models.TestModel, 2)

        keys = [key1, key2]
        models = ndb.get_multi(keys)

        self.assertTrue(2, len(models))

        for model in models:
            self.assertFalse(model.is_new)
            self.assertFalse(model.is_dirty)

    def testGetMultiWithContext(self):
        """Test is_new and is_dirty after getting models with ndb.get_multi with model in the context cache"""

        # Create first model
        model1 = self._createModel(1, put=True)
        del model1

        # Create second model
        model2 = self._createModel(2, put=True)
        self.assertFalse(model2.is_new)
        self.assertFalse(model2.is_dirty)
        del model2

        key1 = ndb.Key(helper_models.TestModel, 1)
        key2 = ndb.Key(helper_models.TestModel, 2)

        keys = [key1, key2]
        models = ndb.get_multi(keys)

        self.assertTrue(2, len(models))

        for model in models:
            self.assertFalse(model.is_new)
            self.assertFalse(model.is_dirty)

    def testGetMultiAsync(self):
        """Test is_new and is_dirty after getting models with ndb.get_multi_async"""

        # Create first model
        model1 = self._createModel(1, put=True)
        self._removeNDBCache(model1.key)
        del model1

        # Create second model
        model2 = self._createModel(2, put=True)
        self._removeNDBCache(model2.key)
        del model2

        key1 = ndb.Key(helper_models.TestModel, 1)
        key2 = ndb.Key(helper_models.TestModel, 2)

        keys = [key1, key2]
        futures = ndb.get_multi_async(keys)

        models = []

        for future in futures:
            model = future.get_result()
            self.assertFalse(model.is_new)
            self.assertFalse(model.is_dirty)
            models.append(model)

        self.assertTrue(2, len(models))

    def testGetMultiAsyncWithContext(self):
        """Test is_new and is_dirty after getting models with ndb.get_multi_async with models in context cache"""

        # Create first model
        model1 = self._createModel(1, put=True)
        del model1

        # Create second model
        model2 = self._createModel(2, put=True)
        del model2

        key1 = ndb.Key(helper_models.TestModel, 1)
        key2 = ndb.Key(helper_models.TestModel, 2)

        keys = [key1, key2]
        futures = ndb.get_multi_async(keys)

        models = []

        for future in futures:
            model = future.get_result()
            self.assertFalse(model.is_new)
            self.assertFalse(model.is_dirty)
            models.append(model)

        self.assertTrue(2, len(models))

    def testDirty(self):
        """Test is_new and is_dirty after editing the put model"""

        model1 = self._createModel(1, put=True)
        model1.ic1 = 123
        self.assertFalse(model1.is_new)
        self.assertTrue(model1.is_dirty)

    def testDirtyRepeatedInt(self):
        """Test is_new and is_dirty after editing repeated int property"""

        model = self._createModel(1, put=True)

        self.assertFalse(model.is_dirty)
        model.nt5 = [123]
        self.assertTrue(model.is_dirty)

        model.put()
        self.assertFalse(model.is_dirty)

        # Setting to the same value should not mark model dirty
        model.nt5 = [123]
        self.assertFalse(model.is_dirty)

    # def testDirtyRepeatedIntAppend(self):

    #     model = self._createModel(1, put=True)

    #     self.assertFalse(model.is_dirty)
    #     model.nt5.append(123)
    #     self.assertTrue(model.is_dirty)

    def testDirtyRepeatedString(self):
        """Test is_new and is_dirty after editing repeated string property"""

        model = self._createModel(1, put=True)

        self.assertFalse(model.is_dirty)
        model.nt6 = ['test']
        self.assertTrue(model.is_dirty)

        model.put()
        self.assertFalse(model.is_dirty)

        # Setting to the same value should not mark model dirty
        model.nt6 = ['test']
        self.assertFalse(model.is_dirty)

    def testDirtyNoChange(self):
        """Test is_new and is_dirty after editing the put model with same value"""

        model1 = self._createModel(1, put=True)
        model1.ic1 = 1
        self.assertFalse(model1.is_new)
        self.assertFalse(model1.is_dirty)

    def testGetByQuery(self):
        """Test is_new and is_dirty when getting a model by query"""
        # Create model, persist, change and persist again
        model = self._createModel(1, put=True)
        model.ic1 = 123
        model.put()

        # Remove model from cache
        self._removeNDBCache(model.key)
        del model

        # Get model by query
        model = helper_models.TestModel.query(helper_models.TestModel.ic1 == 123).get()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testGetByQueryWithContext(self):
        """Test is_new and is_dirty when getting a model by query with model in context cache"""

        # Create model, persist, change and persist again
        model = self._createModel(1, put=True)
        model.ic1 = 123
        model.put()

        # Get model by query
        model = helper_models.TestModel.query(helper_models.TestModel.ic1 == 123).get()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testGetWithQueryAll(self):
        """Test is_new and is_dirty after query for all models of the kind"""
        model1 = self._createModel(1, put=True)
        model2 = self._createModel(2, put=True)
        self._removeNDBCache(model1.key)
        self._removeNDBCache(model2.key)
        del model1
        del model2

        models = helper_models.TestModel.query().fetch(10)
        self.assertEqual(2, len(models))

        self.assertFalse(models[0].is_new)
        self.assertFalse(models[1].is_dirty)

        self.assertFalse(models[0].is_new)
        self.assertFalse(models[1].is_dirty)

    def testGetWithQueryAllWithContext(self):
        """Test is_new and is_dirty after query for all models of the kind when models in context cache"""
        model1 = self._createModel(1, put=True)
        model2 = self._createModel(2, put=True)
        del model1
        del model2

        models = helper_models.TestModel.query().fetch(10)
        self.assertEqual(2, len(models))

        self.assertFalse(models[0].is_new)
        self.assertFalse(models[1].is_dirty)

        self.assertFalse(models[0].is_new)
        self.assertFalse(models[1].is_dirty)

    def testRepeatedStringAssign(self):

        model = helper_models.TestSCR1()
        model.scr1 = ['test']

        self.assertTrue(model.is_new)
        self.assertTrue(model.is_dirty)

        model.put()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)

    def testRepeatedStringInit(self):

        model = helper_models.TestSCR1(scr1=['test'])

        self.assertTrue(model.is_new)
        self.assertTrue(model.is_dirty)

        model.put()

        self.assertFalse(model.is_new)
        self.assertFalse(model.is_dirty)
