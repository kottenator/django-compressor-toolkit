import os

from compressor.filters import CompilerFilter
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured


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


class SCSSFilter(CompilerFilter):
    """
    django-compressor pre-compiler for SCSS files.

    Consists of 2 steps:

    1. ``node-sass input.scss output.css``
    2. ``postcss --use autoprefixer -r output.css``
    """
    command = (
        'node-sass --output-style expanded {include-static} {infile} {outfile} && '
        'postcss --use autoprefixer --autoprefixer.browsers "ie >= 9, > 5%" -r {outfile}'
    )

    def __init__(self, content, attrs, *args, **kwargs):
        """
        Include all available 'static' dirs:

            node-sass --include-path path/to/app-1/static/ --include-path path/to/app-2/static/ ...

        So you can do imports inside your SCSS files:

            @import "app-1/scss/mixins";
            @import "app-2/scss/variables";

            .page-title {
                font-size: $title-font-size;
            }
        """
        static_dirs = get_all_static()

        self.options += (
            ('include-static', ' '.join(['--include-path {}'.format(s) for s in static_dirs])),
        )

        super(SCSSFilter, self).__init__(content, self.command, *args, **kwargs)


class ES6Filter(CompilerFilter):
    """
    django-compressor pre-compiler for ES6 files.

    Transforms ES6 to ES5 AMD module using ``babel``.
    """
    command = (
        'NPM_ROOT=`npm root -g` && '
        'babel --presets=$NPM_ROOT/babel-preset-es2015 '
        '--plugins=$NPM_ROOT/babel-plugin-transform-es2015-modules-amd '
        '--module-id={module-id} "{infile}" -o "{outfile}"'
    )

    def __init__(self, content, attrs, *args, **kwargs):
        """
        Add extra option for compiler:

            'module-id': 'app/script'

        That's AMD module ID for '/static/app/script.js' static file.
        """
        module_id = attrs.get('data-module-id')
        if not module_id:
            module_src = attrs.get('src')
            if not module_src:
                raise ImproperlyConfigured(
                    "Module should contain either \"data-module-id\" or \"src\" attribute"
                )
            module_id = os.path.splitext(module_src.replace(settings.STATIC_URL, ''))[0]

        self.options += (
            ('module-id', module_id),
        )

        super(ES6Filter, self).__init__(content, self.command, *args, **kwargs)
