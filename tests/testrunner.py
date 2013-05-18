#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test runner for Google AppEngine tests.

Example usage:

  To run all the tests in exampletests package

    $ testrunner.py /sdk/path exampletests

  To run all tests in test_example_app.py

    $ testrunner.py /sdk/path exampletests.test_example_app

  To run all tests in specific test case (ExampleAppTestHandlers)

    $ testrunner.py /sdk/path exampletests.test_example_app.ExampleAppTestHandlers

  To run one test

    $ testrunner.py /sdk/path exampletests.test_example_app.ExampleAppTestHandlers testGet

To see usage help run testrunner.py without any arguments.

Code downloaded from: http://github.com/rzajac/gaeteststarter
@author: Rafal Zajac rzajac<at>gmail<dot>com
@copyright: Copyright 2007-2013 Rafal Zajac rzajac<at>gmail<dot>com. All rights reserved.
@license: Licensed under the MIT license
"""

import os
import sys
import logging
import unittest2

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

USAGE = """Usage: testrunner.py SDK_PATH TEST_PATH [TEST_METHOD]

Run unit tests for App Engine apps.

SDK_PATH    Path to the AppEngine SDK
TEST_PATH   Path to module / class containing tests
TEST_METHOD The name of the method to run

Examples:
  testrunner.py /sdk/path exampletests - run all tests in module
  testrunner.py /sdk/path exampletests.test_example_app - run all tests in a specific file
  testrunner.py /sdk/path exampletests.test_example_app.ExampleAppTestHandlers - run all rests in a class
  testrunner.py /sdk/path exampletests.test_example_app.ExampleAppTestHandlers testGet - run one test
"""


def main(sdk_path, test_path, test_method=None):

    os.environ['HTTP_HOST'] = "%s.appspot.com" % 'test-app'

    sys.path.insert(0, sdk_path)

    # Find RF GAE project root path
    gaeapp_path = os.path.dirname(os.path.realpath(__file__)) + '/..'
    gaeapp_path = os.path.realpath(gaeapp_path)

    sys.path.insert(0, gaeapp_path)

    import dev_appserver
    dev_appserver.fix_sys_path()

    suite, error = _create_suite(test_path, test_method)

    if error is None:
        logging.getLogger().setLevel(logging.INFO)
        unittest2.TextTestRunner(verbosity=2).run(suite)
    else:
        print error


def _create_suite(test_name, test_method=None):

    loader = unittest2.defaultTestLoader
    suite = unittest2.TestSuite()

    error = None

    try:
        tests = loader.loadTestsFromName(test_name)

        if len(list(tests.__iter__())) == 0:
            tests = loader.discover(test_name)

        if test_method:
            for test in tests:
                if test._testMethodName == test_method:
                    suite.addTest(test)
        else:
            suite.addTest(tests)

        if suite.countTestCases() == 0:
            raise Exception("'%s' is not found or does not contain any tests." % test_name)

    except Exception, e:
        print e
        error = str(e)

    return suite, error


if __name__ == '__main__':
    args = sys.argv
    arguments_length = len(args)

    if arguments_length > 4 or arguments_length < 3:
        print USAGE
        sys.exit(1)

    SDK_PATH = args[1]
    TEST_PATH = args[2]

    if arguments_length == 4:
        TEST_METHOD = args[3]
    else:
        TEST_METHOD = None

    main(SDK_PATH, TEST_PATH, TEST_METHOD)
