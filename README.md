# OBOparse

## Introduction

OBO file parser implemented with [pyparsing](https://pypi.org/project/pyparsing/).

## Example

```python
from oboparse import obo_parser
from urllib.request import urlopen
from io import TextIOWrapper

with urlopen('http://purl.obolibrary.org/obo/go.obo') as f:
    parse_result = obo_parser.parseFile(TextIOWrapper(f), parseAll=True)
    parse_result.pprint()
```

## Reference

1. https://owlcollab.github.io/oboformat/doc/obo-syntax.html
1. https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html

## License

MIT
