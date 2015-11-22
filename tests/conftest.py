import os

from django.conf import settings


def pytest_configure():
    tests_dir = os.path.dirname(__file__)

    settings.configure(
        DEBUG=True,
        SECRET_KEY='*****',
        INSTALLED_APPS=(
            'django.contrib.staticfiles',
            'compressor',
            'compressor_toolkit',
            'tests.project.base',
            'tests.project.home'
        ),
        ROOT_URLCONF='tests.project.urls',
        STATIC_URL='/static/',
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'compressor.finders.CompressorFinder'
        ),
        COMPRESS_ROOT=os.path.join(tests_dir, 'compress-static'),
        COMPRESS_PRECOMPILERS=(
            ('text/x-scss', 'compressor_toolkit.precompilers.ScssFilter'),
        ),
        COMPRESS_ENABLED=False
    )
