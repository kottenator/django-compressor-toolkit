# django-compressor-toolkit

Set of plug-ins for [django-compressor](https://github.com/django-compressor/django-compressor/).

## Installation

```sh
pip install django-compressor-toolset
```

## Tools

### SCSS pre-compiler

Custom filter for [node-sass](https://github.com/sass/node-sass)
+ [Autoprefixer](https://github.com/postcss/autoprefixer) integration.

Add it to your settings:

```py
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'compressor_toolkit.precompilers.ScssFilter'),
)
```

What does it do:

- `node-sass input.scss output.css`
- `postcss --use autoprefixer -r output.css`

It also includes all the available static sources so you could import them in your SCSS code:

```css
/* auth/scss/login-page.scss */
@import "base/scss/variables";

.error-message {
    background-color: $primary-red-color;
}
```

… where `auth` and `base` - Django apps.
