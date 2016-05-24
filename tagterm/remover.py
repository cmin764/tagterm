"""Handles everything dealing with removing operations."""

import os
import re
from HTMLParser import HTMLParser
from xml.dom import minidom
from xml.etree import ElementTree

from tagterm import base
from tagterm.exceptions import RemoveError


ENCODING = "utf-8"


def content_normalizer(path):
    tree = ElementTree.parse(path)
    root = tree.getroot()

    styleToKeep = {
        'bold': 'b',
        'italic': 'i',
        'super': 'sup',
        'sub': 'sub'
    }

    ok = fin = init = 0

    with open(path) as f:
		content = f.readlines()

    for i in range(0, len(content)):
        line = content[i].strip()
        if line == '/**/' and ok == 0:
            ok = 1
            init = i
        elif line == '/**/':
            fin = i

    regex = ("(font-((weight:( )*bold(;)*)|((style:)( )*italic(;)*)))|"
             "(vertical-align:( )*(super(;)*|sub(;)*))")
    dict = {}

    for i in range (init + 1, fin - 1):
        ok = 0
        line = content[i].split(' ')
        lista = []
        for word in line:
            if re.search(regex, word):
                ok = 1
                lista.append(word)
        if ok == 1:
            dict.update({line[0]: lista})

    for peer in dict:
        p = peer.split('.')

        for child in root.findall('.//'):
            if child.get('class') == p[1]:
                for val in dict[peer]:
                    name = val
                    copychild = child
                    changed = 0
                    nrChildren = 0

                    for c in child.findall("*"):
			            nrChildren += 1

                    for s in styleToKeep:
                        if name.find(s) != -1:
                            changed = 1
                            addChild = styleToKeep[s]
                            currentChild = ElementTree.SubElement(copychild,
                                                      addChild)
                            copychild = currentChild

                    if changed == 1:
                        currentChild.text = child.text

                        if child.text :
                            del child.text

                        if nrChildren > 0:
                            for i in range(0, nrChildren):
                                currentChild.append(child[i])
                            for i in reversed(range(0, nrChildren)):
                                del child[i]

                if 'class' in child.attrib:
                    del child.attrib['class']

    cont = ElementTree.tostring(root, method="xml")
    xml = minidom.parseString(cont)
    content = xml.toprettyxml().encode(ENCODING)
    outFile = open(path, "w")
    outFile.write(content)


class TagTerminator(HTMLParser):

    ADD_PARATAG = True

    TAGS_PATH = os.path.normpath(
        os.path.join(
            base.PROJECT,
            os.path.join(
                "etc",
                "tagterm",
                "tags"
            )
        )
    )

    def __init__(self, log):
        HTMLParser.__init__(self)
        self.log = log

        self.tags = self._load_tags()
        self.chunks = []
        self.level = 0
        self.paralevel = -1

    def _load_tags(self):
        tags = []
        with open(self.TAGS_PATH) as stream:
            for line in stream:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue    # skip comments
                # Strip inline comments and save tags.
                idx = line.find("#")
                idx = idx if idx > 0 else len(line)
                tag = line[:idx].strip()
                tags.append(tag)
        return tags

    def _keep_tag(self, tag):
        for keep in self.tags:
            if re.match(keep + "$", tag, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def _get_html(tag, attrs=None, xtag=False):
        if attrs is None:    # end tag
            return "</{}>".format(tag)

        pairs = ['{}="{}"'.format(*attr) for attr in attrs]
        if pairs:
            pairs.insert(0, "")
        attrs_html = " ".join(pairs)

        ret = "<{}{}{}>".format(
            tag,
            attrs_html,
            " /" if xtag else ""
        )
        return ret

    @staticmethod
    def _postprocess(data):
        lines = []
        for line in data.splitlines():
            line = line.strip()
            if line:
                lines.append(line)
        return base.EOL.join(lines)

    def _check_para(self, tag):
        if tag != "br":
            return
        self.log.debug("New paragraph on level %d", self.level)
        self.chunks.append(base.EOL * 2)
        if self.ADD_PARATAG:
            self.paralevel = self.level

    @property
    def content(self):
        return self._postprocess("".join(self.chunks))

    def handle_starttag(self, tag, attrs):
        if self._keep_tag(tag):
            self.level += 1
            self.log.debug("Keeping tag %r", tag)
            ent = self._get_html(tag, attrs=attrs)
            self.chunks.append(ent)

    def handle_endtag(self, tag):
        if self._keep_tag(tag):
            self.level -= 1
            ent = self._get_html(tag)
            self.chunks.append(ent)

    def handle_startendtag(self, tag, attrs):
        if self._keep_tag(tag):
            self.log.debug("Keeping tag %r", tag)
            ent = self._get_html(tag, attrs=attrs, xtag=True)
            self.chunks.append(ent)
        self._check_para(tag)

    def handle_data(self, data):
        self.log.debug("Keeping data %r", data)
        before = after = ""
        if self.ADD_PARATAG and self.paralevel == self.level:
            self.paralevel = -1
            before, after = "<p>", "</p>"
        self.chunks.extend([before, data, after])


class Remover(base.BaseWriteProcess):

    def remove(self):
        try:
            # Parse XHTML while removing tags and enclose data into XML.
            parser = TagTerminator(self.log)
            parser.feed(self.content)
            content = "<xml>\n{}\n</xml>".format(parser.content)
            # Do one additional XML check/validation more.
            doc = ElementTree.fromstring(content)
            content = ElementTree.tostring(doc, method="xml")
            xml = minidom.parseString(content)
            self.content = xml.toprettyxml().encode(ENCODING)
        except Exception as exc:
            raise RemoveError("could not remove tags ({})".format(exc))

    def get_file_name(self):
        return super(Remover, self).get_file_name() + "-remove"

    def get_file_ext(self):
        return "xml"
