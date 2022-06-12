from pdfparser.data_classes import Page
from pdfparser.util import get_roman


def check_acknowledgements(page: Page, line_space: float):
    errors = []

    if page.lines[0].text.lower() != get_roman(page.pageid):
        errors.append("Acknowledgements page should be enumarated with " + get_roman(page.pageid) + "!")

    if page.lines[1].text != "ACKNOWLEDGEMENTS":
        errors.append("Acknowledgments page must start with 'ACKNOWLEDGMENTS' header!")
    
    return errors

    