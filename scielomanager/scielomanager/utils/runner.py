"""
An alternative Django ``TEST_RUNNER`` which uses unittest2 test discovery from
a base path specified in settings, rather than requiring all tests to be in
``tests`` module of an app.

If you just run ``./manage.py test``, it'll discover and run all tests
underneath the ``TEST_DISCOVERY_ROOT`` setting (a path). If you run
``./manage.py test full.dotted.path.to.test_module``, it'll run the tests in
that module (you can also pass multiple modules).

And (new in this updated version), if you give it a single dotted path to a
package, and that package does not itself directly contain any tests, it'll do
test discovery in all sub-modules of that package.

This code doesn't modify the default unittest2 test discovery behavior, which
only searches for tests in files named "test*.py".

"""
import logging
import warnings
from django.conf import settings
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django.utils.importlib import import_module
from django.utils.unittest.loader import defaultTestLoader
from scielomanager.tools import get_setting_or_raise


DISABLE_LOGGING_BELOW_LEVEL = get_setting_or_raise('DISABLE_LOGGING_BELOW_LEVEL')


class DiscoveryRunner(DjangoTestSuiteRunner):

    def setup_test_environment(self, **kwargs):
        if DISABLE_LOGGING_BELOW_LEVEL:
            level = getattr(logging, DISABLE_LOGGING_BELOW_LEVEL)
            logging.disable(level)
            warnings.warn(
                "Loggings has beed disabled below level: %s" % DISABLE_LOGGING_BELOW_LEVEL
            )
        return super(DiscoveryRunner, self).setup_test_environment(**kwargs)

    """A test suite runner that uses unittest2 test discovery."""
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = None
        discovery_root = settings.TEST_DISCOVERY_ROOT

        if test_labels:
            suite = defaultTestLoader.loadTestsFromNames(test_labels)
            # if single named module has no tests, do discovery within it
            if not suite.countTestCases() and len(test_labels) == 1:
                suite = None
                discovery_root = import_module(test_labels[0]).__path__[0]

        if suite is None:
            suite = defaultTestLoader.discover(
                discovery_root,
                top_level_dir=settings.BASE_PATH,
                )

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))
