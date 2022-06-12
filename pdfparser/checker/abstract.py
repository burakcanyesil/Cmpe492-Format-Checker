from pdfparser.data_classes import Page
from pdfparser.util import get_roman

def check_abstract(page: Page, line_space: float, title: str):
    errors = []

    if page.lines[0].text.lower() != get_roman(page.pageid):
        errors.append("Abstract page should be enumarated with " + get_roman(page.pageid) + "!")

    if page.lines[1].text != "ABSTRACT":
        errors.append("Abstract page must start with 'ABSTRACT' header!")

    title_line: str = page.lines[2].text
    next_line = 3
    if page.lines[2].box.y1 - page.lines[3].box.y2 < line_space * 1.3:
        title_line += " " + page.lines[3].text
        next_line += 1

    if not(title_line.isupper()):
        errors.append("Title should be uppercase!")

    if title_line != title:
        errors.append("Title is different from title page!")

    print (title_line)
    return errors