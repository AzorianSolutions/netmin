from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment
from netmin.lib.jinja_tests import in_list


class JinjaEnvironment(Environment):

    def __init__(self, **kwargs):
        super(JinjaEnvironment, self).__init__(**kwargs)
        self.tests['in_list'] = in_list
        self.globals.update({
            'static': static,
            'url': reverse,
        })
