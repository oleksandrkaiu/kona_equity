import re

from django.utils.encoding import force_text
from django.template import Library, Node
from django.utils.safestring import mark_safe


register = Library()


def strip_spaces_in_tags(value):
    value = force_text(value)
    value = re.sub(r'\s+', ' ', str(value))
    value = re.sub(r'>\s+', '>', str(value))
    value = re.sub(r'\s+<', '<', str(value))
    return value

def highlight_many(text, keywords):
    replacement = "<strong>" + "\\1" + "</strong>"
    text = re.sub("(" + "|".join(map(re.escape, str(keywords))) + ")", replacement, str(text), flags=re.I)
    return text
    

class NoSpacesNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_spaces_in_tags(self.nodelist.render(context).strip())


@register.tag
def nospaces(parser, token):
    """
    Removes any duplicite whitespace in tags and text. Can be used as supplementary tag for {% spaceless %}::
        {% nospaces %}
        <strong>
            Hello
            this is text
        </strong>
        {% nospaces %}
    Returns::
        <strong>Hello this is text</strong>
    """
    nodelist = parser.parse(('endnospaces',))
    parser.delete_first_token()
    return NoSpacesNode(nodelist)

@register.simple_tag
def emphasize(text, key):
    """
    Render highlighted text by search key
    """
    keywords = [key.capitalize(), key.lower(), key.upper()]
    return mark_safe(highlight_many(text, keywords))