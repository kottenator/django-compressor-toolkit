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
    template = '''.a {{
      background: url('{}');
    }}
    '''
    input_css = template.format(original_url)
    output_css = template.format(processed_url)

    assert CssRelativeFilter(input_css).input(
        filename='/var/www/project/app/style.css',
        basename='app/style.css'
    ) == output_css


def test_css_data_uri_filter():
    """
    Test ``compressor_toolkit.filters.CssRelativeFilter``.
    """
    file_dir = os.path.join(TESTS_DIR, 'resources')
    file_path = os.path.join(file_dir, 'style.css')
    image_path = os.path.join(file_dir, 'images', 'icon.svg')

    with open(image_path, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read())

    input_css = '''
    .a {
      background: url(images/icon.svg);
    }
    '''

    output_css = '''
    .a {{
      background: url("data:image/svg+xml;base64,{}");
    }}
    '''.format(image_base64.decode())

    assert CssDataUriFilter(input_css).input(filename=file_path) == output_css
