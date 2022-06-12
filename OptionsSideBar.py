from tkinter import *
from ScrollableFrame import ScrollableFrame

from pdfparser.parse_pdf import Options

class OptionsSideBar:
    def __init__(self, root, options: Options, set_page_names, finish_selecting) -> None:
        self.entries: list[Button] = []
        self.options = options
        self.set_page_names = set_page_names
        
        frame = ScrollableFrame(root, 500, 850)
        frame.grid(row=1, column=1)


        sidebar = frame.scrollable_frame


        dedication_length_label = Label(sidebar, text="Please enter the length of your Dedication Page. (0 if not present)").pack( expand=True, pady=3)
        dedication_length_entry = Entry(sidebar)
        dedication_length_entry.pack(side="top", expand=True, pady=3)
        dedication_length_entry.insert(0, "0")
        self.entries.append(dedication_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()
        
        
        foreword_length_label = Label(sidebar, text="Please enter the length of your Foreword Page. (0 if not present).").pack( expand=True, pady=3)
        foreword_length_entry = Entry(sidebar)
        foreword_length_entry.pack(side="top", expand=True, pady=3)
        foreword_length_entry.insert(0, "0")
        self.entries.append(foreword_length_entry) 
        Button(sidebar, text="Set", command=self.set_entries).pack()       

        preface_length_label = Label(sidebar, text="Please enter the length of your Preface Page. (0 if not present).").pack( expand=True, pady=3)
        preface_length_entry = Entry(sidebar)
        preface_length_entry.pack(side="top", expand=True, pady=3)
        preface_length_entry.insert(0, "0")
        self.entries.append(preface_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        toc_length_label = Label(sidebar, text="Please enter the length of your Table of Content Page.").pack( expand=True, pady=3)
        toc_length_entry = Entry(sidebar)
        toc_length_entry.pack( expand=True, pady=3)
        toc_length_entry.insert(0, "0")
        self.entries.append(toc_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        figures_length_label = Label(sidebar, text="Please enter the length of your List of Figures Page. (0 if not present).").pack( expand=True, pady=3)
        figures_length_entry = Entry(sidebar)
        figures_length_entry.pack( expand=True, pady=3)
        figures_length_entry.insert(0, "0")
        self.entries.append(figures_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        tables_length_label = Label(sidebar, text="Please enter the length of your List of Tables Page. (0 if not present).").pack( expand=True, pady=3)
        tables_length_entry = Entry(sidebar)
        tables_length_entry.pack( expand=True, pady=3)
        tables_length_entry.insert(0, "0")
        self.entries.append(tables_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        symbols_length_label = Label(sidebar, text="Please enter the length of your List of Symbols Page. (0 if not present).").pack( expand=True, pady=3)
        symbols_length_entry = Entry(sidebar)
        symbols_length_entry.pack( expand=True, pady=3)
        symbols_length_entry.insert(0, "0")
        self.entries.append(symbols_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        acronyms_length_label = Label(sidebar, text="Please enter the length of your List of Acronyms Page. (0 if not present).").pack( expand=True, pady=3)
        acronyms_length_entry = Entry(sidebar)
        acronyms_length_entry.pack( expand=True, pady=3)
        acronyms_length_entry.insert(0, "0")
        self.entries.append(acronyms_length_entry)
        Button(sidebar, text="Set", command=self.set_entries).pack()

        introduction_length_label = Label(sidebar, text="Please enter the length of your Introduction.").pack( expand=True, pady=3)
        introduction_length_entry = Entry(sidebar)
        introduction_length_entry.pack( expand=True, pady=3)
        introduction_length_entry.insert(0, "1")
        self.entries.append(introduction_length_entry)
        int_button = Button(sidebar, text="Set", command=self.set_entries).pack()

        body_length_label = Label(sidebar, text="Please enter the length of your Main Body.").pack( expand=True, pady=3)
        body_length_entry = Entry(sidebar)
        body_length_entry.pack( expand=True)
        body_length_entry.insert(0, "1")
        self.entries.append(body_length_entry)
        body_button = Button(sidebar, text="Set", command=self.set_entries).pack()

        conclusion_length_label = Label(sidebar, text="Please enter the length of your Conclusion.").pack( expand=True, pady=3)
        conclusion_length_entry = Entry(sidebar)
        conclusion_length_entry.pack( expand=True)
        conclusion_length_entry.insert(0, "1")
        self.entries.append(conclusion_length_entry)
        conc_button = Button(sidebar, text="Set", command=self.set_entries).pack()

        references_length_label = Label(sidebar, text="Please enter the length of your References.").pack( expand=True, pady=3)
        references_length_entry = Entry(sidebar)
        references_length_entry.pack( expand=True, pady=3)
        references_length_entry.insert(0, "1")
        self.entries.append(references_length_entry)
        ref_button = Button(sidebar, text="Set", command=self.set_entries).pack()

        submit_button = Button(sidebar, text="Submit", command=finish_selecting).pack(pady=10)

    def set_entries(self):
        self.options.dedication_length = int(self.entries[0].get())
        self.options.foreword_length = int(self.entries[1].get())
        self.options.preface_length = int(self.entries[2].get())
        self.options.toc_length = int(self.entries[3].get())
        self.options.figures_length = int(self.entries[4].get())
        self.options.tables_length = int(self.entries[5].get())
        self.options.symbols_length = int(self.entries[6].get())
        self.options.acronyms_length = int(self.entries[7].get())
        self.options.introduction_length = int(self.entries[8].get())
        self.options.body_length = int(self.entries[9].get())
        self.options.conclusion_length = int(self.entries[10].get())
        self.options.reference_length = int(self.entries[11].get())
        self.set_page_names()