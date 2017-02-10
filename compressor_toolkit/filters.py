import logging
import os
import re

from compressor.filters.css_default import CssAbsoluteFilter
from compressor.filters.datauri import CssDataUriFilter as BaseCssDataUriFilter
from django.apps import apps
from django.conf import settings


app_config = apps.get_app_config('compressor_toolkit')
logger = logging.getLogger(__file__)


class CssRelativeFilter(CssAbsoluteFilter):
    """
    Do similar to ``CssAbsoluteFilter`` URL processing
    but replace ``settings.COMPRESS_URL`` prefix with '../' * (N + 1),
    where N is the *depth* of ``settings.COMPRESS_OUTPUT_DIR`` folder.

    E.g. by default ``settings.COMPRESS_OUTPUT_DIR == 'CACHE'``,
    its depth N == 1, prefix == '../' * (1 + 1) == '../../'.

    If ``settings.COMPRESS_OUTPUT_DIR == 'my/compiled/data'``,
    its depth N == 3, prefix == '../' * (3 + 1) == '../../../../'.

    How does it work:

    - original file URL: '/static/my-app/style.css'
    - it has an image link: ``url(images/logo.svg)``
    - compiled file URL: '/static/CACHE/css/abcdef123456.css'
    - replaced image link URL: ``url(../../my-app/images/logo.svg)``
    """
    def add_suffix(self, url):
        url = super(CssRelativeFilter, self).add_suffix(url)
        old_prefix = self.url
        if self.has_scheme:
            old_prefix = '{}{}'.format(self.protocol, old_prefix)
        # One level up from 'css' / 'js' folder
        new_prefix = '..'
        # N levels up from ``settings.COMPRESS_OUTPUT_DIR``
        new_prefix += '/..' * len(list(filter(
            None, os.path.normpath(settings.COMPRESS_OUTPUT_DIR).split(os.sep)
        )))
        return re.sub('^{}'.format(old_prefix), new_prefix, url)


class CssDataUriFilter(BaseCssDataUriFilter):
    """
    Override default ``compressor.filters.datauri.CssDataUriFilter``:

    - fix https://github.com/django-compressor/django-compressor/issues/776
    - introduce new setting - ``COMPRESS_DATA_URI_PATH_PATTERN``,
      to filter only specific file paths or extensions,
      e.g. ``settings.COMPRESS_DATA_URI_PATH_PATTERN = '^.*\.svg$'``.
    """
    def input(self, filename=None, **kwargs):
        if not filename:
            return self.content
        # Store filename - we'll use it to build file paths
        self.filename = filename
        output = self.content
        for url_pattern in self.url_patterns:
            output = url_pattern.sub(self.data_uri_converter, output)
        return output

    def data_uri_converter(self, matchobj):
        url = matchobj.group(1).strip(' \'"')

        # Don't process URLs that start with: 'data:', 'http://', 'https://' and '/'.
        # We're interested only in relative URLs like 'images/icon.png' or '../images/icon.svg'
        if re.match('^(data:|https?://|/)', url):
            return

        file_path = self.get_file_path(url)

        # Process only specific file paths (optional)
        if hasattr(settings, 'COMPRESS_DATA_URI_PATH_PATTERN'):
            if not re.match(settings.COMPRESS_DATA_URI_PATH_PATTERN, file_path):
                return

        try:
            return super(CssDataUriFilter, self).data_uri_converter(matchobj)
        except OSError:
            logger.warning('"{}" file not found'.format(file_path))

        return "url('{}')".format(url)

    def get_file_path(self, url):
        file_path = re.sub('[#?].*$', '', url)
        return os.path.abspath(os.path.join(os.path.dirname(self.filename), file_path))
