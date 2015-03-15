import io

import lxml.etree
from nltk.tree import Tree as NltkTree
from pygments import lexers, formatters, highlight

from hercules import CachedAttr
from visitors.ext.etree import XmlEtreeVisitor, from_etree
from hercules import CachedAttr


# ----------------------------------------------------------------------------
# Core NLP Wrappers. Belongs in its own package.
# ----------------------------------------------------------------------------
class XmlFormatter:
    formatter = formatters.TerminalFormatter()
    lexer = lexers.XmlLexer()

    def pformat(self, doc):
        string = lxml.etree.tostring(doc, pretty_print=True).decode('utf8')
        return highlight(string, self.lexer, self.formatter)

    def pprint(self):
        print(self.pformat())


def pformat_xml(doc, formatter=XmlFormatter()):
    return formatter.pformat(doc)


class CoreNLP:

    def __init__(self, data):
        self.data = data

    @CachedAttr
    def doc(self):
        bytes = self.data['xml'].encode('utf8')
        return lxml.etree.fromstring(bytes)

    def xpath(self, *args, **kwargs):
        return self.doc.xpath(*args, **kwargs)

    @property
    def sentences(self):
        return tuple(map(Sentence, self.doc.xpath('//sentence')))

    def pprint_xml(self):
        print(pformat_xml(self.doc))


class Sentence:

    def __init__(self, el):
        self.el = el

    def __str__(self):
        return self.as_string

    @CachedAttr
    def as_string(self):
        offset = 0
        buf = io.StringIO()
        for tok in self.tokens:
            start, end = tok.span
            while offset < start:
                buf.write(' ')
                offset += 1
            buf.write(tok.word)
            offset += len(tok)
            while offset < end:
                buf.write(' ')
                offset += 1
        return buf.getvalue()

    @property
    def tokens(self):
        return tuple(map(Token, self.el.xpath('tokens/token')))

    @property
    def span(self):
        return (self.start, self.end)

    @property
    def start(self):
        return self.tokens[0].start

    @property
    def end(self):
        return self.tokens[-1].end

    @CachedAttr
    def tree(self):
        string = self.el.xpath('string(parse)')
        return Tree(string)


class Token:

    def __init__(self, token):
        self.token = token

    def __len__(self):
        return len(self.word)

    @property
    def word(self):
        return self.token.xpath('string(word)')

    @property
    def span(self):
        return (self.start, self.end)

    @property
    def start(self):
        return int(self.token.xpath('string(CharacterOffsetBegin)'))

    @property
    def end(self):
        return int(self.token.xpath('string(CharacterOffsetEnd)'))

    @property
    def attrib(self):
        return self.token.attrib


class Tree:

    def __init__(self, string):
        self.string = string
        self.tree = NltkTree.fromstring(string)

    def _tree2etree(self, tree):
        tag = tree.label()
        if not tag.isalpha():
            tag = 'symbol'
        root = lxml.etree.Element(tag)
        root.attrib['label'] = tree.label()
        for child in tree:
            if isinstance(child, NltkTree):
                root.append(self._tree2etree(child))
            else:
                root.text = child
        return root

    @CachedAttr
    def doc(self):
        return self._tree2etree(self.tree)

    def xpath(self, xpath):
        return self.doc.xpath(xpath)

    def pprint(self):
        print(pformat_xml(self.doc))