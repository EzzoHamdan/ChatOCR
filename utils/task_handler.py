# utils/task_handler.py
from werkzeug.utils import secure_filename
import os
from utils.file_extraction import extract_image, extract_pdf, extract_docx, extract_pptx

def handle_file(file, upload_folder, pages_input):
    if not file:
        return "", None

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    try:
        if filename.endswith('.pdf'):
            extracted_text = extract_pdf(file_path, pages_input)
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            extracted_text = extract_docx(file_path, pages_input)
        elif filename.endswith('.pptx') or filename.endswith('.ppt'):
            extracted_text = extract_pptx(file_path, pages_input)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            extracted_text = extract_image(file_path)
        else:
            raise ValueError("Unsupported file type.")
    finally:
        os.remove(file_path)  # Clean up

    return extracted_text, filename

def generate_prompt(task, query, extracted_text):
    if task == 'summarize':
        prompt_to_send = f"Summarize this text:\n{extracted_text}"
    elif task == 'question':
        prompt_to_send = f"Answer the following question based on the text:\n{extracted_text}\n\nQuestion: {query}"
    elif task == 'rewrite':
        prompt_to_send = f"Rephrase the following text:\n{extracted_text}"
    elif task == 'explain':
        prompt_to_send = f"Explain the following text for an average person:\n{extracted_text}"
    elif task == 'explainplus':
        prompt_to_send = f"Explain the following text for a dummy:\n{extracted_text}"
    elif task == 'inquiry':
        prompt_to_send = f"Follow the instructions given with the text:\n{extracted_text}"
    return prompt_to_send
