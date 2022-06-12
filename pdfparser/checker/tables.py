import re
from turtle import left
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance, get_roman


def check_tables(pages: list[Page], line_space: float):
    errors = []
    first_page = pages[0]
    remaining_pages = pages[1:]
    table_pattern = re.compile(r"Table [\d]+\.[\d]+\.")

    for index, page in enumerate(pages):
        if page.lines[0].text.lower() != get_roman(page.pageid):
            errors.append("List of tables page " + str(index+1) + " should be enumarated with " + get_roman(page.pageid) + "!")

    if first_page.lines[1].text != "LIST OF TABLES":
        errors.append("List of tables must start with header 'LIST OF TABLES'")

    first_page_tables = first_page.lines[2:]
    
    left_margin = first_page_tables[0].box.x1

    for index, line in enumerate(first_page_tables):
        if index == len(first_page_tables) - 1:
            break
        next_line = first_page_tables[index + 1]

        if eq_with_tolerance(line.box.x1, left_margin):
            if table_pattern.search(line.text) == None:
                errors.append(" ".join(next_line.text.split()[:2]) + " is in wrong format!")


        if eq_with_tolerance(next_line.box.x1, left_margin):
            if abs(line.box.y1 - next_line.box.y1) < line_space * 1.3:
                errors.append(" ".join(next_line.text.split()[:2]) + " does not have a empty line above it!")

    for page in remaining_pages:
        tables = page.lines[1:]

        for index, line in enumerate(tables):
            if index == len(tables) - 1:
                break
            next_line = tables[index + 1]

            if eq_with_tolerance(line.box.x1, left_margin):
                if table_pattern.search(line.text) == None:
                    errors.append(" ".join(next_line.text.split()[:2]) + " is in wrong format!")

            if eq_with_tolerance(next_line.box.x1, left_margin):
                if abs(line.box.y1 - next_line.box.y2) < line_space * 1.3:
                    errors.append(" ".join(next_line.text.split()[:2]) + " does not have a empty line above it!")


    return errors