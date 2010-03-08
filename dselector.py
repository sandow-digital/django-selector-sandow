#!/usr/bin/env python

"""A Django "port" of Luke Arno's "Selector".

To use, create an instance of Parser in your urls.py.  Parser has special
implementations of the 'patterns' and 'url' functions that essentially
parse pattern urls into regular expressions, and pass them to the builtin
django functions.  Using pattern urls, your urls become more about _what_
they are matching rather than about _how_ they are matching it:

    patterns('foo.views',
        (r'^/(?P<name>[a-zA-Z0-9\-]+)/(?P<foos>\d*.?\d+)/$', 'index', {}, 'foo-index')

becomes, via patterns:

    parser.patterns('foo.views', (r'/{name:slug}/{foos:num}/', 'index', {}, 'foo-index'))

In addition to the builtin patterns (check `pattern_types`), you may also
register additional patterns to an instantiated parser in your URLs module,
or subclass Parser and add them to use throughout your application.

You can optionally end a smart pattern with '!' if you do not want to have
the trailing $ appended (for use in application entry points).  To end with
a literal '!', use '!!'.

DSelector is distributed under the MIT license.
"""

import re
from django.conf.urls.defaults import url as django_url
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

import calendar

__all__ = ['pattern_types', 'Parser']

pattern_types = {
    'word'      : r'\w+',
    'alpha'     : r'[a-zA-Z]+',
    'digits'    : r'\d+',
    'number'    : r'\d*.?\d+',
    'chunk'     : r'[^/^.]+',
    'segment'   : r'[^/]+',
    'any'       : r'.*',
    # common url pieces
    'year'      : r'\d{4}',
    'month'     : r'(%s)' % '|'.join(calendar.month_abbr[1:]),
    'day'       : r'\d{1,2}',
    'slug'      : r'[a-zA-Z0-9\-]+',
}

pattern_re = re.compile(r'{(?P<name>\w+):?(?P<pattern>\w+)?}')
re_template = r'(?P<%s>%s)'
re_findstr  = r'{%(name)s:%(pattern)s}'

class Parser:
    def __init__(self, **extra_patterns):
        self.pattern_types = pattern_types.copy()
        for key, val in extra_patterns.iteritems():
            self.pattern_types[key] = val

    def register(self, name, regex):
        """Registers a new pattern or overrides an old one."""
        # sanity check
        re.compile(regex)
        self.pattern_types[name] = regex
        return True

    def parse_pattern(self, pat):
        """Parses a pattern to a full regex. Surrounds pattern w/ ^ & $, and
        replaces the embedded patterns with regexes."""
        matches = [m.groupdict() for m in pattern_re.finditer(pat)]
        for match in matches:
            # {'pattern': p, 'name': n}
            p, n = match['pattern'], match['name']
            if p is None:
                p = 'segment'
                findstr = '{%s}' % n
            else:
                findstr = re_findstr % match
            replacement = re_template % (n, self.pattern_types[p])
            pat = pat.replace(findstr, replacement)
        pat = ('^%s$' % pat) if not pat.endswith('!') else ('^%s' % pat[:-1])
        return pat

    def patterns(self, prefix, *args):
        """A replacement 'patterns' that implements smart url groups."""
        pattern_list = []
        for t in args:
            if isinstance(t, (list, tuple)):
                t = self.url(prefix=prefix, *t)
            elif isinstance(t, RegexURLPattern):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list

    def url(self, regex, view, kwargs=None, name=None, prefix=''):
        """A replacement for 'url' that understands smart url groups."""
        regex = self.parse_pattern(regex)
        return django_url(regex, view, kwargs, name, prefix)

