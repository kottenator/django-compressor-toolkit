from compressor_toolkit.precompilers import ScssFilter


def test_scss_filter():
    """
    Test ``compressor_toolkit.precompilers.ScssFilter`` on simple SCSS input.
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
    assert ScssFilter(input, None).input() == output
