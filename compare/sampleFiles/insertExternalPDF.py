# !/usr/bin/python

import fitz

original_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//sample.pdf"
external_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//external.pdf"
landscape_file_path= "C://Users//Roshith\Desktop//In progress//BIRTsamples//landscape.pdf"
output_file_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//example-extended.pdf"

original_pdf = fitz.open(original_pdf_path)
external_pdf = fitz.open(external_pdf_path)
landscape_page = fitz.open(landscape_file_path)

original_pdf.insertPDF(external_pdf,start_at=1)
original_pdf.insertPDF(landscape_page,start_at=3)
original_pdf.insertPDF(external_pdf, to_page = 1)  # first 2 pages
original_pdf.insertPDF(external_pdf, from_page = len(external_pdf) - 1) # last 2 pages

original_pdf.save(output_file_path)