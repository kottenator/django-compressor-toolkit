import os

from compressor.filters import CompilerFilter
from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files.temp import NamedTemporaryFile


app_config = apps.get_app_config('compressor_toolkit')


def get_all_static():
    """
    Get all the static files directories found by ``STATICFILES_FINDERS``

    :return: set of paths (top-level folders only)
    """
    static_dirs = set()

    for finder in settings.STATICFILES_FINDERS:
        finder = finders.get_finder(finder)

        if hasattr(finder, 'storages'):
            for storage in finder.storages.values():
                static_dirs.add(storage.location)

        if hasattr(finder, 'storage'):
            static_dirs.add(finder.storage.location)

    return static_dirs


class BaseCompiler(CompilerFilter):
    # Temporary input file extension
    infile_ext = ''

    def input(self, **kwargs):
        """
        Specify temporary input file extension.

        Browserify requires explicit file extension (".js" or ".json" by default).
        https://github.com/substack/node-browserify/issues/1469
        """
        if self.infile is None and "{infile}" in self.command:
            if self.filename is None:
                self.infile = NamedTemporaryFile(mode='wb', suffix=self.infile_ext)
                self.infile.write(self.content.encode(self.default_encoding))
                self.infile.flush()
                self.options += (
                    ('infile', self.infile.name),
                )
        return super(BaseCompiler, self).input(**kwargs)


class SCSSCompiler(BaseCompiler):
    """
    django-compressor pre-compiler for SCSS files.

    Consists of 2 steps:

    1. ``node-sass input.scss output.css``
    2. ``postcss --use autoprefixer -r output.css``

    Includes all available 'static' dirs:

        node-sass --include-path path/to/app-1/static/ --include-path path/to/app-2/static/ ...

    So you can do imports inside your SCSS files:

        @import "app-1/scss/mixins";
        @import "app-2/scss/variables";

        .page-title {
            font-size: $title-font-size;
        }
    """
    command = app_config.SCSS_COMPILER_CMD
    options = (
        ('node_sass_bin', app_config.NODE_SASS_BIN),
        ('postcss_bin', app_config.POSTCSS_BIN),
        ('paths', ' '.join(['--include-path {}'.format(s) for s in get_all_static()])),
        ('node_modules', app_config.NODE_MODULES),
        ('autoprefixer_browsers', app_config.AUTOPREFIXER_BROWSERS),
    )
    infile_ext = '.scss'


class ES6Compiler(BaseCompiler):
    """
    django-compressor pre-compiler for ES6 files.

    Transforms ES6 to ES5 using Browserify + Babel.

    Includes all available 'static' dirs:

        export NODE_PATH="path/to/app-1/static/:path/to/app-2/static/" && browserify ...

    So you can do imports inside your ES6 modules:

        import controller from 'app-1/page-controller';
        import { login, signup } from 'app-2/pages';

        controller.registerPages(login, signup);
    """
    command = app_config.ES6_COMPILER_CMD
    options = (
        ('browserify_bin', app_config.BROWSERIFY_BIN),
        ('paths', os.pathsep.join(get_all_static())),
        ('node_modules', app_config.NODE_MODULES)
    )
    infile_ext = '.js'
