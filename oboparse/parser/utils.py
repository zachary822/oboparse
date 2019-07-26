import pyparsing as pp
from rfc3987 import get_compiled_pattern

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


stanza_type = (pp.Keyword('Term') | pp.Keyword('Typedef') | pp.Keyword('Instance'))
stanza_name = (pp.LineStart() + OPEN_BRACKET + stanza_type + CLOSE_BRACKET)('stanza_name')
tag = pp.Regex(r'[^:\n]+')('tag')
value = pp.OneOrMore(
    pp.Word(pp.printables, excludeChars='{!"') | quoted_string, stopOn=pp.LineEnd()).setParseAction(
    ' '.join)('value')
xsd_type = pp.Combine('xsd:' + pp.Word(pp.alphas))('xsd-type')
dbxref_name = (pp.Regex(r'(?:[^],\"\\\n]|\\.)+') +
               pp.Optional(unqoted_quote_string))
dbxref = pp.Group(
    OPEN_BRACKET + (pp.delimitedList(dbxref_name, ',') | pp.Empty()) + CLOSE_BRACKET
)('dbxref')
tag_value_pair = pp.Group(tag + COLON + value + EOL)
file_path = pp.Regex(r'[^\0\n]+')
iri = pp.Regex(get_compiled_pattern('%(IRI)s'))
