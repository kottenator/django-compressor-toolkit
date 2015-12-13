from django.core.urlresolvers import reverse


def test_view_with_scss_file(client, assert_precompiled):
    """
    Test view that renders *SCSS file* that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    :param assert_precompiled: custom fixture that asserts pre-compiled content
    """
    response = client.get(reverse('scss-file'))
    assert response.status_code == 200
    assert_precompiled(
        'app/layout.scss',
        'css',
        '.title {\n  font: bold 30px Arial, sans-serif;\n}\n'
    )


def test_view_with_inline_scss(client):
    """
    Test view that renders *inline SCSS* that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get(reverse('scss-inline'))
    assert response.status_code == 200
    assert b'<style type="text/css">' \
           b'.title {\n  font: bold 30px Arial, sans-serif;\n}\n' \
           b'</style>' in response.content


def test_view_with_es6_file(client, assert_precompiled):
    """
    Test view that renders *ES6 file* into *ES5 AMD*.

    :param client: ``pytest-django`` fixture: Django test client
    :param assert_precompiled: custom fixture that asserts pre-compiled content
    """
    response = client.get(reverse('es6-file'))
    assert response.status_code == 200
    assert_precompiled(
        'app/scripts.js',
        'js',
        (
            '\'use strict\';\n'
            '\n'
            'define(\'app/scripts\', [\'base/framework\'], function (_framework) {\n'
            '  var _framework2 = _interopRequireDefault(_framework);\n'
            '\n'
            '  function _interopRequireDefault(obj) {\n'
            '    return obj && obj.__esModule ? obj : {\n'
            '      default: obj\n'
            '    };\n'
            '  }\n'
            '\n'
            '  new _framework2.default();\n'
            '  new _framework2.default(\'1.0.1\');\n'
            '});\n'
        )
    )


def test_view_with_inline_es6(client):
    """
    Test view that renders *inline ES6* into *ES5 AMD*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get(reverse('es6-inline'))
    assert response.status_code == 200
    assert b'<script type="text/javascript">"use strict";\n' \
           b'\n' \
           b'define("inline/utils", ["exports"], function (exports) {\n' \
           b'      Object.defineProperty(exports, "__esModule", {\n' \
           b'            value: true\n' \
           b'      });\n' \
           b'\n' \
           b'      var square = exports.square = function square(x) {\n' \
           b'            return x * x;\n' \
           b'      };\n' \
           b'});\n' \
           b'</script>' in response.content
