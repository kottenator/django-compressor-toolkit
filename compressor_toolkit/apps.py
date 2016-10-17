import os

from django.apps.config import AppConfig
from django.conf import settings


class CompressorToolkitConfig(AppConfig):
    name = 'compressor_toolkit'

    LOCAL_NPM_INSTALL = getattr(settings, 'COMPRESS_LOCAL_NPM_INSTALL', True)

    # Path to 'node_modules' where browserify, babelify, autoprefixer, etc, are installed
    NODE_MODULES = getattr(
        settings,
        'COMPRESS_NODE_MODULES',
        os.path.abspath('node_modules') if LOCAL_NPM_INSTALL else '/usr/lib/node_modules'
    )

    # node-sass executable
    NODE_SASS_BIN = getattr(
        settings,
        'COMPRESS_NODE_SASS_BIN',
        'node_modules/.bin/node-sass' if LOCAL_NPM_INSTALL else 'node-sass'
    )

    # postcss executable
    POSTCSS_BIN = getattr(
        settings,
        'COMPRESS_POSTCSS_BIN',
        'node_modules/.bin/node-sass' if LOCAL_NPM_INSTALL else 'postcss'
    )

    # Browser versions config for Autoprefixer
    AUTOPREFIXER_BROWSERS = getattr(settings, 'COMPRESS_AUTOPREFIXER_BROWSERS', 'ie >= 9, > 5%')

    # Custom SCSS transpiler command
    SCSS_COMPILER_CMD = getattr(settings, 'COMPRESS_SCSS_COMPILER_CMD', (
        '{node_sass_bin} --output-style expanded {paths} "{infile}" > "{outfile}" && '
        '{postcss_bin} --use "{node_modules}/autoprefixer" '
        '--autoprefixer.browsers "{autoprefixer_browsers}" -r "{outfile}"'
    ))

    # browserify executable
    BROWSERIFY_BIN = getattr(
        settings,
        'COMPRESS_BROWSERIFY_BIN',
        'node_modules/.bin/browserify' if LOCAL_NPM_INSTALL else 'browserify'
    )

    # Custom ES6 transpiler command
    ES6_COMPILER_CMD = getattr(settings, 'COMPRESS_ES6_COMPILER_CMD', (
        'export NODE_PATH="{paths}" && '
        '{browserify_bin} "{infile}" -o "{outfile}" '
        '-t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-es2015" ]'
    ))
