"""
This is the utilities function for converting pdf to markdown/latex
"""

import os
import glob
import fitz
from PIL import Image

from optimum.onnxruntime import ORTModelForVision2Seq
from transformers import NougatProcessor, VisionEncoderDecoderModel
import torch

from interface.basic_interface import select_pdf_interface, progress_user_interface

SAVE_FOLDER_PATH = "user_output"

processor = NougatProcessor.from_pretrained("./model")
model = ORTModelForVision2Seq.from_pretrained("./model", encoder_file_name="encoder_model.onnx", decoder_file_name="decoder_model.onnx", use_cache=False)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def search_file_name():
    """
    Search pdf file inside the pdf_input folder

    Returns:
        list of pdf path (String)
        list of pdf name (String)
    """
    pdf_files = glob.glob(os.path.join("user_input", '*.pdf'))
    pdf_paths = []
    pdf_names = []

    for pdf_file in pdf_files:
        pdf_paths.append(pdf_file)
        pdf_names.append(os.path.basename(pdf_file)[:-4])
    
    # print(device)

    return pdf_paths, pdf_names

def select_file(pdf_paths, pdf_names):
    """
    Let the user get all of the file list that can be opened and then
    let them choose which one to convert

    Returns:
        selected pdf path (String)
        selected pdf name (String)
    """
    select_num = select_pdf_interface(pdf_names)
    return pdf_paths[select_num], pdf_names[select_num]

def do_ocr(pdf_path, file_name):
    """
    Main function to do the OCR model inference directly using pdf file
    
    Returns:
        result path (String)
    """
    # Open the pdf files and get the images
    images = pdf_to_images(pdf_path)

    # Model inference
    result = []

    for i in range(len(images)):
        result.append(clean_text(image_to_markdown(images[i])))
        progress_user_interface(i+1, len(images))

    # Saving the result into text file
    save_file(" ".join(result), SAVE_FOLDER_PATH, file_name)

    return SAVE_FOLDER_PATH + "/" + file_name



def pdf_to_images(pdf_path):
    """
    open the pdf path and then convert it into images

    Return
    list of Images
    """
    pdf_document = fitz.open(pdf_path)

    images = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        image = page.get_pixmap()

        image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        images.append(image)

    pdf_document.close()

    return images

def image_to_markdown(image):
  """
  Run the model inference, from image to markdown

  Return:
    model output/Markdown (String)
  """
  pixel_values = processor(image, return_tensors="pt").pixel_values

  outputs = model.generate(
    pixel_values.to(device).half(),
    min_length=1,
    max_new_tokens=512,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
  )

  sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
  sequence = processor.post_process_generation(sequence, fix_markdown=False)

  return sequence

def clean_text(input_string):
    """
    Clean the text for better clarity

    Return:
        text (String)
    """
    modified_string = input_string.replace('//(', '$').replace('//)', '$')
    return modified_string

def save_file(input_string, folder_path, file_name):
    """
    Save the file into designated folder and path

    Return:
        file location (String)
    """
    try:
        # Ensure the folder_path exists, create if not
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = os.path.join(folder_path, file_name + '.txt')
        
        with open(file_path, 'w') as file:
            file.write(input_string)
    except Exception as e:
        print(f'Error: {e}')

