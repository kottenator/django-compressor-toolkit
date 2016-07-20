from compressor_toolkit.precompilers import SCSSCompiler, ES6Compiler


def test_scss_compiler():
    """
    Test ``compressor_toolkit.precompilers.SCSSCompiler`` on simple SCSS input.
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
    output_css = '.a .b {\n  padding-left: 5px;\n  padding-right: 6px;\n}'
    assert SCSSCompiler(input_scss, {}).input().strip() == output_css


def test_es6_compiler():
    """
    Test ``compressor_toolkit.precompilers.ES6Compiler`` on simple ES6 input.
    """
    input_es6 = 'export let CONST = 1'
    output_es5 = (
        '"use strict";\n'
        '\n'
        'Object.defineProperty(exports, "__esModule", {\n'
        '  value: true\n'
        '});\n'
        'var CONST = exports.CONST = 1;\n'
    )
    assert output_es5 in ES6Compiler(input_es6, {}).input()
