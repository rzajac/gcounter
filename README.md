# Global Counters

#### Short description:

This package will help you count things using sharded counters in the AppEngine Datastore.

#### Long description

As you know Datastore is NoSQL database and questions like "How many users with confirmed email do we have?" are really hard to do.
You can of course write map reduce job but better idea is to pre calculate data you need in advance. To do that you have to track / monitor
your models for changes. And when they occur update respective counter. This package will help you with monitoring your models.

## Quick Example

Let's say we have model like this:

```python
class User(gcounter.Model):

    uname = ndb.StringProperty(required=True)
    upass = ndb.StringProperty(indexed=False)
    email =  ndb.StringProperty(required=True)
    confirmed = gcounter.BooleanProperty(default=False, counter_name='confirmed_email')
```

You noticed that one of the properties is `gcounter.BooleanProperty(counter_name='confirmed_email')`. This is how you define a property that
is going to be tracked for changes. The *counter_name* parameter you set to a counter name that will hold the global count for all
users in your datastore. And this is how you use it:

```python
new_user = User(uname='joe', email='joe@example.com', pass='secret')
new_user.put()

counter = new_user.get_counter_actions()  # returns {}
```

We just created a new user. His email is not confirmed yet (the confirmed property is False) that's why the call to `get_counter_actions()`
is returning the empty dictionary. Meaning no counters have to be updated. It's worth mentioning now that `gcounter.BooleanProperty()` is
tracking only True values. See descriptions of available counters below.

Some time later the user confirms the email address. So somewhere in your code you might have lines like this:

```python
user = get_user(uname='joe')
user.confirmed = True
user.put()

counter = user.get_counter_actions()  # returns {'confirmed_email': 1}
```

This time the counter dictionary returned with counter name and count equal to 1. This means that you should update the counter name
'confirmed_email' adding to it 1.

If for some reason you would later change confirmed property from True to False and called `user.get_counter_actions()` it would
return `{'confirmed_email': -1}` indicating that you have to decrement the counter.

Now that we have the counter name to update we want to call:

```python
for counter_name, delta in counter.items():
    gcounter.Counter.change_counter(counter_name, actions[counter_name])  # Or even better use Task Queue
```

and we are done. To get current value of the counter you would call `gcounter.Counter.get_count('confirmed_email')`.

This is a very simple example how to use Global Counter module. You of course can have in a model as many counters as you want.

*Please see tests! I believe they document this package better then I here :)*

To run tests run:

```
make test
```

or

```
./tests/testrunner.py /usr/local/google_appengine tests
```

## Some terminology

Here is a terminology clarification that I will be using later in the documentation:

*New model* - model that has not been persisted in the Datastore.
*Persisted model* - model that has been saved in the Datastore.
*Pristine state* - model that has not been edited since retraining from the Datastore.

## Counter types

### gcounter.BooleanCounter

Tracking boolean properties.

It takes the same properties as `ndb.BooleanProperty()` plus `counter_name` property.

It behaves in the following way:

For new models:
 - generate +1 counter action only when persisted with tracked value set to True.
 - models persisted with tracked value set to False or None will not generate any counter actions.

For models that are retrieved from the Datastore:
 - changing tracked value to the same value will not generate any counter actions.
 - changing tracked value from True to False or None will generate counter action -1.
 - changing tracked value from False or None to True will generate counter action +1.

Also:
 - Counter actions can be retrieved only when model is persisted and in pristine state.
 - Accessing counter actions when model is not in pristine state will throw gcounter.ModelTrackingNotSaved exception.
 - This counter cannot have repeated property set

### gcounter.IntegerProperty

Tracking integer properties.

It takes the same properties as `ndb.BooleanProperty()` plus `counter_name` property.

It behaves in the following way:

For new models:
 - generate +1 counter action only when persisted with tracked value greater then 0
 - models persisted with tracked value set to 0 or less will not generate any counter actions.

For models that are retrieved from the Datastore:
 - changing tracked value to the same value will not generate any counter actions.
 - changing tracked value from positive value to 0 or less will generate counter action -1.
 - changing tracked value from 0 or less to positive value will generate counter action +1.

Also:
 - Counter actions can be retrieved only when model is persisted and in pristine state.
 - Accessing counter actions when model is not in pristine state will throw gcounter.ModelTrackingNotSaved exception.
 - This counter cannot have repeated property set

### gcounter.StringProperty

Tracking string properties.

It takes the same properties as `ndb.StringProperty()` plus `counter_name` property.

It behaves in the following way:

For new models:
 - generate +1 counter action only when persisted with tracked value equal to not empty string.
 - models persisted with tracked value set to None should not generate any counter actions.

For models that are retrieved from the Datastore:
 - changing tracked value to the same value will not generate any counter actions.
 - changing tracked value from not empty string to None will generate counter action -1.
 - changing tracked value from None or empty string to not empty string will generate counter action +1.

Also:
 - Counter actions can be retrieved only when model is persisted and in pristine state.
 - This counter may have repeated property set

gcounter.StringProperty counters have more features then other types. First of all they support three counter types:

- *simple counter* - regular counter that we saw in the example above
- *complex counter* - a counter that allows you to build counter name based on tracked property value
- *dependent counter* - a counter that name is constructed from values of other properties in the model

We will see examples of all of them later.

### gcounter.ComputedProperty

This counter is exactly that the name suggests. It takes a function which result is treated as a value for the property.

It takes the same properties as `ndb.ComputedProperty()` plus `counter_name` and `behaviour` property.

The `behaviour` property can be set to any of:

- BooleanProperty
- IntegerProperty
- StringProperty

and it will make a counter behave as chosen counter type. So for example creating a counter like this:

```python
name_length = gcounter.ComputedProperty(lambda self: len(self.name) if self.name else 0, counter_name='cp1n', behaviour='IntegerProperty')
```

will make it behave exactly like `gcounter.IntegerProperty`

# Examples

## gcounter.IntegerProperty counter

```python
class User(gcounter.Model):
    favorite_count = gcounter.IntegerProperty(default=0, counter_name='favorites')
```

This will allow you to count all the users that did favorite something.

## gcounter.BooleanProperty counter

We have seen an example of usage at the beginning of the document.

## gcounter.StringProperty simple not repeated counter

```python
class User(gcounter.Model):
    first_name = gcounter.StringProperty(default=None, counter_name='first_name_set')
```

Counter action will be set to one for all models that have the `first_name` set to not empty string.

## gcounter.StringProperty simple repeated counter

TODO

## gcounter.StringProperty complex counter

```python
class Song(gcounter.Model):
    author = gcounter.StringProperty(counter_name='song_author:%s')


song = Song(author="Bob Dylan")
song.put()

counter = song.get_counter_actions()  # returns {'song_author:bob-dylan': 1}
```

This counter will allow us to answer the question how many songs do we have by author X in the Datastore.
Note that the value of the author property was slugifyed.


## gcounter.StringProperty complex repeated counter

```python
class Song(gcounter.Model):
    codecs = gcounter.StringProperty(counter_name='song_codec:%s', repeated=True)

song = Song()
song.codecs = ['mp3', 'aac']
song.put()

counter = song.get_counter_actions()  # returns {'song_codec:mp3': 1, 'song_codec:aac': 1}
```

Later let's say we remove aac codec from this song:

```python

song = get_song(...)
song.codecs.remove('aac')
song.put()

counter = song.get_counter_actions()  # returns {'song_codec:aac': -1}
```

## gcounter.StringProperty dependent counter

```python
class Place(gcounter.Model):
    # Country
    co = gcounter.StringProperty(default=None, counter_name='loc:%s')
    # Region
    reg = gcounter.StringProperty(default=None, counter_name='loc:<co>:%s')
    # City
    ci = gcounter.StringProperty(default=None, counter_name='loc:<co>:<reg>:%s')
```

In this example we want to count geographical places. The counters for this kind of tracking depend on each other. We see that:

- city counter depends on region and country
- region counter depends on country

The values in the square braces are names of the properties that values will be put inside them. Let's see an example:

```python
place = Place(co='us', reg='ca', ci='Costa Mesa')
place.put()

counters = place.get_counter_actions()  # returns {'loc:us': 1, 'loc:us:ca': 1, 'loc:us:ca:costa-mesa': 1}
```

Changing value of a property that other counters depend on will trigger counter action changes:

```python
place = get_place(...)
place.co = 'pl'
place.put()

counters = place.get_counter_actions()  # returns {'loc:pl': 1, 'loc:pl:ca:costa-mesa': 1, 'loc:pl:ca': 1, 'loc:us': -1, 'loc:us:ca:costa-mesa': -1, 'loc:us:ca': -1}
```

We see that all previous counters got action -1 and the new ones 1.

## gcounter.ComputedProperty counter

TODO

# TODO:

- Better documentation
- More tests











