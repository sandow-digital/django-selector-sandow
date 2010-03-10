.. django-selector documentation master file, created by
   sphinx-quickstart on Sun Mar  7 23:04:33 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-selector
---------------

.. automodule:: dselector

.. highlight:: sh

You can install django-selector with pip::

    pip install django-selector

You can fork django-selector `from its hg repository
<http://dev.jmoiron.net/hg/django-selector>`_::

    hg clone http://dev.jmoiron.net/hg/django-selector

.. highlight:: python

Usage
-----

Here's an example of how a ``urls.py`` file might look when using 
django-selector::

    from django.contrib import admin
    from django.conf import settings
    import dselector

    admin.autodiscover()

    parser = dselector.Parser()
    urlpatterns = parser.patterns('',
        (r'admin/(.*)!', admin.site.root),
    )
    urlpatterns += parser.patterns('myblog',
        (r'blog/{page:digits}/', 'list', {}, 'blog-list'),
        (r'blog/{slug:slug}/', 'detail', {}, 'blog-detail'),
        (r'archive/{year:year}/', 'archive', {}, 'blog-year'),
        (r'archive/{year:year}/{month:month}/', 'archive', {}, 'blog-month'),
        (r'archive/{year:year}/{month:month}/{day:day}/', 'archive', {}, 'blog-day'),
        (r'comment/post/{content_type:slug}/{id:digits}/', 'comment_post', {}, 'comment-post'),
    )

    if settings.DEBUG:
        urlpatterns += parser.patterns('django.views.static',
            r('media/{path:any}', 'serve', {'document_root' : './media/'}),
        )

The primary way of denoting url parts with django-selector's parser is via the
named patterns syntax:  ``{name:pattern}``.  This is parsed into a regular
expression looking roughly like::

    '(?P<name>%s)' % (pattern_definition)

Refer to the :ref:`pattern-list` for a description of all default patterns.
You may optionally leave out the pattern, which will match against the
``segment`` pattern::

    (r'archive/{year}/{month:month}/{day}/', archive, {}, 'blog-day')

Beyond these preprocessing steps, django-selector's ``parser.patterns``
operates as the standard ``django.conf.urls.defaults.patterns``.

Autowrapping
~~~~~~~~~~~~

In addition to translating the shorthand named-pattern syntax to regex,
django-selector bookends your string with ``^`` and ``$``, as these are so
often required that it is often cleaner to assume they are implied.  When 
including another module's patterns (as in the ``admin`` example above), 
you may cancel the automatic ``$`` by adding a bang (``!``).  If for you
need a literal bang at the end of your url pattern, you may use ``!!``, but
in this case you will not get the autowrapped ``$``.

*New in django-selector 0.3*

Because django-selector happily ignores regular expressions and only translates
the named patterns it finds in the URL, it can be backwards compatible with
django's default ``url`` and url formats.  However, because of the inescapable
autowrapping, previous versions were not.  Versions >= ``0.3`` will now
automatically avoid autowrapping *any* pattern that either starts with a ``^``
*or* ends with a ``$``.

This buys the default operation a lot of backwards compatibility, but still
fails urls that are open-ended and lack a ``^`` at the begining.  To achieve
full backwards compatibility create your Parser with *autowrap=False*::

    parser = dselector.Parser(autowrap=False)

Or add this setting to your ``settings.py``::

    SELECTOR_AUTOWRAP=False

.. autoclass:: dselector.Parser
.. automethod:: dselector.Parser.patterns
.. automethod:: dselector.Parser.url

Defining your own named patterns
--------------------------------

You can define your own named patterns for use in your parser in two ways:

* you can initialize a parser with kwargs ``Parser(name=pattern, ...)``
* you can add patterns to a parser with ``Parser.register(name, pattern)``

.. automethod:: dselector.Parser.register


.. _pattern-list:

List of builtin named patterns
------------------------------

=========== ==============================  ===========================================
 name        regex                           description 
=========== ==============================  ===========================================
 word       ``r'\w+'``                       a single word
 alpha      ``r'[a-zA-Z]+'``                 alphabetic characters 
 digits     ``r'\d+'``                       digits
 number     ``r'\d*\.?\d+'``                 float or integer numbers
 chunk      ``r'[^/^.]+'``                   a 'chunk' of text (no /, ^, or .)
 segment    ``r'[^/]+'``                     a url segment (between /'s)
 any        ``r'.*'``                        anything;  good for paths
 year       ``r'\d{4}'``                     a 4 digit number
 month      ``r'(%s)' % '|'.join(months)``   textual abbreviated months (Jan, Feb, etc)
 day        ``r'\d{1,2}'``                   a one or two digit number
 slug       ``r'[a-zA-Z0-9\-]+'``            suitable for a "slug field"
=========== ==============================  ===========================================

**Note** that the default ``month`` pattern uses the locale-aware ``calendar``
module.  If you want to force a certain locale's months, you should either
set that locale or re-assign ``month`` in your parser via ``Parser.register``.

