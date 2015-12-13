# django-compressor-toolkit

[![Build Status](https://travis-ci.org/kottenator/django-compressor-toolkit.svg?branch=master)](https://travis-ci.org/kottenator/django-compressor-toolkit)

Set of add-ons for [django-compressor](https://github.com/django-compressor/django-compressor/)
that simply enables SCSS and ES6 in your Django project.

## Installation

```sh
pip install django-compressor-toolkit
```

## Add-ons

### SCSS pre-compiler

[SCSS](http://sass-lang.com/) is a great language that saves your time and brings joy to CSS development.

The add-on does next:
SCSS → (
[node-sass](https://github.com/sass/node-sass) +
[Autoprefixer](https://github.com/postcss/autoprefixer)
) → CSS.

It also enables Django static imports in SCSS:

```scss
/* app/scss/styles.scss */
@import "base/scss/variables";

.error-message {
  background-color: $primary-red-color;
  color: $white-color;
}
```

… where `app` and `base` - Django apps.

#### Usage

```py
// settings.py

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSFilter'),
)
```

```html
{# Django template #}

{% load compress %}

{% compress css %}
  <link type="text/x-scss" href="{% static 'app/scss/styles.scss' %}">
  <style type="text/x-scss">
    $link-color: #369;
    a {
      color: $link-color;
      &:focus, &:active {
        color: darken($link-color, 10);
      }
    }
  </style>
{% endcompress %}
```

You need `node-sass`, `postcss` and `autoprefixer` to be installed.

Quick install:

```sh
npm install -g node-sass postcss-cli autoprefixer
```

### ES6 AMD pre-compiler

ES6 is a new standard for JavaScript that brings
[great new features](https://hacks.mozilla.org/category/es6-in-depth/).

The standard was approved in July 2015 and not all modern browsers fully support it for now.
But there is a way to use it: transpilers that compile ES6 into good old ES5 syntax.

The add-on does next:
ES6 → (
[Babel](https://github.com/sass/node-sass) +
[AMD](https://github.com/amdjs/amdjs-api/blob/master/AMD.md)
) → ES5.

By default, AMD module ID is generated from file URL:
`{{ STATIC_URL }}app/js/module.js` → `app/js/module`,
but you can set it explicitly - see the example below.

#### Usage

```py
// settings.py

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6AMDFilter'),
)
```

```html
{# Django template #}

{% load compress %}

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.22/require.js"></script>

{% compress js %}
  <script type="module" src="{% static 'base/common.js' %}"></script>
  <script type="module" data-module-id="page/specific" src="{% static 'app/specific.js' %}"></script>
  <script type="module" data-module-id="page/inline">
    import { x } from 'base/common';
    export let y = x * 5;
  </script>
  <script>
    // entry point
    require(['base/common', 'page/specific', 'page/inline']);
  </script>
{% endcompress %}
```

You need `babel-cli`, `babel-preset-es2015` and `babel-plugin-transform-es2015-modules-amd` to be installed.

Quick install:

```sh
npm install -g babel-cli babel-preset-es2015 babel-plugin-transform-es2015-modules-amd
```
