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
    
    return errors