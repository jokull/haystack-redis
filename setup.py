# -*- coding: utf-8 -*-
"""
haystack-redis
~~~~~~~~~~~~~~~~~~~~~~

A Whoosh storage engine using redis for persistance. A Haystack
``SearchBackend``  subclass is also provided. Normally the ``STORAGE`` key could
just be set but Haystack 2.0.0alpha is only aware of ``file`` and ``ram``
backends.

This is especially useful for small sites hosted on Heroku, which does not allow
writing to local disk. The ``REDISTOGO_URL`` environment variable is read,
falling back to the localhost default port.

Usage
-----

Configure your Haystack connections in ``settings.py``::

    import tempfile
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack_redis.RedisEngine',
            'PATH': tempfile.gettempdir(),
        },
    }

"""

from setuptools import setup

setup(
    name='haystack-redis',
    version='0.0.0',
    url='https://github.com/jokull/haystack-redis',
    license='BSD',
    author=u'Jökull Sólberg Auðunsson',
    author_email='jokull@solberg.is',
    description='Use redis as a persistance layer for Whoosh and Haystack',
    long_description=__doc__,
    py_modules=['haystack_redis'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
