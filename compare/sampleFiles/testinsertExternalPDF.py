# !/usr/bin/python

# Recall that PyMuPDF is imported as fitz
import fitz
from fitz.utils import getColor          # function delivers RGB triple for a color name

##############################################################
#https://stackabuse.com/working-with-pdfs-in-python-inserting-deleting-and-reordering-pages/#:~:text=.save(output_file)-,Inserting%20Pages%20with%20PyMuPDF,to%20add%20an%20existing%20page.
##############################################################
original_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//sample.pdf"
extra_page_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//Before.pdf"
output_file_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//example-extended.pdf"
landscape_file_path= "C://Users//Roshith\Desktop//In progress//BIRTsamples//landscape.pdf"

original_pdf = fitz.open(original_pdf_path)
extra_page = fitz.open(extra_page_path)
landscape_page = fitz.open(landscape_file_path)

pink = getColor("pink")
rect = fitz.Rect(0, 0, 50, 50)
pix = fitz.Pixmap("C://Users//Roshith\Desktop//In progress//BIRTsamples//Firefox_Logo.png")        # any supported image file
page = extra_page[0]                          # load page (0-based)
page.insertImage(rect, pixmap=pix, overlay=True)   # insert image

text = "some text containing line breaks and\na prettier mono-spaced font."
fname = "F0"
ffile = "C://Windows//Fonts//TIMESBD.TTF"
where = fitz.Point(300, 100)    # text starts here
# this inserts 2 lines of text using font `DejaVu Sans Mono`
page.insertText(where, text,
                fontname=fname,    # arbitrary if fontfile given
                fontfile=ffile,    # any file containing a font
                fontsize=11,       # default
                rotate=0,          # rotate text
                color=(0, 0, 0),   # some color (blue)
                overlay=True)      # text in foreground


original_pdf.newPage(2,width = 612, height = 792)
original_pdf.insertPDF(extra_page,start_at=1)
original_pdf.insertPDF(landscape_page,start_at=3)
original_pdf.save(output_file_path)