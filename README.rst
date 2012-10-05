haystack-redis
~~~~~~~~~~~~~~

A Whoosh storage engine using redis for persistance. A Haystack
``SearchBackend``  subclass is also provided. Normally the ``STORAGE`` key could
just be set but Haystack 2.0.0beta is only aware of ``file`` and ``ram``
backends.

This is especially useful for small sites hosted on Heroku, which does not allow
writing to local disk. The ``REDISTOGO_URL`` environment variable is read,
falling back to the localhost default port.

Code is based on maxpert_’s snippet (see blog post_)

.. _maxpert: https://github.com/maxpert
.. _post: http://blog.creapptives.com/post/32262168370/python-whoosh-with-redis-storage

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

Installation
------------

Currently some in-development features are still needed::

    $ pip install -e git+https://github.com/andymccurdy/redis-py.git@master@egg=redis
    $ pip install -e git+https://github.com/toastdriven/django-haystack.git@master#egg=django-haystack
    $ pip install -e git+https://github.com/jokull/haystack-redis-backend.git@master#egg=haystack-redis-engine
