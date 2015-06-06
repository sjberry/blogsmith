import html

import misaka as m
from misaka import HtmlRenderer, Markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


_default_extensions = m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT | m.EXT_FENCED_CODE | m.EXT_TABLES | m.EXT_LAX_HTML_BLOCKS


class CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<code class="block highlight">'

        for i, t in source:
            yield i, t

        yield 0, '</code>'


class MarkdownRenderer(HtmlRenderer):
    def __init__(self, *args, extensions=_default_extensions, **kwargs):
        super(MarkdownRenderer, self).__init__(*args, **kwargs)
        self.extensions = extensions

    def block_code(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = CodeHtmlFormatter()
            output = highlight(text, lexer, formatter)
        except ClassNotFound:
            output = '<code class="block">%s</code>\n' % html.escape(text.strip(), quote=True)

        return output

    def render(self, text):
        return Markdown(self, extensions=self.extensions).render(text)
