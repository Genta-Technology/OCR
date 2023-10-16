"""
This is the basic command line interface ui
"""

def line():
    print("----------------------------------------------------------")

def strip():
    print("==========================================================")

def main_user_interface():
    strip()
    print("Welcome to the Genta OCR")
    print("Please copy your pdf into the designated pdf_input files \n")
    user_input = input("press the enter key to continue")
    line()

def select_pdf_interface(pdf_names):
    print("We found several files:")
    for i in range(len(pdf_names)):
        print(str(i+1) + ". " + pdf_names[i])
        i += 1
    print("please select one that you would like to convert")
    select = int(input("Please input the file number: "))
    select -= 1
    if select > len(pdf_names):
        print("Your number is not in the list, please try again")
        line()
        select = select_pdf_interface(pdf_names)
    else:
        print("You select: " + pdf_names[select])
    return select

def progress_user_interface(progress, total):
    print("Progress report: " + str(round((progress/total)*100, 4)) + "%")

def finish_user_interface(return_path):
    line()
    print("File is sucessfully saved at: " + return_path)
    line()

def end_user_interface():
    status = input("To convert another file, press enter, to quit, type exit: ")
    if status.lower == "exit":
        return False
    else:
        return True
        
    