import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
SECRET_KEY = '*****'
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'compressor',
    'compressor_toolkit',
    'test_project.base',
    'test_project.app'
)
ROOT_URLCONF = 'test_project.urls'
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)
MIDDLEWARE_CLASSES = ()
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.static',
)
COMPRESS_ROOT = os.path.join(BASE_DIR, 'compressor')
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    ('module', 'compressor_toolkit.precompilers.ES6Compiler')
)
COMPRESS_ENABLED = False

# path to folder with installed Node.js packages
# auto-detect it for test purposes
COMPRESS_NODE_PACKAGES = '`npm root -g`'
