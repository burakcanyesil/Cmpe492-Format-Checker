from pdfparser.data_classes import Page
from pdfparser.util import get_roman

def check_abstract_tr(page: Page, line_space: float, title: str):
    turkish_characters = {
                    "S¸": "Ş",
                    "˙I": "İ",
                    "˘G": "Ğ",
                    "C¸": "Ç",
                    "¨O": "Ö",
                    "¨U": "Ü",
                    "s¸": "ş",
                    "˘g": "ğ",
                    "c¸": "ç",
                    "¨o": "ö",
                    "¨u": "ü"
                    }

    # PDFminer does not work well with Turkish characters and displays their accent seperately,
    # so we need to replace them manually
    for line in page.lines:
        for char, tr_char in turkish_characters.items():
            line.text = line.text.replace(char, tr_char)

    errors = []

    if page.lines[0].text.lower() != get_roman(page.pageid):
        errors.append("Özet page should be enumarated with " + get_roman(page.pageid) + "!")

    if page.lines[1].text != "ÖZET":
        errors.append("Özet page must start with 'ÖZET' header!")

    title_line: str = page.lines[2].text
    next_line = 3
    if page.lines[2].box.y1 - page.lines[3].box.y2 < line_space * 1.3:
        title_line += " " + page.lines[3].text
        next_line += 1

    if not(title_line.isupper()):
        errors.append("Title should be uppercase!")
    
    return errors