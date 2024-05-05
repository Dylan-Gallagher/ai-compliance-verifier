from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer
import re

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def get_optional_fontinfo(o) -> str:
    """Font info of LTChar if available, otherwise empty string"""
    if hasattr(o, 'fontname') and hasattr(o, 'size'):
        return f'{o.fontname} {round(o.size)}pt'
    return ''


def matches_format(s):
    """Check if a string matches the format of the 'page string' in a pdf"""
    pattern = r'^\d+ \nEN \n$'
    return bool(re.match(pattern, s))


def is_valid(element):
    """Check if a textbox from the pdf is valid (body) or useless (header/footnotes)"""
    invalid_lines = ['5662/24  \n', 'TREE.2.B \n', 'RB/ek \nLIMITE \n', '  \n', ' \n']
    if element.get_text() in invalid_lines or matches_format(element.get_text()):
        return False

    # Check if it's a reference (small text)
    a = next(iter(element))
    if is_iterable(a):
        e = next(iter(a))
        if hasattr(e, 'size'):
            if e.size < 10.0:
                return False
    return True


def parse_EU_act(path, raw_text=False):
    """
    Convert a pdf to a string:
    
    Parameters:
    path: path to pdf
    raw_text: set to False if you want to strip footnotes and references
    
    """
    if raw_text:
        return extract_text(path)

    combined_str = ""
    for page_layout in extract_pages(path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                if is_valid(element):
                    combined_str += element.get_text()

    return combined_str


if __name__ == "__main__":
    print(parse_EU_act("ai_act/ai-act-draft.pdf"))
