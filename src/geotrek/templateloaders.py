# -*- coding: utf-8 -*-

from os.path import dirname, join, abspath, isdir

from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app
from django.template import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as BaseLoader


class Loader(BaseLoader):
    """
    Specify wich app to use to extends template
       ex: mapentity/base.html : {% extends "mapentity:mapentity/base.html" %}
           to force extends original base.html and stop recursive error
    """

    def _get_template_vars(self, template_name):
        app_name, template_name = template_name.split(":", 1)
        try:
            template_dir = abspath(join(dirname(get_app(app_name).__file__), 'templates'))

        except ImproperlyConfigured:
            raise TemplateDoesNotExist()

        return template_name, template_dir

    def load_template_source(self, template_name, template_dirs=None):
        if ":" not in template_name:
            raise TemplateDoesNotExist()

        template_name, template_dir = self._get_template_vars(template_name)

        if not isdir(template_dir):
            raise TemplateDoesNotExist()

        return super(Loader, self).load_template_source(template_name, template_dirs=[template_dir])
    load_template_source.is_usable = True
