from pdfparser.data_classes import Page


def check_title(title: Page, line_space: float):
    errors = []
    title_text: str

    title_line: str = title.lines[0].text
    if title_line.lower == "i":
        errors.append("Title pages should not be enumarated!")
    elif title.lines[0].box.y1 - title.lines[1].box.y2 < line_space * 1.3:
        title_line += " " + title.lines[1].text

    if not(title_line.upper):
        errors.append("Title should be uppercase!")
    title_text = title_line
    
    print(title_text)
    return errors, title_text