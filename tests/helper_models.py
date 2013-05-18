#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper models used in tests.

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# GAE imports
from google.appengine.ext import ndb

# Gcounter imports
import gcounter


class TestModel(gcounter.Model):
    """General test model"""

    ic1 = gcounter.IntegerProperty(default=None, counter_name='ic1')
    sc1 = gcounter.StringProperty(default='test', counter_name='sc1', indexed=False)

    scr1 = gcounter.StringProperty(repeated=True, counter_name='sc1', indexed=False)

    # Single properties
    nt1 = ndb.IntegerProperty(default=None, indexed=False)
    nt2 = ndb.IntegerProperty(default=2, indexed=False)
    nt3 = ndb.StringProperty(default=None, indexed=False)
    nt4 = ndb.StringProperty(default='test', indexed=False)

    # Repeated properties
    nt5 = ndb.IntegerProperty(repeated=True, indexed=False)
    nt6 = ndb.StringProperty(repeated=True, indexed=False)


class TestBC1(gcounter.Model):
    """Test model gcounter.BooleanProperty"""

    # BooleanProperty with simple counter and no default value
    bc1 = gcounter.BooleanProperty(default=None, counter_name='bc1n')


class TestBC2(gcounter.Model):
    """Test model gcounter.BooleanProperty"""

    # BooleanProperty with simple counter and default value set to False
    bc2 = gcounter.BooleanProperty(default=False, counter_name='bc2n')


class TestBC3(gcounter.Model):
    """Test model gcounter.BooleanProperty"""

    # BooleanProperty with simple counter and default value set to True
    bc3 = gcounter.BooleanProperty(default=True, counter_name='bc3n')


class TestSC1(gcounter.Model):
    """Test model gcounter.StringProperty with simple counter"""

    # StringProperty with simple counter and default value set to some string
    sc1 = gcounter.StringProperty(default='test', counter_name='sc1n')


class TestSC2(gcounter.Model):
    """Test model gcounter.StringProperty with simple counter"""

    # StringProperty with simple counter and default value set to None
    sc2 = gcounter.StringProperty(default=None, counter_name='sc2n')


class TestSCR1(gcounter.Model):
    """Test model for repeated gcounter.StringProperty with simple counter"""

    # Repeated StringProperty with simple counter
    scr1 = gcounter.StringProperty(counter_name='scr1n', repeated=True)


class TestCC1(gcounter.Model):
    """Test model for gcounter.StringProperty with complex counter"""

    # StringProperty with complex counter and default value set to string
    cc1 = gcounter.StringProperty(default='test', counter_name='cc1n:%s')


class TestCC2(gcounter.Model):
    """Test model for gcounter.StringProperty with complex counter"""

    # StringProperty with complex counter and default value set to None
    cc2 = gcounter.StringProperty(default=None, counter_name='cc2n:%s')


class TestCCR1(gcounter.Model):
    """Test model for repeated gcounter.StringProperty with complex counter"""

    # Repeated StringProperty with complex counter
    ccr1 = gcounter.StringProperty(counter_name='ccr1n:%s', repeated=True)


class TestIC1(gcounter.Model):
    """Test model gcounter.IntegerProperty"""

    # IntegerProperty with simple counter and default value set to None
    ic1 = gcounter.IntegerProperty(default=None, counter_name='ic1n')


class TestIC2(gcounter.Model):
    """Test model gcounter.IntegerProperty"""

    # IntegerProperty with simple counter and default value set to -1
    ic2 = gcounter.IntegerProperty(default=-1, counter_name='ic2n')


class TestIC3(gcounter.Model):
    """Test model gcounter.IntegerProperty"""

    # IntegerProperty with simple counter and default value set to 1
    ic3 = gcounter.IntegerProperty(default=1, counter_name='ic3n')


class TestIC4(gcounter.Model):
    """Test model gcounter.IntegerProperty"""

    # IntegerProperty with simple counter and default value set to 0
    ic4 = gcounter.IntegerProperty(default=0, counter_name='ic4n')


class TestDC1(gcounter.Model):
    """Test model for dependent counters"""

    # Country
    co = gcounter.StringProperty(default=None, counter_name='loc:%s')
    # Region
    reg = gcounter.StringProperty(default=None, counter_name='loc:<co>:%s')
    # City
    ci = gcounter.StringProperty(default=None, counter_name='loc:<co>:<reg>:%s')


class TestCP1(gcounter.Model):
    """Test model for computed counters"""

    # The value of the cp1 is the length of value of name.
    # Global counter will behave as gcounter.IntegerProperty
    cp1 = gcounter.ComputedProperty(lambda self: len(self.name) if self.name else 0, counter_name='cp1n', behaviour='IntegerProperty')
    name = ndb.StringProperty(default=None)


class TestCP2(gcounter.Model):
    """Test model for computed counters"""

    # The value of the cp2 is the value of my_value + ' test'.
    # Global counter will behave as gcounter.StringProperty
    cp2 = gcounter.ComputedProperty(lambda self: self.my_value + ' ' + ' test' if self.my_value else 'test', counter_name='cp2n', behaviour='StringProperty')
    my_value = ndb.StringProperty(default=None)


class TestCP3(gcounter.Model):
    """Test model for dependent counters"""

    # The value of the cp3 is negation of my_value.
    # Global counter will behave as gcounter.BooleanProperty
    cp3 = gcounter.ComputedProperty(lambda self: not self.my_value, counter_name='cp3n', behaviour='BooleanProperty')
    my_value = ndb.BooleanProperty(default=False)
