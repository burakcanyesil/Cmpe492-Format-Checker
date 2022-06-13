import shutil
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from pdf2image import convert_from_path
from ScrollableFrame import ScrollableFrame
from OptionsSideBar import OptionsSideBar
from pdfparser.data_classes import *
from pdfparser.parse_pdf import get_errors
import os

imagetks = []

page_names: list[StringVar] = []

options: Options = Options(
    dedication_length=0, 
    foreword_length=0,
    preface_length=0, 
    toc_length=1,
    figures_length=0, 
    tables_length=0, 
    symbols_length=0, 
    acronyms_length=0,
    introduction_length = 1,
    body_length = 1,
    conclusion_length = 1,
    reference_length = 1
    )

introduction_length = 1
body_length = 1
conclusion_length = 1
reference_length = 1

file_name: str

def render_pages(window, images):
    row = 1
    column = 0
    for i in range(len(images)):
        frame = Frame(window)
        image = ImageTk.PhotoImage(images[i])
        
        imagetks.append(image)
        page_names.append(StringVar())

        label = Label(frame, image=image, textvariable=page_names[i], compound="top")
        label.pack()
        frame.grid(row=row, column=column)
        column += 1
        if column == 3:
            column = 0
            row += 1
    for i in range(row+1):
        window.columnconfigure(i, pad=15)
    for i in range(column+1):
        window.rowconfigure(i, pad=15)

def set_page_names():
    global options, introduction_length, body_length, conclusion_length, reference_length
    page_names[0].set("Title")
    page_names[1].set("Approval")
    current_page = 2

    if current_page + options.dedication_length > len(page_names):
        pass
    else:
        for i in range(options.dedication_length):
            page_names[current_page].set("Dedication")
            current_page += 1

    if current_page + options.foreword_length > len(page_names):
        pass
    else:
        for i in range(options.foreword_length):
            page_names[current_page].set("Foreword")
            current_page += 1

    if current_page + options.preface_length > len(page_names):
        pass
    else:
        for i in range(options.preface_length):
            page_names[current_page].set("Preface")
            current_page += 1

    page_names[current_page].set("Acknowledgements (Should be one page)")
    current_page += 1

    page_names[current_page].set("Abstract (Should be one page)")
    current_page += 1

    page_names[current_page].set("Turkish Abstract (Should be one page)")
    current_page += 1

    if current_page + options.figures_length > len(page_names):
        pass
    else:
        for i in range(options.toc_length):
            page_names[current_page].set("Table of Contents")
            current_page += 1

    if current_page + options.figures_length > len(page_names):
        pass
    else:
        for i in range(options.figures_length):
            page_names[current_page].set("List of Figures")
            current_page += 1

    if current_page + options.tables_length > len(page_names):
        pass
    else:
        for i in range(options.tables_length):
            page_names[current_page].set("List of Tables")
            current_page += 1

    if current_page + options.symbols_length > len(page_names):
        pass
    else:
        for i in range(options.symbols_length):
            page_names[current_page].set("List of Symbols")
            current_page += 1

    if current_page + options.acronyms_length > len(page_names):
        pass
    else:
        for i in range(options.acronyms_length):
            page_names[current_page].set("List of Acronyms/Abbreviations")
            current_page += 1
    
    if current_page + options.introduction_length > len(page_names):
        pass
    else:
        for i in range(options.introduction_length):
            page_names[current_page].set("Introduction")
            current_page += 1
    
    if current_page + options.body_length > len(page_names):
        pass
    else:
        for i in range(options.body_length):
            page_names[current_page].set("Main Body")
            current_page += 1

    if current_page + options.conclusion_length > len(page_names):
        pass
    else:
        for i in range(options.conclusion_length):
            page_names[current_page].set("Conclusion")
            current_page += 1

    if current_page + options.reference_length > len(page_names):
        pass
    else:
        for i in range(options.reference_length):
            page_names[current_page].set("References")
            current_page += 1

    for i in range(current_page, len(page_names)):
        page_names[i].set("Appendix")
   
root = Tk()
root.geometry("1920x1080")

frame = ScrollableFrame(root, 1100, 850)
frame.grid(row=1, column=0, )

# OPEN FILE
file_bar = Frame(root, bg="red")
file_bar.grid(row=0, column=0)

def select_file():
    global file_name
    filetypes = (
        ("PDF File", "*.pdf"),
    )

    file_name =  filedialog.askopenfilename(
        title="Select PDF",
        initialdir="./",
        filetypes=filetypes
    )

    images = convert_from_path(file_name, size=(350, 490))

    if os.path.isdir("./images"):
        shutil.rmtree("./images")

    os.makedirs("./images")
    render_pages(frame.scrollable_frame, images)
    set_page_names()


file_button = Button(
    file_bar,
    text = "Select PDF",
    command=select_file
)

file_button.pack()



# SIDEBAR
# ###################################
def finish_selecting():
    errors = get_errors(options, file_name)
    new_window = Toplevel(root)
    new_window.title("Results")
    new_window.geometry("1280x720")

    frame = ScrollableFrame(new_window, 1200, 700)
    new_container = frame.scrollable_frame
    frame.pack(expand=True, fill="both", side="top")
    Frame(new_container, width=650, height=1).pack(side="top", fill="x", expand=True)
    Label(new_container,
            text="Title Page Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["title"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["title"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["title"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="Approval Page Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["approval"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["approval"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["approval"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")

    Label(new_container,
            text="Acknowledgements Section Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["acknowledgements"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["acknowledgements"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["acknowledgements"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="Abstract Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["abstract"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")
    
    if len(errors["abstract"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["abstract"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="Özet Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["turkish_abstract"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["turkish_abstract"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["turkish_abstract"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="Table of Contents Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["toc"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["toc"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["toc"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="List of Figures Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["figures"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["figures"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["figures"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="List of Tables Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["tables"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["tables"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["tables"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="List of Symbols Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["symbols"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["symbols"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["symbols"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")


    Label(new_container,
            text="List of Acronyms/Abbreviations Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["acronyms"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

    if len(errors["acronyms"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for error in errors["acronyms"]:
            Label(new_container,
                text=error, 
                font="Times 16 bold",
            ).pack(fill="x", side="top")

    int_label = Label(new_container,
            text="Introduction Section Errors", 
            font="Times 32 bold",
            bg = "green"
        )
    int_label.pack(fill="x", pady=40, side="top")
    if len(errors["introduction"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for page, error_list in errors["introduction"].items():
            Label(
                new_container,
                text="Page " + str(page),
                bg="lightgrey",
                font="Times 24 bold"
            ).pack(fill="x", side="top")
            for error in error_list:
                int_label.config(bg="red")
                Label(new_container,
                    text=error, 
                    font="Times 16 bold",
                ).pack(fill="x", side="top")


    body_label = Label(new_container,
            text="Body Section Errors", 
            font="Times 32 bold",
            bg = "green"
        )
    body_label.pack(fill="x", pady=40, side="top")
    if len(errors["body"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for page, error_list in errors["body"].items():
            Label(
                new_container,
                text="Page " + str(page+options.introduction_length),
                bg="lightgrey",
                font="Times 24 bold"
            ).pack(fill="x", side="top")
            for error in error_list:
                body_label.config(bg="red")
                Label(new_container,
                    text=error, 
                    font="Times 16 bold",
                ).pack(fill="x", side="top")


    conc_label = Label(new_container,
            text="Conclusion Errors", 
            font="Times 32 bold",
            bg = "green"
        )
    conc_label.pack(fill="x", pady=40, side="top")

    if len(errors["conclusion"]) == 0:
        Label(new_container,
                text="No errors found!", 
                font="Times 24 bold",
            ).pack(fill="x", side="top")
    else:
        for page, error_list in errors["conclusion"].items():
            Label(
                new_container,
                text="Page " + str(page+options.introduction_length+options.body_length),
                bg="lightgrey",
                font="Times 24 bold"
            ).pack(fill="x", side="top")
            for error in error_list:
                conc_label.config(bg="red")
                Label(new_container,
                    text=error, 
                    font="Times 16 bold",
                ).pack(fill="x", side="top")


    Label(new_container,
            text="References Errors", 
            font="Times 32 bold",
            bg = "green" if len(errors["references"]) == 0 else "red"
        ).pack(fill="x", pady=40, side="top")

        # Not implemented
    Label(new_container,
            text="No errors found!", 
            font="Times 24 bold",
        ).pack(fill="x", side="top")




OptionsSideBar(root, options, set_page_names, finish_selecting)
# ###################################

root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=1)

root.title("Format Checker")

root.mainloop()