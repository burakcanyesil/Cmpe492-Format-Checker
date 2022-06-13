import re
from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance


def check_body(pages: list[Page], line_space: float, introduction_length: int, left_margin: float, new_paragraph_margin: float):
    errors = {}

    first_page = pages[0]
    remaining_pages = pages[1:]

    roman_pattern = re.compile(r"\([mdclxvi]+\)")
    chapter_header_pattern = re.compile(r"^[\d]+\. ")
    first_subheader_pattern = re.compile(r"^[\d]+\.[\d]+\. ")

    wrong_equation = re.compile(r"Equation ([\d]+\.[\d]+)")

    for index, page in enumerate(pages):
        errors[index+1] = []
        is_fullpage = False
        if len(page.lines) == 2:
            for line in page.lines:
                if line.vertical:
                    is_fullpage = True
                break
        if is_fullpage and page.lines[0].text == str(index + 1 + introduction_length):
            errors[index+1].append("Page " + str(index + 1) + " should not have paginaton because it is vertical!")
        if page.lines[0].text != str(index + 1 + introduction_length) and not is_fullpage:
            errors[index+1].append("Body page " + str(index + 1) + " should be enumerated with " + str(index + 1 + introduction_length))
 


    for page_index, page in enumerate(pages):
        body = page.lines[1:]
        is_equation = False
        is_list = False
        is_figure = False
        is_table = False

        for index, line in enumerate(body):
            if index + 1 == len(body):
                break
            next_line = body[index+1]

            if chapter_header_pattern.search(line.text) != None:
                is_equation = False
                is_list = False
                is_figure = False
                is_table = False

                if not(" ".join(line.text.split()[1:]).isupper()):
                    errors[page_index+1].append("Main header '" + line.text + "' should be uppercase!")
                if not index == 0:
                    errors[page_index+1].append("Main header '" + line.text + "' should start a new page!")
                if not abs(next_line.box.y2-line.box.y1) > line_space * 1.9:
                    errors[page_index+1].append("After main header '" + line.text + "' there should be two empty lines!")
                continue
            
            if first_subheader_pattern.search(line.text) != None:
                is_equation = False
                is_list = False
                is_figure = False
                is_table = False
                

                if not abs(next_line.box.y2-line.box.y1) > line_space * 0.9:
                    errors[page_index+1].append("After first subheader '" + line.text + "' there should be one empty lines!")

                continue

            next_line_center = (next_line.box.y1 + next_line.box.y2) / 2
            next_next_line_center = 0
            if(index + 2) < len(body):
                next_next_line_center = (body[index+2].box.y1 + body[index+2].box.y2) / 2
                if next_next_line_center < next_line.box.y2 + 2 and next_next_line_center > next_line.box.y1 - 2 and body[index+2].box.x1 < next_line.box.x1:
                    next_line.box.x1 = body[index+2].box.x1
                    next_line.text = body[index+2].text + next_line.text
            if next_line_center < line.box.y2 + 3 and next_line_center > line.box.y1 - 3:
                next_line.text = line.text + next_line.text
                next_line.box.x1 = line.box.x1
                continue

            if is_equation:
                if ((line.box.x1 > left_margin * 1.01 and line.box.x1 < new_paragraph_margin * 0.99) or line.box.x1 > new_paragraph_margin * 1.01):
                    continue
                else:
                    if not(eq_with_tolerance(next_line.box.x1, left_margin)) and not (next_line.text.startswith("Figure") or next_line.text == "__figure__" or next_line.text.startswith("Table")) and next_line.text.lower().startswith("where"):
                        errors[page_index+1].append("First line after equation starting with '" + " ".join(next_line.text.split()[:3]) + "' cannot be a new paragraph!")
                    is_equation = False

            if is_figure:
                if abs(next_line.box.y2 - line.box.y1) < line_space * 1.1:
                    continue
                else:
                    is_figure = False

            if is_table:
                if abs(next_line.box.y2 - line.box.y1) > line_space * 1.1 and (eq_with_tolerance(next_line.box.x1, left_margin) or eq_with_tolerance(next_line.box.x1, new_paragraph_margin)):
                    is_table = False
                else:
                    continue

            if line.text.startswith("Figure") or line.text == "__figure__":
                is_figure = True
                is_equation = False
                is_table = False

            if line.text.startswith("Table"):
                is_table = True
                is_figure = False
                is_equation = False
            if roman_pattern.search(next_line.text) != None or next_line.text.startswith("•"):
                is_list = True
            if roman_pattern.search(line.text) != None or line.text.startswith("•"):
                is_list = True

            result =  wrong_equation.search(line.text)
            if result != None:
                errors[page_index+1].append("Reference to Equation " + str(result.group(1)) + " is in wrong format! Should be Equation (" + str(result.group(1)) + ")")


            if ((line.box.x1 > left_margin * 1.05 and line.box.x1 < new_paragraph_margin * 0.95) or line.box.x1 > new_paragraph_margin * 1.05) and not is_figure and not is_table and not is_list:
                is_equation = True

            if eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(line.box.y1 - next_line.box.y2) < line_space * 1.3 and not is_list:
                errors[page_index+1].append("No new line before paragraph starting with '" + " ".join(next_line.text.split()[:3]) + "'!")
            
            if is_list and eq_with_tolerance(next_line.box.x1, new_paragraph_margin) and abs(next_line.box.y2 - line.box.y1) > line_space * 1.3:
                is_list = False

            if ((next_line.box.x1 > left_margin * 1.05 and next_line.box.x1 < new_paragraph_margin * 0.95) or next_line.box.x1 > new_paragraph_margin * 1.05) and not is_figure and not is_table and not is_list:
                if abs(line.box.y1 - next_line.box.y2) < line_space * 1.7 and abs(line.box.y1 - next_line.box.y2) > line_space * 0.8 and not is_equation:
                    errors[page_index+1].append("There should be one empty line between line starting with '" + " ".join(next_line.text.split()[:3]) + "' and equation." + line.text)
                is_equation = True
    
            last_line = body[-1]
        
        last_line = body[-1]
        if page_index != len(pages) - 1:
            if eq_with_tolerance(last_line.box.x1, new_paragraph_margin) and eq_with_tolerance(pages[page_index+1].lines[1].box.x1, left_margin):
                errors[1].append("One line of a new paragraph left in the end of the page " + str(page_index + 1) + " .")
    return errors