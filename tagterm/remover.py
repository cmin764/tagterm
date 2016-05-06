"""Handles everything dealing with removing operations."""

import os
import re
from HTMLParser import HTMLParser
from xml.dom import minidom
from xml.etree import ElementTree

from tagterm import base
from tagterm.exceptions import RemoveError


class TagTerminator(HTMLParser):

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

    @property
    def content(self):
        return self._postprocess("".join(self.chunks))

    def handle_starttag(self, tag, attrs):
        if self._keep_tag(tag):
            self.log.debug("Keeping tag %r", tag)
            ent = self._get_html(tag, attrs=attrs)
            self.chunks.append(ent)

    def handle_endtag(self, tag):
        if self._keep_tag(tag):
            ent = self._get_html(tag)
            self.chunks.append(ent)

    def handle_startendtag(self, tag, attrs):
        if self._keep_tag(tag):
            self.log.debug("Keeping tag %r", tag)
            ent = self._get_html(tag, attrs=attrs, xtag=True)
            self.chunks.append(ent)

    def handle_data(self, data):
        self.log.debug("Keeping data %r", data)
        self.chunks.append(data)


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
            self.content = xml.toprettyxml()
        except Exception as exc:
            raise RemoveError("could not remove tags ({})".format(exc))

    def get_file_name(self):
        return super(Remover, self).get_file_name() + "-remove"

    def get_file_ext(self):
        return "xml"
