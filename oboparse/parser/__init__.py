"""
OBO parser

as described in https://owlcollab.github.io/oboformat/doc/obo-syntax.html
https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html
"""
import pyparsing as pp

from .utils import CLOSE_BRACKET, COLON, EOL, OPEN_BRACKET, SYNONYM_SCOPE, _id_value, basic_tag_value_pair, \
    boolean_tag, comment, id_only_tag, obo_unquoted, quoted_string, synonym_type_id, unqoted_quote_string

__all__ = ['obo_parser']

stanza_type = (pp.Keyword('Term') | pp.Keyword('Typedef') | pp.Keyword('Instance'))
stanza_name = (pp.LineStart() + OPEN_BRACKET + stanza_type + CLOSE_BRACKET)('stanza_name')

tag = pp.Word(pp.alphas + '_-.')('tag')

value = pp.OneOrMore(
    pp.Word(pp.printables, excludeChars='{!"') | quoted_string, stopOn=pp.LineEnd()).setParseAction(
    ' '.join)('value')

dbxref_name = (pp.Regex(r'(?:[^],\"\\\n]|\\.)+') +
               pp.Optional(unqoted_quote_string))
dbxref = pp.Group(
    OPEN_BRACKET + (pp.delimitedList(dbxref_name, ',') | pp.Empty()) + CLOSE_BRACKET
)('dbxref')

tag_value_pair = pp.Group(tag + COLON + value + EOL)

iri = pp.Word(pp.printables + ' ')

# header tags
format_version_tag = pp.Group(pp.Keyword('format-version') + COLON + obo_unquoted)('format-version')

data_version_tag = pp.Group(pp.Keyword('data-version') + COLON + obo_unquoted)('data-version')

date_tag = pp.Group(pp.Keyword('date') + COLON + pp.Regex(r'\d{2}:\d{2}:\d{4}\s+\d{2}:\d{2}'))('date')

auto_generated_by_tag = pp.Group(pp.Keyword('auto-generated-by') + COLON + obo_unquoted)('auto-generated-by')

import_tag = pp.Group(pp.Keyword('import') + COLON + iri)('import')

subsetdef_tag = pp.Group(pp.Keyword('subsetdef') + COLON + _id_value + unqoted_quote_string)('subsetdef')

synonymtypedef_tag = pp.Group(
    pp.Keyword('synonymtypedef') + COLON + _id_value + unqoted_quote_string + pp.Optional(SYNONYM_SCOPE)
)('synonymtypedef')

# stanza tags
is_anonymous = boolean_tag('is_anonymous')

_id_tag = id_only_tag('id')

name_tag = basic_tag_value_pair('name')

namespace_tag = basic_tag_value_pair('namespace')

alt_id_tag = id_only_tag('ald_id')

_def_tag = pp.Group(
    pp.Keyword('def') + COLON + unqoted_quote_string + dbxref +
    EOL
)('def')

comment_tag = basic_tag_value_pair('comment')

subset_tag = id_only_tag('subset')

synonym_tag = pp.Group(
    pp.Keyword('synonym') + COLON + unqoted_quote_string +
    pp.Optional(SYNONYM_SCOPE, default="RELATED") + pp.Optional(synonym_type_id) + pp.Optional(dbxref) +
    EOL
)('synonym')

xref_tag = pp.Group(
    pp.Keyword('xref') + COLON + _id_value + pp.Optional(unqoted_quote_string) + EOL
)('xref')

builtin_tag = boolean_tag('builtin')

xsd_type = pp.Combine('xsd:' + pp.Word(pp.printables, excludeChars='!{'))('xsd-type')

property_value_tag = pp.Group(
    pp.Keyword('property_value') + COLON + _id_value + ((unqoted_quote_string + xsd_type) | _id_value) + EOL
)('property_value')

is_a_tag = id_only_tag('is_a')

intersection_of_tag = pp.Group(
    pp.Keyword('intersection_of') + COLON + _id_value + pp.Optional(_id_value) + EOL
)('intersection_of')

union_of_tag = id_only_tag('union_of')

equivalent_to_tag = id_only_tag('equivalent_to')

disjoint_from_tag = id_only_tag('disjoint_from')

relationship_tag = pp.Group(pp.Keyword('relationship') + COLON + _id_value + _id_value + EOL)('relationship')

is_obsolete = boolean_tag('is_obsolete')

replaced_by_tag = id_only_tag('replaced_by')

consider_tag = id_only_tag('consider')

created_by_tag = basic_tag_value_pair('created_by')

creation_date_tag = pp.Group(
    pp.Keyword('creation_date') + COLON + pp.pyparsing_common.iso8601_datetime + EOL
)('creation_date')

stanza = pp.Group(
    stanza_name +
    pp.Group(
        pp.OneOrMore(
            is_anonymous |
            _id_tag |
            name_tag |
            namespace_tag |
            alt_id_tag |
            _def_tag |
            comment_tag |
            subset_tag |
            synonym_tag |
            xref_tag |
            builtin_tag |
            property_value_tag |
            is_a_tag |
            intersection_of_tag |
            union_of_tag |
            equivalent_to_tag |
            disjoint_from_tag |
            relationship_tag |
            is_obsolete |
            replaced_by_tag |
            consider_tag |
            created_by_tag |
            creation_date_tag |
            pp.Group(tag + COLON + obo_unquoted + EOL) |
            tag_value_pair
        )
    )
)

headers = pp.OneOrMore(
    format_version_tag |
    data_version_tag |
    date_tag |
    import_tag |
    subsetdef_tag |
    synonymtypedef_tag |
    pp.Group(tag + COLON + obo_unquoted) |
    tag_value_pair
)

stanzas = pp.OneOrMore(
    stanza |
    comment
)

obo_parser = pp.Group(headers)('headers') + pp.Group(stanzas)('stanzas')
