from pdfparser.data_classes import Page
from pdfparser.util import eq_with_tolerance

def _get_title(name: str):
    name_arr = name.split()
    
    if name_arr[0] == "Prof.":
        return name_arr[0]
    else:
        return name_arr[0] + " " + name_arr[1]
    
def __clean_points(name: str):
    stop_index = 0
    result = ""
    for index, char in enumerate(name[::-1]):
        if char.isalpha():
            stop_index = index
            break
    
    return name[:-stop_index]

def check_approval(approval: Page, line_space: float, title: str):
    turkish_characters = {"S¸": "Ş",
                    "˙I": "İ",
                    "˘G": "Ğ",
                    "C¸": "Ç",
                    "¨O": "Ö",
                    "¨U": "Ü",
                    "s¸": "ş",
                    "˘g": "ğ",
                    "c¸": "ç",
                    "¨o": "ö",
                    "¨u": "ü",
                    }

    for line in approval.lines:
        for ch, ch_tr in turkish_characters.items():
            line.text = line.text.replace(ch, ch_tr)
            
    errors = []
    valid_titles = ["Prof.", "Assoc. Prof.", "Assist. Prof.", "Assistant Prof.", "Associate Prof."]

    if approval.lines[0].text.lower() != "ii":
        errors.append("Approval page should be enumarated!")

    title_line: str = approval.lines[1].text
    next_line = 2
    if approval.lines[1].box.y1 - approval.lines[2].box.y2 < line_space * 1.1:
        title_line += " " + approval.lines[2].text
        next_line += 1

    if not(title_line.isupper()):
        errors.append("Title should be uppercase!")

    if title_line != title:
        errors.append("Title is different from title page!")

    if approval.lines[next_line].text.lower() != "approved by:":
        errors.append("'APPROVED BY:' line could not be found!")
    elif not (approval.lines[next_line].text.isupper):
        errors.append("'APPROVED BY:' should be uppercase!")
    
    next_line += 1
    thesis_supervisor_name = approval.lines[next_line]
    next_line += 1

    if not(thesis_supervisor_name.text.endswith(" .")):
        thesis_supervisor_signature = approval.lines[next_line]
        next_line += 1

        if not(eq_with_tolerance(thesis_supervisor_signature.box.y1, thesis_supervisor_name.box.y1)):
            errors.append("Signature place of " + thesis_supervisor_name.text + " does not align with their name!")
    else:
        thesis_supervisor_name.text = __clean_points(thesis_supervisor_name.text)

    thesis_supervisor_mark = approval.lines[next_line].text
    next_line += 1

    if (_get_title(thesis_supervisor_name.text)) not in valid_titles:
        errors.append("Title of " + thesis_supervisor_name.text + " is not valid!")
    
    if (thesis_supervisor_mark != "(Thesis Supervisor)"):
        errors.append("Thesis supervisor must have '(Thesis Supervisor)' written under it!")

 

    # Return early to prevent infinite loop
    if "DATE OF APPROVAL" not in approval.lines[-1].text:
        errors.append("Approval page should end with Date of Approval!")
        return errors

    while "DATE OF APPROVAL" not in approval.lines[next_line].text:
        name = approval.lines[next_line]
        
        next_line += 1

        if not (name.text.endswith(" .")):
            signature = approval.lines[next_line]
            next_line += 1

            if not(eq_with_tolerance(signature.box.y1, name.box.y1)):
                errors.append("Signature place of " + name.text + " does not align with their name!")
        else:
            name.text = __clean_points(name.text)



        if (_get_title(name.text)) not in valid_titles:
            errors.append("Title of " + name.text + " is not valid!")

        if ("Dr." in name.text):
            errors.append("Title of " + name.text + " includes 'Dr.'!")



        # Prevent index out of reach
        if next_line > len(approval.lines) - 1:
            return errors
    return errors