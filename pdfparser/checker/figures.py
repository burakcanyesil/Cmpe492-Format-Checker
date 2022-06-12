import re
from turtle import left
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance, get_roman


def check_figures(pages: list[Page], line_space: float):
    errors = []
    first_page = pages[0]
    remaining_pages = pages[1:]
    figure_pattern = re.compile(r"Figure [\d]+\.[\d]+\.")

    for index, page in enumerate(pages):
        if page.lines[0].text.lower() != get_roman(page.pageid):
            errors.append("List of figures page " + str(index) + " should be enumarated with " + get_roman(page.pageid) + "!")

    if first_page.lines[1].text != "LIST OF FIGURES":
        errors.append("List of figures must start with header 'LIST OF FIGURES'")

    first_page_figures = first_page.lines[2:]
    
    left_margin = first_page_figures[0].box.x1

    for index, line in enumerate(first_page_figures):
        if index == len(first_page_figures) - 1:
            break
        next_line = first_page_figures[index + 1]

        if eq_with_tolerance(line.box.x1, left_margin):
            if figure_pattern.search(line.text) == None:
                errors.append(" ".join(next_line.text.split()[:2]) + " is in wrong format!")


        if eq_with_tolerance(next_line.box.x1, left_margin):
            if abs(line.box.y1 - next_line.box.y1) < line_space * 1.3:
                errors.append(" ".join(next_line.text.split()[:2]) + " does not have a empty line above it!")

    for page in remaining_pages:
        figures = page.lines[1:]

        for index, line in enumerate(figures):
            if index == len(figures) - 1:
                break
            next_line = figures[index + 1]

            if eq_with_tolerance(line.box.x1, left_margin):
                if figure_pattern.search(line.text) == None:
                    errors.append(" ".join(next_line.text.split()[:2]) + " is in wrong format!")

            if eq_with_tolerance(next_line.box.x1, left_margin):
                if abs(line.box.y1 - next_line.box.y2) < line_space * 1.3:
                    errors.append(" ".join(next_line.text.split()[:2]) + " does not have a empty line above it!")


    return errors