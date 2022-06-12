import re
from pdfparser.data_classes import Document, Line, Page
from pdfparser.util import get_roman

def check_toc(document: Document):
    errors = []

    toc = document.toc

    for index, page in enumerate(toc):
        if page.lines[0].text.lower() != get_roman(page.pageid):
            errors.append("Table of content page " + str(index) + " should be enumarated with " + get_roman(page.pageid) + "!")
        
    if toc[0].lines[1].text != "TABLE OF CONTENTS":
        errors.append("Table of contents section should start with header 'TABLE OF CONTENTS'!")

    for index in range(1, len(toc)):
        toc[0].lines.extend(toc[index].lines[1:])

    is_two_line = False
    for index in range(2, len(toc[0].lines)):
        current_line: Line = toc[0].lines[index]

        if is_two_line:
            is_two_line = False
            continue

        if current_line.text[0].isdigit():
            if re.search(r"(\. )+[\d]+$", current_line.text) == None:
                if toc[0].lines[index+1].text[0].isdigit():
                    print(toc[0].lines[index])
                    errors.append("Misalignment in the points of line " + current_line.text + "!")
                else: 
                    if re.search(r"(\. )+[\d]+$", toc[0].lines[index+1].text) == None:
                        errors.append("Missing page number for line " + current_line.text + "!")
                    is_two_line = True
        else:
            if re.search(r"[mdclxvi]+$", current_line.text) == None and not (current_line.text.startswith("REFERENCES") or current_line.text.startswith("APPENDIX")):
                print(current_line)
                errors.append("Preliminary pages should be enumerated with roman numbers.")

    return errors

