import enum
from re import S, T
from tracemalloc import stop
from typing import Iterable
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
from pdfparser.checker.abstract import check_abstract
from pdfparser.checker.acronyms import check_acronyms
from pdfparser.checker.body import check_body
from pdfparser.checker.figures import check_figures
from pdfparser.checker.introduction import check_introduction
from pdfparser.checker.references import check_references
from pdfparser.checker.symbols import check_symbols
from pdfparser.checker.tables import check_tables
from pdfparser.checker.title import *
from pdfparser.checker.approval import *
from pdfparser.checker.acknowledgements import *
from pdfparser.checker.abstract_tr import *
from pdfparser.checker.toc import *
from pdfparser.data_classes import *




def __extract_elements(element) -> list[Page]:
    sub_elements = []

    if isinstance(element, Iterable):
        for sub_element in element:
            if sub_element.__class__.__name__ == "LTTextLineHorizontal":
                box = element.bbox
                text = element.get_text().strip()

                sub_elements.append(Line(text, Box(box[0], box[1], box[2], box[3])))
            elif sub_element.__class__.__name__ == "LTTextLineVertical":
                box = element.bbox
                text = element.get_text().strip()

                sub_elements.append(Line(text, Box(box[0], box[1], box[2], box[3]), True))
            elif sub_element.__class__.__name__ == "LTPage":
                box = Box(sub_element.bbox[0], sub_element.bbox[1], sub_element.bbox[2], sub_element.bbox[3])
                sub_elements.append(Page(sub_element.pageid, box, __extract_elements(sub_element)))
            elif sub_element.__class__.__name__ == "LTFigure" and element.__class__.__name__ == "LTFigure":
                box = sub_element.bbox
                sub_elements.append(Line("__figure__", Box(box[0], box[1], box[2], box[3])))

            else: 
                sub_elements.extend(__extract_elements(sub_element))
    return sub_elements

def __get_document(options: Options, pages: list[Page]):
    document = Document()
    current_page = 0
    
    document.title = pages[current_page]
    current_page += 1

    document.approval = pages[current_page]
    current_page += 1

    document.dedication = []
    for i in range(options.dedication_length):
        document.dedication.append(pages[current_page])
        current_page += 1

    document.foreword = []
    for i in range(options.foreword_length):
        document.foreword.append(pages[current_page])
        current_page += 1

    document.preface = []
    for i in range(options.preface_length):
        document.foreword.append(pages[current_page])
        current_page += 1

    document.acknowledgements = pages[current_page]
    current_page += 1

    document.abstract = pages[current_page]
    current_page += 1

    document.turkish_abstract = pages[current_page]
    current_page += 1

    document.toc = []
    for i in range(options.toc_length):
        document.toc.append(pages[current_page])
        current_page += 1

    document.figures = []
    for i in range(options.figures_length):
        document.figures.append(pages[current_page])
        current_page += 1

    document.tables = []
    for i in range(options.tables_length):
        document.tables.append(pages[current_page])
        current_page += 1

    document.symbols = []
    for i in range(options.symbols_length):
        document.symbols.append(pages[current_page])
        current_page += 1

    document.acronyms = []
    for i in range(options.acronyms_length):
        document.acronyms.append(pages[current_page])
        current_page += 1

    document.introduction = []
    for i in range(options.introduction_length):
        document.introduction.append(pages[current_page])
        current_page += 1

    document.body = []
    for i in range(options.body_length):
        document.body.append(pages[current_page])
        current_page += 1

    document.conclusion = []
    for i in range(options.conclusion_length):
        document.conclusion.append(pages[current_page])
        current_page += 1

    document.references = []
    for i in range(options.reference_length):
        document.references.append(pages[current_page])
        current_page += 1

    document.appendix = []
    for i in range(current_page, len(pages)):
        document.appendix.append(pages[i])

    return document

def get_errors(options: Options, file_name):
    pdf_pages = extract_pages(file_name, laparams=LAParams(line_overlap=0.4, char_margin=6, line_margin=0.2, detect_vertical=True))
    parsed_pages = __extract_elements(pdf_pages)

    for page in parsed_pages:
        page.lines.sort(key= lambda line : line.box.y1, reverse=True)

    errors = {}

    document = __get_document(options, parsed_pages)
    
    line_space = 10

    title_errors, title = check_title(document.title, line_space)
    errors["title"] = title_errors
    errors["approval"] = check_approval(document.approval, line_space, title)
    errors["acknowledgements"] = check_acknowledgements(document.acknowledgements, line_space)
    errors["abstract"] = check_abstract(document.abstract, line_space, title)
    errors["turkish_abstract"] = check_abstract_tr(document.turkish_abstract, line_space, title)
    errors["toc"] = check_toc(document)
    errors["figures"] = check_figures(document.figures, line_space)
    errors["tables"] = check_tables(document.tables, line_space)
    errors["symbols"] = check_symbols(document.symbols, line_space)
    errors["acronyms"] = check_acronyms(document.acronyms, line_space)
    _, left_margin, new_paragraph_margin = check_introduction(document.introduction, line_space)
    errors["introduction"] = check_body(document.introduction, line_space, 0, left_margin, new_paragraph_margin)
    errors["body"] = check_body(document.body, line_space, options.introduction_length, left_margin, new_paragraph_margin)
    errors["conclusion"] = check_body(document.conclusion, line_space, options.introduction_length+options.body_length, left_margin, new_paragraph_margin)
    errors["references"] = check_references(document.references)
    return errors
