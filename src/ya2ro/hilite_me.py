from pygments import highlight
from pygments.lexers.data import YamlLexer
from pygments.lexers.scdoc import ScdocLexer
from pygments.formatters import HtmlFormatter

def yaml_formatter(code):

    formatter = HtmlFormatter(linenos=True, full=True, style='friendly')
    html = highlight(code, YamlLexer(), formatter)

    return html
    
def bib_formatter(code):

    formatter = HtmlFormatter(linenos=True, full=True, style='friendly')
    html = highlight(code, ScdocLexer(), formatter)

    return html