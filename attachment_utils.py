"""
attachment_utils.py

This module provides utility functions for managing file attachments,
particularly for handling CSV files.

Functions:
    - initialise_file_pj(): Sets the path to the directory for sending attachments.
    - prepare_csv(): Prepares and combines CSV tables for analysis and 
      returns them in Markdown format.
"""

import os
import re
import pandas as pd
import pypdfium2 as pdfium

def prepare_csv():
    """
    Prépare et combine les tableaux CSV pour l'analyse.

    Returns:
        str: Une chaîne Markdown représentant les tableaux combinés.
    """
    input_table = []
    csv_filepath = os.getenv("CSV_PATH")
    file_names = os.listdir(csv_filepath)
    csv_files = [file for file in file_names if re.search(r'\.csv$', file)]
    if csv_files:
        combined_table = ''
        for csv in csv_files:
            t = pd.read_csv(csv_filepath + csv, nrows=200)
            merged_df = pd.concat([t.head(5), t.tail(5)], ignore_index=True)
            input_table = merged_df.to_markdown(tablefmt="grid")
            combined_table += 2 * "\n" + 98 * "#" + 2 * "\n" + input_table.strip()
        return combined_table
    return ""

def prepare_pdf():
    """
    Transforme et prépare en image les PDF pour l'analyse.

    Returns:
        Images from pdf
    """
    pdf_filepath = os.getenv("CSV_PATH")
    file_names = os.listdir(pdf_filepath)
    pdf_files = [file for file in file_names if re.search(r'\.pdf$', file)]

    # Check if the /tmp directory already exists
    if pdf_files:
        if not os.path.exists('CSV_PDF/tmp'):
            try:
                # Create the /tmp directory if it does not exist
                os.mkdir(os.path.join(pdf_filepath,'tmp'))
                print("The /tmp directory has been created successfully.")
            except OSError as e:
                # Handle potential errors during directory creation
                print(f"Error creating the /tmp directory: {e.strerror}")
        for pdf  in pdf_files:
            current_pdf = pdfium.PdfDocument(os.path.join(pdf_filepath, pdf))
            for i in range(len(current_pdf)):
                page = current_pdf[i]
                image = page.render(scale=4).to_pil()
                image.save(os.path.join(pdf_filepath, 'tmp', f"output_{i:03d}.jpg"))
                print("Sucessfully processed pdf")