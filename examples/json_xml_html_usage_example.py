import json
import decimal
from io import StringIO
from html.parser import HTMLParser
from xml.dom import minidom


def json_use_example():
    print('\n'+'JSON use example' + '*'*50+'\n')
    print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))
    print(json.dumps("\"foo\bar"))
    print(json.dumps('\u1234'))
    print(json.dumps('\\'))
    print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
    io = StringIO('["streaming API"]')
    print(json.load(io))

    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, complex):
                return [obj.real, obj.imag]
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

    print(json.dumps(2 + 1j, cls=ComplexEncoder), ComplexEncoder().encode(2 + 1j),
          list(ComplexEncoder().iterencode(2 + 1j)))

    def as_complex(dct):
        if '__complex__' in dct:
            return complex(dct['real'], dct['imag'])
        return dct

    print(json.loads('{"__complex__": true, "real": 1, "imag": 2}',
                     object_hook=as_complex))
    print(json.loads('1.1', parse_float=decimal.Decimal))
    print('\n')

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
    print('\n')

def html_parser_example():
    print('\n' + 'HTMLParser use example' + '*' * 50+'\n')
    parser = MyHTMLParser()
    parser.feed('<html><head><title>Test</title></head>'
                      '<body><h1>Parse me!</h1></body></html>')


def xml_example():
    print('\n' + 'XML use example' + '*' * 50+'\n')
    # parse an xml file by name
    mydoc = minidom.parse('items.xml')

    items = mydoc.getElementsByTagName('item')

    # one specific item attribute
    print('Item #2 attribute:')
    print(items[1].attributes['name'].value)

    # all item attributes
    print('\nAll attributes:')
    for elem in items:
        print(elem.attributes['name'].value)

    # one specific item's data
    print('\nItem #2 data:')
    print(items[1].firstChild.data)
    print(items[1].childNodes[0].data)

    # all items data
    print('\nAll item data:')
    for elem in items:
        print(elem.firstChild.data)


if __name__ == "__main__":
    xml_example()
    html_parser_example()
    json_use_example()
