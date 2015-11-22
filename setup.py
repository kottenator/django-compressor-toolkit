from setuptools import setup

setup(
    name='django-compressor-toolkit',
    version='0.0.1',
    description='Set of plug-ins for django-compressor',
    url='https://github.com/kottenator/django-compressor-toolkit',
    author='Rostyslav Bryzgunov',
    author_email='kottenator@gmail.com',
    license='MIT',
    include_package_data=True,
    setup_requires=[
        'setuptools-git'
    ],
    install_requires=[
        'django-compressor~=1.5'
    ],
    extras_require={
        'test': [
            'django',
            'pytest',
            'pytest-django',
            'pytest-cov'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
