import base64
import os
import pytest

from compressor_toolkit.filters import CssRelativeFilter, CssDataUriFilter

from tests.utils import TESTS_DIR


@pytest.mark.parametrize('original_url, processed_url', [
    ('images/icon.svg', '../../app/images/icon.svg'),
    ('./images/icon.svg', '../../app/images/icon.svg'),
    ('../images/icon.svg', '../../images/icon.svg'),
    ('/images/icon.svg', '/images/icon.svg')
], ids=['letter', 'one dot', 'two dots', 'slash'])
def test_css_relative_url_filter(original_url, processed_url):
    """
    Test ``compressor_toolkit.filters.CssRelativeFilter``.

    :param original_url: Test function parameter: URL in the original CSS file
                         which is located in '$PROJECT_ROOT/app/static/app/style.css'
                         and will be collected to '$STATIC_ROOT/app/style.css'
    :param processed_url: Test function parameter: URL in the processed CSS file
                          which is located in '$STATIC_ROOT/CACHE/css/abcd1234.css'
    """
    template = '''
    .a {{
      background: url('{}');
    }}
    '''
    input_css = template.format(original_url)
    output_css = template.format(processed_url)

    # ``filename`` and ``basename`` are fakes - file existence doesn't matter for this test
    # ``filename`` must be not empty to make the filter work
    # ``basename`` contains Django app name 'app', which will be a part of the output URL
    assert CssRelativeFilter(input_css).input(
        filename='...',
        basename='app/style.css'
    ) == output_css


@pytest.mark.parametrize('image_path, is_processed', [
    ('images/icon.svg', True),
    ('images/icon.png', True),
    ('images/icon.jpg', False),
    ('images/skip/icon.svg', False),
    ('images/large.svg', False)
], ids=['ok svg', 'ok png', 'skip jpg', 'skip folder', 'skip large'])
def test_css_data_uri_filter(settings, image_path, is_processed):
    """
    Test ``compressor_toolkit.filters.CssRelativeFilter``.

    :param settings: ``pytest-django`` fixture: mutable Django settings
    :param image_path: Test function parameter: relative path to the image file
    :param is_processed: Test function parameter: is data URI transformation applied?
    """
    # configure related settings
    settings.COMPRESS_DATA_URI_MAX_SIZE = 5 * 1024
    settings.COMPRESS_DATA_URI_INCLUDE_PATHS = '.+\.(svg|png)$'
    settings.COMPRESS_DATA_URI_EXCLUDE_PATHS = '/skip/'

    file_dir = os.path.join(TESTS_DIR, 'resources')
    file_path = os.path.join(file_dir, 'style.css')

    if is_processed:
        with open(os.path.join(file_dir, image_path), 'rb') as image_file:
            processed_image = 'data:image/{};base64,{}'.format(
                'svg+xml' if image_path.endswith('.svg') else 'png',
                base64.b64encode(image_file.read()).decode()
            )
    else:
        processed_image = image_path

    template = '''
    .a {{
      background: url("{}");
    }}
    '''
    input_css = template.format(image_path)
    output_css = template.format(processed_image)

    assert CssDataUriFilter(input_css).input(filename=file_path) == output_css
