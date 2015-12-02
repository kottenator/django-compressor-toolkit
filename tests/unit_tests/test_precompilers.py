from compressor_toolkit.precompilers import SCSSFilter, ES6AMDFilter


def test_scss_filter():
    """
    Test ``compressor_toolkit.precompilers.SCSSFilter`` on simple SCSS input.
    """
    input = '''
    .a {
        .b {
            padding: {
                left: 5px;
                right: 6px;
            }
        }
    }
    '''

    output = '.a .b {\n  padding-left: 5px;\n  padding-right: 6px;\n}\n'
    assert SCSSFilter(input, None).input() == output


def test_es6_amd_filter():
    """
    Test ``compressor_toolkit.precompilers.ES6AMDFilter`` on simple ES6 input.
    """
    input = 'export let CONST = 1'
    output = '"use strict";\n' \
             '\n' \
             'define("my-module", ["exports"], function (exports) {\n' \
             '  Object.defineProperty(exports, "__esModule", {\n' \
             '    value: true\n' \
             '  });\n' \
             '  var CONST = exports.CONST = 1;\n' \
             '});\n'
    assert ES6AMDFilter(input, {'data-module-id': 'my-module'}).input() == output
