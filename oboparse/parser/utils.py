import pyparsing as pp

quoted_string = pp.QuotedString('"', unquoteResults=False, escChar='\\')
unqoted_quote_string = pp.QuotedString('"', escChar='\\')

obo_unquoted = pp.Regex(r'(?:[^\{!\\\n]|\\.)+')

OPEN_BRACKET = pp.Suppress(pp.Literal('['))
CLOSE_BRACKET = pp.Suppress(pp.Literal(']'))
OPEN_BRACE = pp.Suppress(pp.Literal('{'))
CLOSE_BRACE = pp.Suppress(pp.Literal('}'))
COLON = pp.Suppress(pp.Literal(':'))

_id_value = pp.Word(pp.printables, excludeChars='{!="')
synonym_type_id = pp.Word(pp.printables, excludeChars='{!=["')

modifier = pp.Group(
    OPEN_BRACE +
    pp.delimitedList(pp.Group(_id_value + pp.Suppress(pp.Literal('=')) + unqoted_quote_string), ',') +
    CLOSE_BRACE
)('modifier')

comment = pp.Suppress(pp.Literal('!') + pp.restOfLine)

EOL = pp.Optional(modifier) + pp.Optional(comment)

TRUE = pp.Keyword('true').setParseAction(lambda toks: True)
FALSE = pp.Keyword('false').setParseAction(lambda toks: False)
BOOLEAN = TRUE | FALSE

EXACT = pp.Keyword("EXACT")
BROAD = pp.Keyword("BROAD")
NARROW = pp.Keyword("NARROW")
RELATED = pp.Keyword("RELATED")

SYNONYM_SCOPE = (EXACT | BROAD | NARROW | RELATED)('synonym_scope')


def boolean_tag(tag_name: str) -> pp.ParserElement:
    return pp.Group(
        pp.Keyword(tag_name) + COLON + BOOLEAN + EOL
    )(tag_name)


def id_only_tag(tag_name: str) -> pp.ParserElement:
    return pp.Group(
        pp.Keyword(tag_name) + COLON + _id_value + EOL
    )(tag_name)


def basic_tag_value_pair(tag_name: str) -> pp.ParserElement:
    return pp.Group(pp.Keyword(tag_name) + COLON + obo_unquoted + EOL)(tag_name)
