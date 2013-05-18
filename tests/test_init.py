#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests init and set

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


class TestInitSet(TestCountersMain):

    def testInitBC1True(self):

        model = helper_models.TestBC1(bc1=True)
        model.put()

        self.assertEquals({'bc1n': 1}, model.get_counter_actions())

    def testSetBC1True(self):

        model = helper_models.TestBC1()
        model.bc1 = True
        model.put()

        self.assertEquals({'bc1n': 1}, model.get_counter_actions())

    def testInitTestBC1None(self):

        model = helper_models.TestBC1(bc1=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC1None(self):

        model = helper_models.TestBC1()
        model.bc1 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitTestBC1False(self):

        model = helper_models.TestBC1(bc1=False)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC1False(self):

        model = helper_models.TestBC1()
        model.bc1 = False
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitTestBC2True(self):

        model = helper_models.TestBC2(bc2=True)
        model.put()

        self.assertEquals({'bc2n': 1}, model.get_counter_actions())

    def testSetBC2True(self):

        model = helper_models.TestBC2()
        model.bc2 = True
        model.put()

        self.assertEquals({'bc2n': 1}, model.get_counter_actions())

    def testInitTestBC2None(self):

        model = helper_models.TestBC2(bc2=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC2None(self):

        model = helper_models.TestBC2()
        model.bc2 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitTestBC2False(self):

        model = helper_models.TestBC2(bc2=False)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC2False(self):

        model = helper_models.TestBC2()
        model.bc2 = False
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitTestBC3True(self):

        model = helper_models.TestBC3(bc3=True)
        model.put()

        self.assertEquals({'bc3n': 1}, model.get_counter_actions())

    def testSetBC3True(self):

        model = helper_models.TestBC3()
        model.bc3 = True
        model.put()

        self.assertEquals({'bc3n': 1}, model.get_counter_actions())

    def testInitTestBC3None(self):

        model = helper_models.TestBC3(bc3=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC3None(self):

        model = helper_models.TestBC3()
        model.bc3 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitTestBC3False(self):

        model = helper_models.TestBC3(bc3=False)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetBC3False(self):

        model = helper_models.TestBC3()
        model.bc3 = False
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitSC1String(self):

        model = helper_models.TestSC1(sc1='string')
        model.put()

        self.assertEquals({'sc1n': 1}, model.get_counter_actions())

    def testSetSC1String(self):

        model = helper_models.TestSC1()
        model.sc1 = 'string'
        model.put()

        self.assertEquals({'sc1n': 1}, model.get_counter_actions())

    def testInitSC1None(self):

        model = helper_models.TestSC1(sc1=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetSC1None(self):

        model = helper_models.TestSC1()
        model.sc1 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitSC1Empty(self):

        with self.assertRaises(datastore_errors.BadValueError):
            helper_models.TestSC1(sc1='')

    def testSetSC1Empty(self):

        model = helper_models.TestSC1()

        with self.assertRaises(datastore_errors.BadValueError):
            model.sc1 = ''

    def testInitSC2String(self):

        model = helper_models.TestSC2(sc2='string')
        model.put()

        self.assertEquals({'sc2n': 1}, model.get_counter_actions())

    def testSetSC2String(self):

        model = helper_models.TestSC2()
        model.sc2 = 'string'
        model.put()

        self.assertEquals({'sc2n': 1}, model.get_counter_actions())

    def testInitSC2None(self):

        model = helper_models.TestSC2(sc2=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetSC2None(self):

        model = helper_models.TestSC2()
        model.sc2 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitSC2Empty(self):

        with self.assertRaises(datastore_errors.BadValueError):
            helper_models.TestSC2(sc2='')

    def testSetSC2Empty(self):

        model = helper_models.TestSC2()

        with self.assertRaises(datastore_errors.BadValueError):
            model.sc2 = ''

    def testInitSCR1String(self):

        model = helper_models.TestSCR1(scr1=['string'])
        model.put()

        self.assertEquals({'scr1n': 1}, model.get_counter_actions())

    def testSetSCR1String(self):

        model = helper_models.TestSCR1()
        model.scr1 = ['string']
        model.put()

        self.assertEquals({'scr1n': 1}, model.get_counter_actions())

    def testInitSCR1Empty(self):

        model = helper_models.TestSCR1(scr1=[])
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetSCR1Empty(self):

        model = helper_models.TestSCR1()
        model.scr1 = []
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC1Plus(self):

        model = helper_models.TestIC1(ic1=123)
        model.put()

        self.assertEquals({'ic1n': 1}, model.get_counter_actions())

    def testSetIC1Plus(self):

        model = helper_models.TestIC1()
        model.ic1 = 123
        model.put()

        self.assertEquals({'ic1n': 1}, model.get_counter_actions())

    def testInitIC1Minus(self):

        model = helper_models.TestIC1(ic1=-123)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC1Minus(self):

        model = helper_models.TestIC1()
        model.ic1 = -123
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC1Zero(self):

        model = helper_models.TestIC1(ic1=0)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC1Zero(self):

        model = helper_models.TestIC1()
        model.ic1 = 0
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC1None(self):

        model = helper_models.TestIC1(ic1=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC1None(self):

        model = helper_models.TestIC1()
        model.ic1 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC2Plus(self):

        model = helper_models.TestIC2(ic2=123)
        model.put()

        self.assertEquals({'ic2n': 1}, model.get_counter_actions())

    def testSetIC2Plus(self):

        model = helper_models.TestIC2()
        model.ic2 = 123
        model.put()

        self.assertEquals({'ic2n': 1}, model.get_counter_actions())

    def testInitIC2Minus(self):

        model = helper_models.TestIC2(ic2=-123)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC2Minus(self):

        model = helper_models.TestIC2()
        model.ic2 = -123
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC2Zero(self):

        model = helper_models.TestIC2(ic2=0)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC2Zero(self):

        model = helper_models.TestIC2()
        model.ic2 = 0
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC2None(self):

        model = helper_models.TestIC2(ic2=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC2None(self):

        model = helper_models.TestIC2()
        model.ic2 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC3Plus(self):

        model = helper_models.TestIC3(ic3=123)
        model.put()

        self.assertEquals({'ic3n': 1}, model.get_counter_actions())

    def testSetIC3Plus(self):

        model = helper_models.TestIC3()
        model.ic3 = 123
        model.put()

        self.assertEquals({'ic3n': 1}, model.get_counter_actions())

    def testInitIC3Minus(self):

        model = helper_models.TestIC3(ic3=-123)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC3Minus(self):

        model = helper_models.TestIC3()
        model.ic3 = -123
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC3Zero(self):

        model = helper_models.TestIC3(ic3=0)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC3Zero(self):

        model = helper_models.TestIC3()
        model.ic3 = 0
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC3None(self):

        model = helper_models.TestIC3(ic3=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC3None(self):

        model = helper_models.TestIC3()
        model.ic3 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC4Plus(self):

        model = helper_models.TestIC4(ic4=123)
        model.put()

        self.assertEquals({'ic4n': 1}, model.get_counter_actions())

    def testSetIC4Plus(self):

        model = helper_models.TestIC4()
        model.ic4 = 123
        model.put()

        self.assertEquals({'ic4n': 1}, model.get_counter_actions())

    def testInitIC4Minus(self):

        model = helper_models.TestIC4(ic4=-123)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC4Minus(self):

        model = helper_models.TestIC4()
        model.ic4 = -123
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC4Zero(self):

        model = helper_models.TestIC4(ic4=0)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC4Zero(self):

        model = helper_models.TestIC4()
        model.ic4 = 0
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testInitIC4None(self):

        model = helper_models.TestIC4(ic4=None)
        model.put()

        self.assertEquals({}, model.get_counter_actions())

    def testSetIC4None(self):

        model = helper_models.TestIC4()
        model.ic4 = None
        model.put()

        self.assertEquals({}, model.get_counter_actions())
