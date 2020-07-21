
#https://github.com/pymupdf/PyMuPDF/wiki/How-to-Make-your-own-PDF-Shape

import fitz


original_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//After.pdf"
output_file_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//shapes.pdf"

doc = fitz.open(original_pdf_path)    # or new: fitz.open(), followed by insertPage()
page1 = doc[0]                         # choose some page
page2 = doc[0]
img = page1.newShape()
img.drawCircle(fitz.Point(200, 200),200)
img.finish(color = (1,0,0), fill = (1,1,0), closePath = False)
img.commit
doc.save(output_file_path)
