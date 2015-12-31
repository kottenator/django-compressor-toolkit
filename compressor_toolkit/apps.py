from django.apps.config import AppConfig
from django.conf import settings


class CompressorToolkitConfig(AppConfig):
    name = 'compressor_toolkit'

    # Path to 'node_modules' where browserify, babelify, autoprefixer, etc, are installed
    NODE_MODULES = getattr(settings, 'COMPRESS_NODE_MODULES', None) or '/usr/lib/node_modules'

    # Custom SCSS transpiler command
    SCSS_COMPILER_CMD = getattr(settings, 'COMPRESS_SCSS_COMPILER_CMD', None) or (
        'node-sass --output-style expanded {paths} "{infile}" "{outfile}" && '
        'postcss --use "{node_modules}/autoprefixer" '
        '--autoprefixer.browsers "{autoprefixer_browsers}" -r "{outfile}"'
    )

    # Browser versions config for Autoprefixer
    AUTOPREFIXER_BROWSERS = getattr(settings, 'COMPRESS_AUTOPREFIXER_BROWSERS', None) or (
        'ie >= 9, > 5%'
    )

    # Custom ES6 transpiler command
    ES6_COMPILER_CMD = getattr(settings, 'COMPRESS_ES6_COMPILER_CMD', None) or (
        'export NODE_PATH="{paths}" && '
        'browserify "{infile}" -o "{outfile}" --no-bundle-external --node '
        '-t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-es2015" ]'
    )
