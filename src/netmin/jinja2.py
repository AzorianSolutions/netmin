from django.templatetags.static import static
from django.urls import reverse
from inspect import getmembers, isfunction
from jinja2 import Environment
from lib import jinja_filters, jinja_tests


class JinjaEnvironment(Environment):

    def __init__(self, **kwargs):
        super(JinjaEnvironment, self).__init__(**kwargs)

        # Load filter definitions
        for item in getmembers(jinja_filters):
            if not str(item[0]).startswith('_') and isfunction(item[1]):
                self.filters[item[0]] = item[1]

        # Load test definitions
        for item in getmembers(jinja_tests):
            if not str(item[0]).startswith('_') and isfunction(item[1]):
                self.tests[item[0]] = item[1]

        self.globals.update({
            'static': static,
            'url': reverse,
        })
