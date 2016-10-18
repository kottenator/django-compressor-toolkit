import re

from django.core.urlresolvers import reverse


def test_view_with_scss_file(client, precompiled):
    """
    Test view that renders *SCSS file* that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    :param precompiled: custom fixture that asserts pre-compiled content
    """
    response = client.get(reverse('scss-file'))
    assert response.status_code == 200
    assert precompiled('app/layout.scss', 'css').strip() == \
        '.title {\n  font: bold 30px Arial, sans-serif;\n}'


def test_view_with_inline_scss(client):
    """
    Test view that renders *inline SCSS* that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get(reverse('scss-inline'))
    assert response.status_code == 200
    assert re.search(
        r'<style type="text/css">.title \{\n\s*font: bold 30px Arial, sans-serif;\n\}\s*</style>',
        response.content.decode('utf8')
    )


def test_view_with_es6_file(client, precompiled):
    """
    Test view that renders *ES6 file* into *ES5 file*.

    :param client: ``pytest-django`` fixture: Django test client
    :param precompiled: custom fixture that asserts pre-compiled content
    """
    response = client.get(reverse('es6-file'))
    assert response.status_code == 200
    assert precompiled('app/scripts.js', 'js') == (
        '(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=='
        '"function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f='
        'new Error("Cannot find module \'"+o+"\'");throw f.code="MODULE_NOT_FOUND",f}'
        'var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];'
        'return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=='
        '"function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:['
        'function(require,module,exports){\n'
        '\'use strict\';\n'
        '\n'
        'var _framework = require(\'base/framework\');\n'
        '\n'
        'var _framework2 = _interopRequireDefault(_framework);\n'
        '\n'
        'function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : '
        '{ default: obj }; }\n'
        '\n'
        'new _framework2.default();\n'
        'new _framework2.default(\'1.0.1\');\n'
        '\n'
        '},{"base/framework":2}],2:[function(require,module,exports){\n'
        '\'use strict\';\n'
        '\n'
        'Object.defineProperty(exports, "__esModule", {\n'
        '  value: true\n'
        '});\n'
        '\n'
        'function _classCallCheck(instance, Constructor) {'
        ' if (!(instance instanceof Constructor)) {'
        ' throw new TypeError("Cannot call a class as a function"); } }\n'
        '\n'
        'var version = exports.version = \'1.0\';\n'
        '\n'
        'var _class = function _class(customVersion) {\n'
        '  _classCallCheck(this, _class);\n'
        '\n'
        '  console.log(\'Framework v\' + (customVersion || version) + \' initialized\');\n'
        '};\n'
        '\n'
        'exports.default = _class;\n'
        '\n'
        '},{}]},{},[1]);\n'
    )


def test_view_with_inline_es6(client):
    """
    Test view that renders *inline ES6* into *inline ES5*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get(reverse('es6-inline'))
    assert response.status_code == 200
    assert b'"use strict";\n' \
           b'\n' \
           b'var square = function square(x) {\n' \
           b'      return x * x;\n' \
           b'};\n'\
           b'console.log("Square of 2:", square(2));' in response.content
