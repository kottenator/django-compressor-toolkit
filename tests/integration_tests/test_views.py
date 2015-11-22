def test_inline_import(client):
    """
    Test view that renders template that contains *inline SCSS*
    that *imports SCSS* file from *another Django app*.

    :param client: ``pytest-django`` fixture: Django test client
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'font: bold 30px Arial, sans-serif;' in response.content
