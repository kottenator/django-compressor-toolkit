from django.conf import settings
from django.contrib.staticfiles import finders
from compressor.filters import CompilerFilter


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


class ScssFilter(CompilerFilter):
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
        super().__init__(content, self.command, *args, **kwargs)
