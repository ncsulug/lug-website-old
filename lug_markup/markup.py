# -*- coding: utf-8 -*-
from creoleparser.core import Parser
from creoleparser.dialects import create_dialect, creole11_base, parse_args
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

global_cache = {}

# This includes Markdown-style backticks for inline code.
INLINE_MARKUP = [
    ('**','strong'),    ('//','em'),        (',,','sub'),
    ('^^','sup'),       ('__','u'),         ('##','code'),
    ('`', 'code')
]

def build_interwikis():
    from django.conf import settings
    bases, spaces, classes = {}, {}, {}
    for name, (base, space) in getattr(settings, 'INTERWIKIS', {}).items():
        bases[name] = base
        spaces[name] = space
        classes[name] = lambda page: name + '-link'
    return bases, spaces, classes


def wiki_link_path(link):
    if link.startswith("~"):
        # User profile
        return reverse('profile', args=[link[1:]])
    else:
        # TODO: Make this actually do wiki links
        return link


def wiki_link_class(link):
    if link.startswith("~"):
        return 'user-link'
    else:
        return 'wiki-link'


def create_lug_dialect():
    iw_bases, iw_spaces, iw_classes = build_interwikis()

    return create_dialect(creole11_base,
        # Markup customizations
        simple_markup = INLINE_MARKUP,
        indent_style = '',
        indent_class = 'quote',
        no_wiki_monospace = False,
        # Internal links
        wiki_links_base_url = "",
        wiki_links_path_func = wiki_link_path,
        wiki_links_class_func = wiki_link_class,
        # Everyone else's links
        external_links_class = 'external-link',
        interwiki_links_base_urls = iw_bases,
        interwiki_links_class_funcs = iw_classes,
        interwiki_links_space_chars = iw_spaces
    )


def get_parser():
    if 'parser' not in global_cache:
        global_cache['parser'] = Parser(dialect=create_lug_dialect(),
                                        method='html')
    return global_cache['parser']


def render_markup(text):
    return mark_safe(get_parser().render(text))

