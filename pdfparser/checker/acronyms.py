import re
from turtle import left
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance, get_roman


def check_acronyms(pages: list[Page], line_space: float):
    errors = []
    first_page = pages[0]
    remaining_pages = pages[1:]

    for index, page in enumerate(pages):
        if page.lines[0].text.lower() != get_roman(page.pageid):
            errors.append("List of acronyms/abbreviations page " + str(index+1) + " should be enumarated with " + get_roman(page.pageid) + "!")

    if first_page.lines[1].text != "LIST OF ACRONYMS/ABBREVIATIONS":
        errors.append("List of acronyms/abbreviations must start with header 'LIST OF ACRONYMS/ABBREVIATIONS'")

    first_page_acronyms = first_page.lines[2:]

    for index, line in enumerate(first_page_acronyms):
        if index == len(first_page_acronyms) - 1:
            break
        next_line = first_page_acronyms[index + 1]

        if abs(line.box.y1 - next_line.box.y2) > line_space * 1.3:
            errors.append(" ".join(next_line.text.split()[:2]) + " have an empty line above it!")

    for page in remaining_pages:
        acronyms = page.lines[1:]

        for index, line in enumerate(acronyms):
            if index == len(acronyms) - 1:
                break
            next_line = acronyms[index + 1]

            if abs(line.box.y1 - next_line.box.y1) < line_space * 1.3:
                errors.append(" ".join(next_line.text.split()[:2]) + " does not have a empty line above it!")


    return errors