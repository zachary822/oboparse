import networkx as nx
import pyparsing as pp

from .parser import obo_parser

__all__ = ['obo_parser', 'parse_result_to_networkx']


def parse_result_to_networkx(result: pp.ParseResults) -> nx.MultiDiGraph:
    common_attrs = {}

    try:
        common_attrs['name'] = result['headers']['ontology'][1]
        common_attrs['version'] = result['headers']['data-version'][1]
    except (KeyError, IndexError):
        pass

    graph = nx.MultiDiGraph(**common_attrs)

    for stanza in result[1]:
        name, tvps = stanza
        if name == 'Term':
            try:
                if tvps['is_obsolete'][1]:
                    continue
            except KeyError:
                pass

            _id = tvps['id'][1]

            for key, *vals in tvps:
                if key == 'is_a':
                    graph.add_edge(vals[0], _id, key='is_a')
                elif key == 'relationship':
                    graph.add_edge(vals[1], _id, key=vals[0])

    return graph
