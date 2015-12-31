from django.apps.config import AppConfig
from django.conf import settings


class CompressorToolkitConfig(AppConfig):
    name = 'compressor_toolkit'

    # Custom SCSS transpiler command
    SCSS_COMPILER_CMD = getattr(settings, 'COMPRESS_SCSS_COMPILER_CMD', None)

    # Custom ES6 transpiler command
    ES6_COMPILER_CMD = getattr(settings, 'COMPRESS_ES6_COMPILER_CMD', None)

    # Path to 'node_modules' where browserify, babelify, autoprefixer, etc, are installed
    NODE_MODULES = getattr(settings, 'COMPRESS_NODE_MODULES', None) or '/usr/lib/node_modules'
