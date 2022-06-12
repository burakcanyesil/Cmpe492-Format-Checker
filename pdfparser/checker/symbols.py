import re
from turtle import left
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance, get_roman


def check_symbols(pages: list[Page], line_space: float):
    errors = []
    first_page = pages[0]

    for index, page in enumerate(pages):
        if page.lines[0].text.lower() != get_roman(page.pageid):
            errors.append("List of symbols page " + str(index) + " should be enumarated with " + get_roman(page.pageid) + "!")

    if first_page.lines[1].text != "LIST OF SYMBOLS":
        errors.append("List of symbols must start with header 'LIST OF SYMBOLS'")

    # Spacing checking for symbols is nearly impossible because of PDF implemenation of non-latin characters, subscripts and superscripts

    return errors