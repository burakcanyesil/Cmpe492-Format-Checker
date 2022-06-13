import re
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance


def check_introduction(pages: list[Page], line_space: float):
    errors = {}

    first_page = pages[0]
    remaining_pages = pages[1:]

    left_margin: float
    new_paragraph_margin: float 

    roman_pattern = re.compile(r"\([mdclxvi]+\)")

    for index, page in enumerate(pages):
        errors[index+1] = []
        if page.lines[0].text != str(index + 1):
            errors[1].append("Introduction page " + str(index + 1) + " should be enumerated with " + str(index + 1))
    
    if first_page.lines[1].text != "1. INTRODUCTION":
        errors[1].append("Introduction section should start with header '1. INTRODUCTION'!")
    
    first_page_body = first_page.lines[2:]

    left_margin = first_page_body[1].box.x1
    new_paragraph_margin = first_page_body[0].box.x1

    is_equation = False
    is_list = False

    for index, line in enumerate(first_page_body):
        if index + 1 == len(first_page_body):
            break
        next_line = first_page_body[index+1]

        next_line_center = (next_line.box.y1 + next_line.box.y2) / 2
        if next_line_center < line.box.y2 and next_line_center > line.box.y1:
            next_line.text = line.text + next_line.text
            next_line.box.x1 = line.box.x1
            continue

        if is_equation:
            if next_line.box.x1 > new_paragraph_margin * 1.2:
                continue
            else:
                if not(eq_with_tolerance(next_line.box.x1, left_margin)):
                    errors[1].append("First line after equation starting with '" + " ".join(next_line.text.split()[:3]) + "' cannot be a new paragraph!")
                is_equation = False

        if roman_pattern.match(line.text) != None:
            is_list = True

        if eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(line.box.y1 - next_line.box.y2) < line_space * 1.3 and not is_list:
            errors[1].append("No new line before paragraph starting with " + " ".join(next_line.text.split()[:3]))

        if is_list and eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(next_line.box.y2 - line.box.y1) > line_space * 1.3:
            is_list = False

        if next_line.box.x1 > new_paragraph_margin * 1.1:
            if abs(line.box.y1 - next_line.box.y2) < line_space * 1.9:
                errors[1].append("There should be one empty line between text and equation.")
            is_equation = True
    
    last_line = first_page_body[-1]
    if len(remaining_pages) > 0:
        if eq_with_tolerance(last_line.box.x1, new_paragraph_margin) and eq_with_tolerance(remaining_pages[0].lines[1].box.x1, left_margin):
            errors[1].append("One line of a new paragraph left in the end of the page 1.")

    for page_index, page in enumerate(remaining_pages):
        body = page.lines[1:]
        is_equation = False
        is_list = False

        for index, line in enumerate(body):
            if index + 1 == len(body):
                break
            next_line = body[index+1]

            next_line_center = (next_line.box.y1 + next_line.box.y2) / 2
            if next_line_center < line.box.y2 and next_line_center > line.box.y1:
                next_line.text = line.text + next_line.text
                next_line.box.x1 = line.box.x1
                continue

            if is_equation:
                if next_line.box.x1 > new_paragraph_margin * 1.2:
                    continue
                else:
                    if not(eq_with_tolerance(next_line.box.x1, left_margin)):
                        errors[page_index+1].append("First line after equation starting with '" + " ".join(next_line.text.split()[:3]) + "' cannot be a new paragraph!")
                    is_equation = False


            if roman_pattern.match(line.text) != None:
                is_list = True

            if eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(line.box.y1 - next_line.box.y2) < line_space * 1.3 and not is_list:
                print(line)
                errors[page_index+1].append("No new line before paragraph starting with " + " ".join(next_line.text.split()[:3]))
            
            if is_list and eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(next_line.box.y2 - line.box.y1) > line_space * 1.3:
                is_list = False

            if next_line.box.x1 > new_paragraph_margin * 1.1:
                if abs(line.box.y1 - next_line.box.y2) < line_space * 1.9:
                    errors[page_index+1].append("There should be one empty line between text and equation.")
                is_equation = True
    
            last_line = first_page_body[-1]
        
        last_line = body[-1]
        if page_index != len(remaining_pages) - 1:
            if eq_with_tolerance(last_line.box.x1, new_paragraph_margin) and eq_with_tolerance(remaining_pages[page_index+1].lines[1].box.x1, left_margin):
                errors[1].append("One line of a new paragraph left in the end of the page " + str(page_index + 1) + " .")
    return errors, left_margin, new_paragraph_margin
            
        