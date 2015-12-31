from setuptools import setup

import compressor_toolkit


setup(
    name='django-compressor-toolkit',
    version=compressor_toolkit.__version__,
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
            'pytest-cov',
            'pytest-pythonpath'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
