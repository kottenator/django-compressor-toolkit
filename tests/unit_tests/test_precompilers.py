from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
import pytest

from compressor_toolkit.precompilers import SCSSFilter, ES6AMDFilter


def test_scss_filter():
    """
    Test ``compressor_toolkit.precompilers.SCSSFilter`` on simple SCSS input.
    """
    input_scss = '''
    .a {
        .b {
            padding: {
                left: 5px;
                right: 6px;
            }
        }
    }
    '''
    output_css = '.a .b {\n  padding-left: 5px;\n  padding-right: 6px;\n}\n'
    assert SCSSFilter(input_scss, None).input() == output_css


def test_es6_amd_filter():
    """
    Test ``compressor_toolkit.precompilers.ES6AMDFilter`` on simple ES6 input.
    """
    input_es6 = 'export let CONST = 1'
    output_js = (
        '"use strict";\n'
        '\n'
        'define("%s", ["exports"], function (exports) {\n'
        '  Object.defineProperty(exports, "__esModule", {\n'
        '    value: true\n'
        '  });\n'
        '  var CONST = exports.CONST = 1;\n'
        '});\n'
    )

    module_id = 'my-module'
    assert ES6AMDFilter(
        input_es6,
        {'data-module-id': module_id}
    ).input() == output_js % module_id

    module_url = static('my-app/sub/module.js')
    module_id = 'my-app/sub/module'
    assert ES6AMDFilter(
        input_es6,
        {'src': module_url}
    ).input() == output_js % module_id

    with pytest.raises(ImproperlyConfigured):
        ES6AMDFilter(input_es6, {}).input()
