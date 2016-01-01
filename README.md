# django-compressor-toolkit

[![Build Status](https://travis-ci.org/kottenator/django-compressor-toolkit.svg?branch=master)](https://travis-ci.org/kottenator/django-compressor-toolkit)

Set of add-ons for [django-compressor](https://github.com/django-compressor/django-compressor/)
that simply enables SCSS and ES6 in your Django project.

## Installation

```sh
pip install django-compressor-toolkit
```

```py
// settings.py

INSTALLED_APPS += ('compressor_toolkit',)
```

## Add-ons

### SCSS pre-compiler

[SCSS](http://sass-lang.com/) is a great language that saves your time and brings joy to CSS development.

The add-on does next:
SCSS → (
[node-sass](https://github.com/sass/node-sass) +
[Autoprefixer](https://github.com/postcss/autoprefixer)
) → CSS.

It also enables Django static imports in SCSS, see the example below.

#### Usage

```py
// settings.py

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
)
```

```html
{# Django template #}

{% load compress %}

{% compress css %}
  <link type="text/x-scss" href="{% static 'app/layout.scss' %}">
{% endcompress %}
```

```scss
/* app/static/app/layout.scss */

@import "base/variables";

.title {
  font: bold $title-size Arial, sans-serif;
}
```

```scss
/* base/static/base/variables.scss */

$title-size: 30px;
```

#### Requisites

You need `node-sass`, `postcss-cli` and `autoprefixer` to be installed. Quick install:

```sh
npm install -g node-sass postcss-cli autoprefixer
```

### ES6 pre-compiler

ES6 is a new standard for JavaScript that brings
[great new features](https://hacks.mozilla.org/category/es6-in-depth/).

The standard was approved in July 2015 and not all modern browsers fully support it for now.
But there is a way to use it: transpilers that compile ES6 into good old ES5 syntax.

The add-on does next:
ES6 → (
[Browserify](http://browserify.org/) +
[Babelify](https://github.com/babel/babelify)
) → ES5.

It also enables Django static imports in ES6, see the example below.

#### Usage

```py
// settings.py

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
)
```

```html
{# Django template #}

{% load compress %}

{% compress js %}
  <script type="module" src="{% static 'app/scripts.js' %}"></script>
{% endcompress %}
```

```js
// app/static/app/scripts.js

import Framework from 'base/framework';

new Framework;
new Framework('1.0.1');
```

```js
// base/static/base/framework.js

export let version = '1.0';

export default class {
  constructor(customVersion) {
    console.log(`Framework v${customVersion || version} initialized`);
  }
}
```

#### Requisites

You need `browserify`, `babelify` and `babel-preset-es2015` to be installed. Quick install:

```sh
npm install -g browserify babelify babel-preset-es2015
```

## Django settings

### `COMPRESS_NODE_MODULES`

Path to `node_modules` where `browserify`, `babelify`, `autoprefixer`, etc, are installed.

Default: `/usr/lib/node_modules`

### `COMPRESS_SCSS_COMPILER_CMD`

Command that will be executed to transform SCSS into CSS code.

Default:

```sh
node-sass --output-style expanded {paths} "{infile}" "{outfile}" &&
postcss --use "{node_modules}/autoprefixer" --autoprefixer.browsers "{autoprefixer_browsers}" -r "{outfile}"
```

Placeholders:
- `{infile}` - input file path
- `{outfile}` - output file path
- `{paths}` - specially for `node-sass`, include all Django app static folders:
  `--include-path=/path/to/app-1/static/ --include-path=/path/to/app-2/static/ ...`
- `{node_modules}` - see `COMPRESS_NODE_MODULES` setting
- `{autoprefixer_browsers}` - see `COMPRESS_AUTOPREFIXER_BROWSERS` setting

### `COMPRESS_AUTOPREFIXER_BROWSERS`

Browser versions config for Autoprefixer.

Default: `ie >= 9, > 5%`

### `COMPRESS_ES6_COMPILER_CMD`

Command that will be executed to transform ES6 into ES5 code.

Default:

```sh
export NODE_PATH="{paths}" && browserify "{infile}" -o "{outfile}" --no-bundle-external --node
-t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-es2015" ]
```

Placeholders:
- `{infile}` - input file path
- `{outfile}` - output file path
- `{paths}` - specially for `browserify`, include all Django app static folders:
  `/path/to/app-1/static/:/path/to/app-2/static/:...` (like `PATH` variable)
- `{node_modules}` - see `COMPRESS_NODE_MODULES` setting

## Contribute and test

```sh
git clone https://github.com/kottenator/django-compressor-toolkit.git
cd django-compressor-toolkit
pip install -e .[test]
py.test
```
