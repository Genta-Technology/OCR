"""
This is basic command line interface when the user inputted their pdf files
and then we save the output as a txt file
"""

from interface.basic_interface import main_user_interface, finish_user_interface, end_user_interface
from modules.pdf_ocr import search_file_name, select_file, do_ocr

while True:
    main_user_interface()

    pdf_paths, pdf_names = search_file_name()
    pdf_path, pdf_name = select_file(pdf_paths, pdf_names)

    return_path = do_ocr(pdf_path, pdf_name)

    finish_user_interface(return_path)

    loop = end_user_interface()
    if loop:
        break