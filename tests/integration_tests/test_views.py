from django.core.urlresolvers import reverse


def test_view_with_scss_file(client, assert_precompiled):
    """
    Test view that renders template that *includes SCSS file*
    that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    :param assert_precompiled: custom ``pytest`` fixture that compares pre-compiled
                               by ``django-compressor`` content with expected content
    """
    response = client.get(reverse('scss-file'))
    assert response.status_code == 200
    assert_precompiled(
        'app/layout.scss',
        'css',
        '.title {\n  margin: 0;\n  padding: 0;\n  font: bold 30px Arial, sans-serif;\n}\n'
    )


def test_view_with_inline_scss(client):
    """
    Test view that renders template that contains *inline SCSS*
    that *imports SCSS file from another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get(reverse('inline-scss'))
    assert response.status_code == 200
    assert b'font: bold 30px Arial, sans-serif;' in response.content
