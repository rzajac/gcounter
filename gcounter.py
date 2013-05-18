#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source for global counter module

Code downloaded from: http://github.com/rzajac/gcounter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

# Python imports
import re
import copy
import unicodedata
import random

# GAE imports
from google.appengine.api import memcache, datastore_errors
from google.appengine.ext import ndb

BadValueError = datastore_errors.BadValueError

# Global Counter imports

DEBUG = False


class NotSupportedError(Exception):
    pass


class ModelTrackingError(Exception):
    pass


class ModelTrackingNotSaved(Exception):
    pass


class Model(ndb.Model):
    """Base class for models that want to support property change tracking
        and global counters.

        NOTE: All methods beginning with underscore are considered private
    """

    def __init__(self, *args, **kwds):

        if DEBUG:
            print '__init__', args, kwds

        # See: http://docs.python.org/2/reference/datamodel.html#object.__setattr__
        self.__dict__['_prop_names'] = []

        super(Model, self).__init__(*args, **kwds)

        # Get property descriptors
        self._set_prop_descriptors()

        # Initial values
        self._init_values = copy.deepcopy(self.to_dict())

        # True if entity is not persisted in the Datastore
        self._is_new = True

        # Did entity changed after creating or getting from the Datastore
        self._is_dirty = False

        # By default there are no actions
        self._counter_actions = {}

        if kwds:
            # Get initialization keyword keys
            init_keys = set(kwds.keys())
            # Test if any of the passed keywords set instance properties
            prop_set = self._prop_names & init_keys
            if prop_set:
                for prop in prop_set:

                    # Property values passed by constructor
                    # Doing this we simulate as they would be set
                    # by setters
                    self._init_values[prop] = self._prop_def[prop]['def']

                    if self._prop_def[prop]['def'] != kwds[prop]:
                        # If default value is changed during initialization
                        # we have to set _is_dirty to True
                        self._is_dirty = True
                        break

    def __set__(self, instance, value):
        if DEBUG:
            print 'm __set__ ' + str(instance) + ' ' + str(value)

    def __setattr__(self, name, value):
        if DEBUG:
            print 'm __setattr__ ' + str(name) + ' ' + str(value)

        # This is set only during Model.query(). That means the model
        # cannot be new!
        # Also see: https://code.google.com/p/appengine-ndb-experiment/issues/detail?id=211
        # NOTE: This is using internal APIs test. If they ever change
        # we are screwed!
        if name == '_projection':
            self.__dict__['_is_new'] = False
            return

        # Set as dirty only when name referrers to one of the model properties and
        # its value is different from the current value.
        # We skip properties that start with '_'.
        if not name.startswith('_') and name in self._prop_names and getattr(self, name) != value:
            self.__dict__['_is_dirty'] = True

        super(Model, self).__setattr__(name, value)

    @classmethod
    def _pre_get_hook(cls, key):
        """Hook that runs before Key.get() when getting an entity of this model.
            See: https://developers.google.com/appengine/docs/python/ndb/modelclass
        """
        if DEBUG:
            print '_pre_get_hook ' + str(key)

    @classmethod
    def _post_get_hook(cls, key, future):
        """Hook that runs after Key.get() when getting an entity of this model.
            See: https://developers.google.com/appengine/docs/python/ndb/modelclass
        """
        if DEBUG:
            print '_post_get_hook'

        self = future.get_result()
        if self:
            # Test needed because post_get_hook is called even if get() fails!
            # http://stackoverflow.com/a/12096066/282882
            self._is_new = False

    def _pre_put_hook(self):
        """Hook runs begore put()
            See: https://developers.google.com/appengine/docs/python/ndb/modelclass
        """
        if DEBUG:
            print '_pre_put_hook'

    def _post_put_hook(self, future):
        """Hook runs after put()
            See: https://developers.google.com/appengine/docs/python/ndb/modelclass
        """
        if DEBUG:
            print '_post_put_hook'

        key = future.get_result()
        if key:
            # Get counter actions before we change
            # values of _is_new and _is_dirty
            self._get_counter_actions()
            # The entity is no longer new
            self._is_new = False
            # We just saved it so it's not dirty
            self._is_dirty = False
            # Reset initial values to the ones we have right now
            self._init_values = copy.deepcopy(self.to_dict())

    @property
    def is_new(self):
        """Returns True if model is not persisted in the Datastore"""
        return self._is_new

    @property
    def is_dirty(self):
        """Returns True if model is dirty"""
        return self._is_dirty

    def put(self, **ctx_options):
        """Puts model into the Datastore"""
        if DEBUG:
            print 'put'

        ret = ndb.Model.put(self, **ctx_options)
        return ret

    def _ensure_saved_and_not_dirty(self):
        """Throws an exception if model is dirty or not saved in the Datastore"""
        if self.is_new or self._is_dirty:
            raise ModelTrackingNotSaved('You have to put the model in the Datastore before you can get counter actions.')

    def _set_prop_descriptors(self):
        """Create dictionaries describing model properties

            Sets:
                self._prop_def - dictionary with property definitions
                self._prop_names - set with all property names
                self._rev_deps - reverse dependencies

        """
        self._prop_def = {}
        self._rev_deps = {}

        for name, prop in self.__class__._properties.items():

            if isinstance(prop, TrackedProperty):
                tracked = True
                deps = prop._dependencies
                beh = prop._counter_behaviour
            else:
                tracked = False
                deps = []
                beh = None

            self._prop_def[name] = {
                'def': prop._default,
                'req': prop._required,
                'rep': prop._repeated,
                'tra': tracked,
                'dep': deps,
                'beh': beh}

            if beh is not None and prop._counter_behaviour.startswith('CP'):
                self._prop_def[name]['def'] = None

            # Build reverse dependencies dictionary
            for dep in deps:
                if dep not in self._rev_deps:
                    self._rev_deps[dep] = [name]
                elif name not in self._rev_deps[dep]:
                    self._rev_deps[dep].append(name)

        self._prop_names = set(self._prop_def.keys())

    def _get_counter_actions(self):
        """Get counter actions"""
        updated_properties = self._get_updated_properties()
        if updated_properties:
            counter_actions = self._get_actions(updated_properties)
            self._counter_actions = Counter.aggregate_counters(counter_actions)
        else:
            self._counter_actions = {}

    def _get_updated_properties(self):
        """Get watched properties that have changed since last time the entity
            was put to the Datastore.
        """
        new_values = self.to_dict()

        # print '\n-----------------'
        # print 'GET UPDATED PROPERTIES'
        # print 'Prop defs: ', self._prop_def
        # print 'Rev deps: ', self._rev_deps
        # print 'Prop names: ', self._prop_names
        # print 'Initial values: ', self._init_values
        # print 'Current values: ', new_values
        # print 'Is New: ', self._is_new

        # Dictionary of updated properties
        updated_properties = {}

        for name in self._prop_names:
            # Skip properties that are not watched
            if not self._prop_def[name]['tra']:
                continue

            # print 'Prop name: ', name

            # Original value
            value_orig = self._init_values[name]

            beh = self._prop_def[name]['beh']
            if self._is_new and beh is not None and beh.startswith('CP'):
                value_orig = self._prop_def[name]['def']

            # The value the property has now
            value_new = new_values[name]

            # Default property value
            default = self._prop_def[name]['def']

            # Is property required
            is_required = self._prop_def[name]['req']

            # Indicates if value was updated / changed
            set_updated = False

            if value_orig != value_new:
                set_updated = True

            elif self._is_new:
                if value_new == default:
                    set_updated = True

                # Deal with required parameters passed to __init__
                if is_required and value_orig == value_new:
                    set_updated = True
                    value_orig = None

            if set_updated:
                watched_dict = {
                    'old': value_orig,
                    'new': value_new,
                    'def': default,
                    'dep': self._prop_def[name]['dep']}

                updated_properties[name] = watched_dict

                # Add dependent properties
                if name in self._rev_deps:
                    for dep_name in self._rev_deps[name]:

                        if dep_name in self._init_values:
                            old_dep = self._init_values[dep_name]
                            deps = self._prop_def[dep_name]['dep']
                            dep_def = self._prop_def[dep_name]['def']
                        else:
                            old_dep = getattr(self, dep_name)
                            deps = []
                            dep_def = self.__class__._properties[dep_name]._default

                        updated_properties[dep_name] = {
                            'old': old_dep,
                            'new': getattr(self, dep_name),
                            'dep': deps,
                            'def': dep_def}

        # print 'Updated props: ', updated_properties
        # print '-----------------'
        return updated_properties

    def _get_actions(self, updated_properties):
        """Get counter actions based on updated properties"""

        counter_actions = []
        for name, data in updated_properties.items():
            # Get the property class
            prop = getattr(self.__class__, name)

            # Check if the property is dependent on some other property(s)
            deps = {}
            for dep_name in data['dep']:
                if dep_name in updated_properties:
                    deps[dep_name] = {
                        'new': updated_properties[dep_name]['new'],
                        'old': updated_properties[dep_name]['old']}
                else:
                    deps[dep_name] = {
                        'new': getattr(self, dep_name),
                        'old': getattr(self, dep_name)}

            # Get action based on property type
            action = prop._get_counter_actions(data, self.is_new, deps)

            if action:
                counter_actions.append(action)

        return counter_actions

    def _reset_counter_actions(self):
        self._counter_actions = {}

    def get_counter_actions(self):
        """Get counter actions"""

        self._ensure_saved_and_not_dirty()

        ret = copy.deepcopy(self._counter_actions)
        self._reset_counter_actions()
        return ret


class TrackedProperty(object):
    """Mix-in class for all tracked properties

        NOTE: All methods beginning with underscore are considered private
    """

    def __init__(self):
        self._counter_type = None
        self._counter_name = None
        self._repeated = False
        self._counter_behaviour = None

    def is_simple_counter(self):
        return self._counter_type == 'sc'

    def is_complex_counter(self):
        return self._counter_type == 'cc'

    def is_dependent_counter(self):
        return self._counter_type == 'dc'

    def _get_counter_type(self):
        """Get Counter type based on counter name """

        if '<' in self._counter_name:
            counter_type = 'dc'  # Dependent counter
        elif '%s' in self._counter_name:
            counter_type = 'cc'  # Complex counter
        else:
            counter_type = 'sc'  # Simple counter

        return counter_type

    @property
    def _dependencies(self):
        """Get list of property names this property is dependent on"""

        deps = re.findall(r'<([a-z_0-9]+)>', self._counter_name, re.I)
        return list(set(deps))

    def _get_counter_actions_int(self, change, is_new, **kwds):
        """Get global counter actions for gcounter.IntegerProperty properties"""

        old_value = change['old']
        new_value = change['new']
        def_value = change['def']

        actions = {}

        # Nothing to do if both are None or 0
        if (old_value is None or old_value == 0) and (new_value is None or new_value == 0):
            return {}

        # If this is a new instance and default value is more then 0 we bump the counter
        if is_new and 0 < def_value <= new_value:
            return Counter.add_delta(actions, self._counter_name, 1)

        if (old_value <= 0 or old_value is None) and new_value > 0:
            return Counter.add_delta(actions, self._counter_name, 1)

        if old_value > 0 and (new_value <= 0 or new_value is None):
            if not is_new:
                return Counter.add_delta(actions, self._counter_name, -1)

        return actions

    def _get_counter_actions_boolean(self, change, is_new, **kwds):

        old_value = change['old']
        new_value = change['new']
        def_value = change['def']

        actions = {}

        # Nothing to do if both are None or False
        if (old_value is None or old_value is False) and (new_value is None or new_value is False):
            return {}

        # If this is a new instance and default value is True we bump the counter
        if is_new and def_value and new_value == def_value:
            return Counter.add_delta(actions, self._counter_name, 1)

        if not old_value and new_value:
            return Counter.add_delta(actions, self._counter_name, 1)

        if old_value and not new_value:
            if not is_new:
                return Counter.add_delta(actions, self._counter_name, -1)

        return actions

    def _get_counter(self, value, deps=None):
        """Get counter name based on counter type and the property value

            Note: For dependent counter the value is expected to be a list
        """

        if value in [None, '', []]:
            return None

        if self._counter_type == 'sc':
            return self._counter_name
        elif self._counter_type == 'cc':
            return self._counter_name % TextTools.slugify(value)
        elif self._counter_type == 'dc':
            counter_name = self._counter_name

            for dep_name, dep_value in deps.items():
                marker = '<' + dep_name + '>'

                if dep_value is None:
                    dep_value = ''
                else:
                    dep_value = TextTools.slugify(dep_value)

                counter_name = counter_name.replace(marker, dep_value)

            if '%s' in counter_name:
                counter_name = counter_name % TextTools.slugify(value)

            return counter_name
        else:
            raise NotSupportedError

    def _get_counter_actions_string(self, change, is_new, deps=None):

        old_value = change['old']
        new_value = change['new']
        def_value = change['def']

        actions = {}

        # Nothing to do if both are None or empty strings
        if (old_value is None or old_value == '') and (new_value is None or new_value == ''):
            return {}

        # If this is a new instance and default value is not none or empty string
        # We bump the counter
        if is_new and def_value and new_value == def_value:
            return Counter.add_delta(actions, self._get_counter(new_value), 1)

        # For the simple counter the change of the value does not matter
        # as long as both values are not None or empty string.
        # Unless this is a new entity then we have to bump the counter.
        if self._counter_type == 'sc' and old_value and new_value:
            if is_new:
                return Counter.add_delta(actions, self._get_counter(new_value), 1)
            else:
                return {}

        if self._repeated and self._counter_type == 'cc':

            ld = ListDiffer(new_value, old_value)
            added = ld.added()
            removed = ld.removed()

            if len(added) == 0 and len(removed) == 0:
                return {}

            for add_value in added:
                Counter.add_delta(actions, self._get_counter(add_value), 1)

            for remove_value in removed:
                Counter.add_delta(actions, self._get_counter(remove_value), -1)

            return actions

        if self._counter_type == 'dc':
            old_deps = {}
            new_deps = {}
            for prop_name, dep in deps.items():
                old_deps[prop_name] = dep['old']
                new_deps[prop_name] = dep['new']

            counter_name_new = self._get_counter(new_value, new_deps)
            Counter.add_delta(actions, counter_name_new, 1)

            counter_name_old = self._get_counter(old_value, old_deps)
            Counter.add_delta(actions, counter_name_old, -1)

            return actions
        else:
            counter_name_old = self._get_counter(old_value)
            counter_name_new = self._get_counter(new_value)

        if old_value != new_value:
            Counter.add_delta(actions, counter_name_new, 1)
            if not is_new:
                Counter.add_delta(actions, counter_name_old, -1)

        return actions


class IntegerProperty(ndb.IntegerProperty, TrackedProperty):

    def __init__(self, counter_name, **kwds):
        super(IntegerProperty, self).__init__(**kwds)
        self._counter_name = counter_name
        self._counter_type = self._get_counter_type()
        self._counter_behaviour = 'IntegerProperty'
        IntegerProperty._validate_counter(self)

    @staticmethod
    def _validate_counter(inst):
        if inst._repeated:
            raise ModelTrackingError('Tracked IntegerProperty cannot be repeated property.')
        if inst._counter_type != 'sc':
            raise ModelTrackingError('Tracked IntegerProperty must be simple counter type.')

    def _get_counter_actions(self, change, is_new, deps=None):
        return self._get_counter_actions_int(change, is_new)


class BooleanProperty(ndb.BooleanProperty, TrackedProperty):

    def __init__(self, counter_name, **kwds):
        super(BooleanProperty, self).__init__(**kwds)
        self._counter_name = counter_name
        self._counter_type = self._get_counter_type()
        self._counter_behaviour = 'BooleanProperty'
        BooleanProperty._validate_counter(self)

    @staticmethod
    def _validate_counter(inst):
        if inst._repeated:
            raise ModelTrackingError('Tracked BooleanProperty cannot be repeated property.')
        if inst._counter_type != 'sc':
            raise ModelTrackingError('Tracked BooleanProperty must be simple counter type.')

    def _get_counter_actions(self, change, is_new, deps=None):
        return self._get_counter_actions_boolean(change, is_new)


class StringProperty(ndb.StringProperty, TrackedProperty):

    def __init__(self, counter_name, **kwds):
        super(StringProperty, self).__init__(**kwds)
        self._counter_name = counter_name
        self._counter_type = self._get_counter_type()
        self._counter_behaviour = 'StringProperty'
        StringProperty._validate_counter(self)

    @staticmethod
    def _validate_counter(inst):
        if inst._counter_type == 'dc' and inst._repeated:
            raise ModelTrackingError('You cannot have repeated and dependent counter property in the same time.')

    def _validate(self, value):
        super(StringProperty, self)._validate(value)
        if value == '':
            raise BadValueError('Property must not be an empty string')

    def _get_counter_actions(self, change, is_new, deps=None):
        return self._get_counter_actions_string(change, is_new, deps)


class ComputedProperty(ndb.ComputedProperty, TrackedProperty):

    def __init__(self, func, counter_name, behaviour='StringProperty', name=None, indexed=None, repeated=None):
        super(ComputedProperty, self).__init__(func, name, indexed, repeated)
        self._counter_name = counter_name
        self._counter_type = self._get_counter_type()
        self._counter_behaviour = 'CP' + behaviour

    def _get_counter_actions(self, change, is_new, deps=None):
        if self._counter_behaviour == 'CPStringProperty':
            StringProperty._validate_counter(self)
            return self._get_counter_actions_string(change, is_new, deps)
        elif self._counter_behaviour == 'CPBooleanProperty':
            BooleanProperty._validate_counter(self)
            return self._get_counter_actions_boolean(change, is_new)
        elif self._counter_behaviour == 'CPIntegerProperty':
            IntegerProperty._validate_counter(self)
            return self._get_counter_actions_int(change, is_new)
        else:
            raise NotImplementedError


class TextTools(object):

    @staticmethod
    def slugify(value):
        """
        Normalizes string, converts to lowercase, removes non-ascii characters,
        and converts spaces to hyphens.  For use in URLs and filenames

        From Django's "django/template/defaultfilters.py".
        """
        _slugify_strip_re = re.compile(r'[^\w\s-]')
        _slugify_hyphenate_re = re.compile(r'[-\s]+')

        if not isinstance(value, unicode):
            value = unicode(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(_slugify_strip_re.sub('', value).strip().lower())
        return _slugify_hyphenate_re.sub('-', value)


class ListDiffer(object):
    """Calculate the difference between two lists"""

    def __init__(self, current_list, old_list):
        self.intersect = None
        self.current_list, self.old_list = current_list, old_list
        self.set_current, self.set_old = set(current_list), set(old_list)

    def added(self):
        return self.set_current - self.set_old

    def removed(self):
        return self.set_old - self.set_current

    def get_intersect(self):
        if self.intersect is None:
            self.intersect = self.set_current.intersection(self.set_old)

    def changed(self):
        self.get_intersect()
        return set(o for o in self.intersect if self.old_list[o] != self.current_list[o])

    def unchanged(self):
        self.get_intersect()
        return set(o for o in self.intersect if self.old_list[o] == self.current_list[o])


class GeneralCounterShardConfig(ndb.Model):
    """Tracks the number of shards for each named counter."""

    name = ndb.StringProperty(required=True)
    num_shards = ndb.IntegerProperty(default=20, indexed=False)


class GeneralCounterShard(ndb.Model):
    """Shards for each named counter"""

    name = ndb.StringProperty(required=True)
    count = ndb.IntegerProperty(default=0, indexed=False)


class CounterActions(ndb.Model):
    """Counter actions

        Helper model to store multiple operations on counters as JSON object.
        This is later used to aggregate many counter actions (add, subtract).

        It's used to save thousands of calls to Datastore by first aggregating
        actions on the same counters and then making a call to edit a counter in
        Datastore.
    """

    actions = ndb.JsonProperty(required=True)
    processed = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Counter(object):
    """Utility class for shard counters"""

    @staticmethod
    def get_count(name, force=False):
        """Retrieve the value for a given sharded counter.

        Arguments:
          name - The name of the counter
          force - Set to True to force counter retrieval from the Datastore
        """
        total = memcache.get(name)
        if total is None or force is True:
            total = 0
            for counter in GeneralCounterShard.query(GeneralCounterShard.name == name):
                total += counter.count
            memcache.add(name, total, 60)
        return total

    @staticmethod
    def incr(name):
        """Increment the value for a given shard counter.

        Arguments:
          name - The name of the counter
        """
        Counter.change_counter(name, 1)

    @staticmethod
    def decr(name):
        """Decrement the value for a given shard counter.

        Arguments:
          name - The name of the counter
        """
        Counter.change_counter(name, -1)

    @staticmethod
    def change_counter(name, delta):
        """Change counter value by delta

            Arguments:
                name - the name of the counter
                delta - the change delta. Ex.: -1, +1, +10...
        """
        config = GeneralCounterShardConfig.get_or_insert(name, name=name)

        @ndb.transactional
        def txn():
            index = random.randint(0, config.num_shards - 1)
            shard_name = name + str(index)
            counter = GeneralCounterShard.get_by_id(shard_name)
            if counter is None:
                counter = GeneralCounterShard(id=shard_name, name=name)
            counter.count += delta
            counter.put()

        txn()

        memcache.delete(name)

    @staticmethod
    def increase_shards(name, num):
        """Increase the number of shards for a given shard counter.
        Will never decrease the number of shards.

        Arguments:
          name - The name of the counter
          num - How many shards to use

        """
        config = GeneralCounterShardConfig.get_or_insert(name, name=name)

        @ndb.transactional
        def txn():
            if config.num_shards < num:
                config.num_shards = num
                config.put()

        txn()

    @staticmethod
    def add_delta(actions, counter_name, delta):
        """Helper for adding delta to counter_name

            Arguments:
                actions - dictionary of counter actions
                counter_name - the name of counter to change
                delta - the amount to change counter
        """

        if counter_name is None:
            return

        if counter_name not in actions:
            actions[counter_name] = 0

        actions[counter_name] += delta

        return actions

    @staticmethod
    def aggregate_counters(counter_actions, remove_zero=True):
        """Aggregate array of counter action dictionaries to one dictionary"""

        c_act_aggr = {}
        for actions in counter_actions:
            for action, delta in actions.items():
                count = c_act_aggr.get(action, 0) + delta
                if remove_zero and count == 0:
                    del c_act_aggr[action]
                else:
                    c_act_aggr[action] = count

        return c_act_aggr

    @staticmethod
    def get_model_counters(models):
        """Get models counter actions"""

        counter_actions = []
        for model in models:
            ca = model.get_counter_actions()
            counter_actions.append(ca)
        return counter_actions
