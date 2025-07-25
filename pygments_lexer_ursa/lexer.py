"""
    pygments.lexers.ursa
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for Ursa.

    :copyright: Copyright 2006-2024 by the Pygments team.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import include, RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace
import pygments.unistring as uni

__all__ = ['CustomLexer']

URSA_IDENT_START = ('(?:[$_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') +
                  ']|\\\\u[a-fA-F0-9]{4})')
URSA_IDENT_PART = ('(?:[$' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl',
                                       'Mn', 'Mc', 'Nd', 'Pc') +
                 '\u200c\u200d]|\\\\u[a-fA-F0-9]{4})')
URSA_IDENT = URSA_IDENT_START + '(?:' + URSA_IDENT_PART + ')*'


class CustomLexer(RegexLexer):
    """
    For Ursa source code.
    """

    name = 'Ursa'
    url = 'https://ursalang.github.io'
    aliases = ['ursa', 'Ursalang', 'ursalang']
    filenames = ['*.ursa']
    mimetypes = ['application/x-ursa', 'text/x-ursa']

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Whitespace),
            (r'//.*?$', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
        ],
        'comment': [
            (r'[^*/]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'root': [
            (r'\A#! ?/.*?$', Comment.Hashbang),  # recognized by ursa
            include('commentsandwhitespace'),

            # Numeric literals
            (r'0[bB][01]+n?', Number.Bin),
            (r'0[oO]?[0-7]+n?', Number.Oct),  # Browsers support "0o7" and "07" (< ES5) notations
            (r'0[xX][0-9a-fA-F]+n?', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'(\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+)([eE][-+]?[0-9]+)?', Number.Float),

            (r'~|:|\\(?=\n)|'
             r'<<|>>>?|==?|!=?|:=|(?:<=|>=|[-<>+*%&|^/])', Operator),
            (r'[{(\[;,]', Punctuation),
            (r'[})\].]', Punctuation),

            (r'(await|break|continue|else|fn|gen|if|in|launch|loop|pub|return|static|yield)\b', Keyword),
            (r'(class|for|let|trait|var|use)\b', Keyword.Declaration),

            (r'(true|false|null)\b', Keyword.Constant),
            (r'(and|or|not)\b', Operator.Word),

            (r'(print|pi|sqrt|exp|log|sin|cos|tan|range)\b', Name.Builtin),

            # Match stuff like: function() {...}
            (r'([a-zA-Z_?.$][\w?.$]*)(?=\(\) \{)', Name.Other),

            (URSA_IDENT, Name.Other),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
        ],
    }
