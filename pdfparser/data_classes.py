from dataclasses import dataclass


@dataclass
class Options:
    dedication_length: int
    foreword_length: int
    preface_length: int
    toc_length: int
    figures_length: int
    tables_length: int
    symbols_length: int
    acronyms_length: int
    introduction_length: int
    body_length: int
    conclusion_length: int
    reference_length: int

@dataclass
class Box:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclass
class Line:
    text: str
    box: Box
    vertical: bool = False

@dataclass
class Page:
    pageid: int
    box: Box
    lines: list[Line]

class Document:
    title: Page = None
    approval: Page = None
    dedication: list[Page] = []
    foreword: list[Page] = []
    preface: list[Page] = []
    acknowledgements: Page = None
    abstract: Page = None
    turkish_abstract: Page = None
    toc: list[Page] = None
    figures: list[Page] = []
    tables: list[Page] = []
    symbols: list[Page] = []
    acronyms: list[Page] = []
    introduction: list[Page] = []
    body: list[Page] = []
    conclusion: list[Page] = []
    references: list[Page] = []
    appendix: list[Page] = []

    def __init__(self) -> None:
        pass
